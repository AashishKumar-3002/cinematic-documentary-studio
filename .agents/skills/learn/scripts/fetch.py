"""Read public media and GitHub source into project-local learning bundles."""
from __future__ import annotations
import argparse, hashlib, html, importlib.util, ipaddress, json, os, re, socket, subprocess, sys, tempfile
import urllib.parse, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'tools'))
from studio_runtime import find_tool
os.environ['HF_HOME'] = str(ROOT/'.cache/huggingface')
os.environ['PIP_CACHE_DIR'] = str(ROOT/'.cache/pip')
TMP = ROOT/'.cache/tmp'
TMP.mkdir(parents=True, exist_ok=True)
research_python=ROOT/'.research-venv'/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
YTPY = Path(sys.executable) if importlib.util.find_spec('yt_dlp') or not research_python.is_file() else research_python
MEDIA = {'.mp3','.wav','.m4a','.mp4','.webm','.ogg','.flac','.opus','.mov','.mkv'}

def run(args):
    p = subprocess.run([str(x) for x in args], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=1800)
    if p.returncode: raise RuntimeError(p.stderr[-1500:] or p.stdout[-1500:])
    return p.stdout

def public_url(url):
    u=urllib.parse.urlsplit(url)
    if u.scheme not in ('https','http') or not u.hostname or u.username or u.password:
        raise ValueError('Use a public HTTP(S) URL without credentials')
    addresses=socket.getaddrinfo(u.hostname,u.port or (443 if u.scheme=='https' else 80))
    if any(not ipaddress.ip_address(x[4][0].split('%')[0]).is_global for x in addresses):
        raise ValueError('Private-network URLs are not supported')

class Redirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        public_url(newurl)
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def get(url, limit=4*1024*1024):
    public_url(url)
    opener=urllib.request.build_opener(Redirects())
    with opener.open(urllib.request.Request(url,headers={'User-Agent':'Documentary-Learn/1.0','Accept':'application/vnd.github+json' if 'api.github.com' in url else '*/*'}),timeout=60) as r:
        data=r.read(limit+1)
    if len(data)>limit: raise ValueError(f'Source exceeds {limit} byte limit')
    return data

def folder_for(out,title,source):
    name=re.sub('[^a-z0-9]+','-',title.lower()).strip('-')[:55] or 'source'
    p=out/(name+'-'+hashlib.sha256(source.encode()).hexdigest()[:8])
    p.mkdir(parents=True,exist_ok=True)
    return p

def stamp(t):
    return f'{int(t)//3600}:{int(t)%3600//60:02d}:{int(t)%60:02d}'

def yt(*args):
    return run([YTPY,'-m','yt_dlp','--ignore-config','--no-warnings','--no-cache-dir','--js-runtimes','node','--socket-timeout','30','--retries','2',*args])

def transcribe(path,model):
    from faster_whisper import WhisperModel
    print(f'Local transcription: {model}',flush=True)
    m=WhisperModel(model,device='cpu',compute_type='int8',cpu_threads=2,download_root=str(ROOT/'models/whisper'))
    segs,info=m.transcribe(str(path),word_timestamps=True)
    rows=[{'start':s.start,'end':s.end,'text':s.text.strip()} for s in segs]
    return rows,info.language

