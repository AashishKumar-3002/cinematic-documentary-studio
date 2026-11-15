"""Download project-local runtime files; model hashes match the verified pilot environment."""
import argparse
import hashlib
import json
import platform
import re
import shutil
import urllib.request
import zipfile
from pathlib import Path
from studio_runtime import find_tool

ROOT=Path(__file__).resolve().parents[1]
MODELS={
    'kokoro-v1.0.onnx':'beb0d1848dee9a49da392cc3df26958d46cfa35d321edf434f52949153f0df3a',
    'voices-v1.0.bin':'bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d',
}
BASE='https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/'

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def download(url,path,expected):
    if path.exists() and digest(path)==expected:
        print(f'Verified existing {path.name}',flush=True);return
    path.parent.mkdir(parents=True,exist_ok=True)
    partial=path.with_suffix(path.suffix+'.part')
    req=urllib.request.Request(url,headers={'User-Agent':'Cinematic-Documentary-Studio/1.0'})
    print(f'Downloading {path.name}',flush=True)
    with urllib.request.urlopen(req,timeout=120) as src,partial.open('wb') as out:
        shutil.copyfileobj(src,out)
    if digest(partial)!=expected:raise RuntimeError(f'SHA-256 mismatch: {path.name}; partial file was not installed')
    partial.replace(path)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--models',action='store_true')
    p.add_argument('--ffmpeg',action='store_true')
    p.add_argument('--check',action='store_true',help='Check existing files without downloading')
    a=p.parse_args()
    if a.check:
        result={'models':{name:(ROOT/'models'/name).is_file() and digest(ROOT/'models'/name)==sha for name,sha in MODELS.items()},
                'ffmpeg':all(find_tool(name,required=False) for name in ['ffmpeg','ffprobe'])}
        print(json.dumps(result,indent=2));return 0 if all(result['models'].values()) and result['ffmpeg'] else 1
    if a.models:
        for name,sha in MODELS.items():download(BASE+name,ROOT/'models'/name,sha)
    if a.ffmpeg:
        if platform.system()!='Windows':
            for name in ['ffmpeg','ffprobe']:find_tool(name)
            print('Using existing FFmpeg/FFprobe; no system packages changed',flush=True)
            return 0
        target=ROOT/'tools/bin';target.mkdir(parents=True,exist_ok=True)
        for name in ['ffmpeg.exe','ffprobe.exe']:
            src=shutil.which(name)
            if not (target/name).exists() and src:shutil.copy2(src,target/name)
        if not all((target/n).exists() for n in ['ffmpeg.exe','ffprobe.exe']):
            url='https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
            checksum=urllib.request.urlopen(url+'.sha256',timeout=30).read().decode()
            match=re.search(r'\b[a-fA-F0-9]{64}\b',checksum)
            if not match:raise RuntimeError('Vendor SHA-256 was unavailable; no binary installed')
            archive=ROOT/'.cache/downloads/ffmpeg-release-essentials.zip'
            download(url,archive,match.group().lower())
            with zipfile.ZipFile(archive) as z:
                for name in ['ffmpeg.exe','ffprobe.exe']:
                    members=[n for n in z.namelist() if n.endswith('/bin/'+name)]
                    if len(members)!=1:raise RuntimeError(f'Unexpected FFmpeg archive layout: {name}')
                    with z.open(members[0]) as src,(target/name).open('wb') as out:shutil.copyfileobj(src,out)
                for member in z.namelist():
                    if Path(member).name.upper().startswith('LICENSE') and not member.endswith('/'):
                        with z.open(member) as src,(target/'FFMPEG-LICENSE.txt').open('wb') as out:shutil.copyfileobj(src,out)
                        break
        print('FFmpeg and FFprobe are available under tools/bin',flush=True)
    if not (a.models or a.ffmpeg):p.print_help()
    return 0

if __name__=='__main__':raise SystemExit(main())