def github(url,out,max_files):
    parts=urllib.parse.urlsplit(url).path.strip('/').split('/')
    if len(parts)<2: raise ValueError('Provide a GitHub repository URL')
    owner,repo=parts[:2]; repo=repo.removesuffix('.git')
    api=f'https://api.github.com/repos/{owner}/{repo}'
    meta=json.loads(get(api)); ref=meta['default_branch']; only=None
    if len(parts)>2:
        if parts[2] not in ('tree','blob') or len(parts)<4: raise ValueError('Use a repository, tree, or blob URL')
        ref=parts[3]; only='/'.join(parts[4:])
    commit=json.loads(get(api+'/commits/'+urllib.parse.quote(ref,safe='')))['sha']
    tree=json.loads(get(api+'/git/trees/'+commit+'?recursive=1',limit=16*1024*1024))
    paths=[r['path'] for r in tree['tree'] if r['type']=='blob' and r.get('size',0)<=150000]
    if only: paths=[p for p in paths if p==only or p.startswith(only.rstrip('/')+'/')]
    priorities=lambda p:(0 if Path(p).name.lower().startswith('readme') else 1 if p.endswith('SKILL.md') else 2 if p.startswith(('docs/','examples/')) else 3,p)
    docs=sorted([p for p in paths if Path(p).suffix.lower() in ('.md','.rst','.txt','.toml','.json','.py','.js','.ts','.tsx','.html','.htm','.css','.svg')],key=priorities)
    selected=docs[:max_files]; folder=folder_for(out,owner+'-'+repo,url); chunks=[]
    for path in selected:
        raw=f'https://raw.githubusercontent.com/{owner}/{repo}/{commit}/'+urllib.parse.quote(path,safe='/')
        content=get(raw,limit=150000).decode('utf-8',errors='replace')
        chunks.append(f'## File: {path}\nSource: {raw}\n\n{content}\n')
    if not selected: raise ValueError('No supported text files found')
    (folder/'repository.md').write_text('\n'.join(chunks),encoding='utf-8')
    return folder,{'title':owner+'/'+repo,'source':url,'how':'GitHub source read only','commit':commit,'files':selected,'eligible_files':len(docs),'truncated_tree':tree.get('truncated',False),'scope':'Selected text files only; repository code was not executed'}

def media(source,out,model,frames):
    local=Path(source).is_file(); info={}; rows=None; language=None
    with tempfile.TemporaryDirectory(dir=TMP) as td:
        work=Path(td); audio=None
        if local: audio=Path(source).resolve(); title=audio.stem
        else:
            public_url(source)
            info=json.loads(yt('--skip-download','--no-playlist','--dump-single-json','--',source))
            title=info.get('title') or 'media'
            print(f'Reading: {title}',flush=True)
            lang=info.get('language') or 'en'
            for table,flag in [(info.get('subtitles') or {},'--write-subs'),(info.get('automatic_captions') or {},'--write-auto-subs')]:
                for code in dict.fromkeys([lang,lang+'-orig','en','en-orig']):
                    if code not in table: continue
                    try:
                        yt('--skip-download','--no-playlist',flag,'--sub-langs',code,'--sub-format','json3','-o',str(work/'cap.%(ext)s'),'--',source)
                        files=list(work.glob('cap*.json3'))
                        if not files: continue
                        events=json.loads(files[0].read_text(encoding='utf-8')).get('events',[])
                        rows=[]
                        for e in events:
                            text=html.unescape(''.join(s.get('utf8','') for s in e.get('segs',[]))).strip()
                            if text and (not rows or text!=rows[-1]['text']):
                                start=e.get('tStartMs',0)/1000
                                rows.append({'start':start,'end':start+e.get('dDurationMs',0)/1000,'text':text})
                        if rows: language=code; break
                    except Exception as exc: print(f'Caption attempt failed: {exc}',flush=True)
                    finally:
                        for f in work.glob('cap*.json3'): f.unlink()
                if rows: break
            if not rows:
                yt('--no-playlist','--max-filesize','1G','-f','bestaudio/best','-o',str(work/'audio.%(ext)s'),'--',source)
                audio=next(work.glob('audio.*'),None)
                if audio is None: raise RuntimeError('Audio download failed or exceeded 1 GB')
        how='captions' if rows else 'local transcription'
        if not rows: rows,language=transcribe(audio,model)
        if not rows: raise RuntimeError('No spoken words found')
        folder=folder_for(out,title,source)
        (folder/'transcript.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
        (folder/'transcript.md').write_text(f'# {title}\n\nSource: {source}\nWords from: {how}\n\n'+'\n'.join(f"[{stamp(r['start'])}] {r['text']}" for r in rows)+'\n',encoding='utf-8')
        frame_files=[]
        if frames:
            video=audio if local and audio.suffix.lower() in ('.mp4','.webm','.mov','.mkv') else None
            if video is None and not local:
                yt('--no-playlist','--max-filesize','1G','-f','bestvideo[height<=720]/best[height<=720]/best','-o',str(work/'video.%(ext)s'),'--',source)
                video=next(work.glob('video.*'),None)
            if video is not None:
                duration=float(info.get('duration') or rows[-1]['end'])
                from PIL import Image,ImageDraw
                sheet=Image.new('RGB',(640*min(3,frames),390*((frames+2)//3)), '#101b20')
                for i in range(frames):
                    t=duration*(i+.5)/frames; f=folder/f'frame-{i:02d}-{int(t)}s.jpg'
                    run([find_tool('ffmpeg'),'-y','-v','error','-ss',t,'-i',video,'-frames:v','1','-vf','scale=640:-1',f])
                    with Image.open(f) as im: sheet.paste(im,(i%3*640,i//3*390+28))
                    ImageDraw.Draw(sheet).text((i%3*640+10,i//3*390+7),stamp(t),fill='white')
                    frame_files.append({'file':f.name,'seconds':t})
                sheet.save(folder/'contact-sheet.jpg')
        return folder,{'title':title,'source':source,'how':how,'language':language,'channel':info.get('uploader'),'duration':info.get('duration'),'frames':frame_files,'visual_limit':'Sampled frames only' if frame_files else 'No screen content inspected'}

def expand(source,latest):
    u=urllib.parse.urlsplit(source)
    if u.hostname in ('github.com','www.github.com') or Path(source).is_file(): return [source]
    if u.path.endswith(('.rss','.xml')) or 'feed' in u.path.lower() or (u.hostname or '').startswith('feeds.'):
        tree=ET.fromstring(get(source)); urls=[]
        for item in tree.findall('./channel/item'):
            enc=item.find('enclosure')
            if enc is not None and enc.get('url'): urls.append(enc.get('url'))
        if not urls: raise ValueError('No RSS audio enclosures found')
        return urls[:latest or 1]
    if u.hostname in ('youtube.com','www.youtube.com','m.youtube.com') and (u.path=='/playlist' or u.path.startswith(('/@','/channel/'))):
        data=json.loads(yt('--flat-playlist','--playlist-end',latest or 5,'--dump-single-json','--',source))
        return [e.get('webpage_url') or e.get('url') for e in data.get('entries',[]) if e]
    return [source]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('sources',nargs='+'); p.add_argument('--out',type=Path,default=ROOT/'learned')
    p.add_argument('--model',default='tiny.en'); p.add_argument('--latest',type=int)
    p.add_argument('--frames',type=int,default=0); p.add_argument('--max-files',type=int,default=20)
    a=p.parse_args()
    if not 0<=a.frames<=20 or not 1<=a.max_files<=50 or (a.latest is not None and not 1<=a.latest<=20): p.error('Limits: frames 0..20, files 1..50, latest 1..20')
    done=[]; failed=[]
    for source in a.sources:
        try: items=expand(source,a.latest)
        except Exception as exc: failed.append({'source':source,'error':str(exc)}); continue
        for item in items:
            try:
                host=urllib.parse.urlsplit(item).hostname
                folder,meta=github(item,a.out,a.max_files) if host in ('github.com','www.github.com') else media(item,a.out,a.model,a.frames)
                meta['retrieved_at']=datetime.now(timezone.utc).isoformat()
                (folder/'source.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False),encoding='utf-8')
                done.append({'folder':str(folder),**meta}); print(f'OK: {folder}',flush=True)
            except Exception as exc: failed.append({'source':item,'error':str(exc)}); print(f'FAILED: {item}: {exc}',flush=True)
    print(json.dumps({'done':done,'failed':failed},indent=2,ensure_ascii=False))
    return 1 if failed else 0

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8',errors='replace')
    raise SystemExit(main())
