"""Verify the assembled deliverable and generate a contact sheet from the actual MP4."""
import hashlib
import json
import re
import subprocess
from pathlib import Path
from PIL import Image,ImageDraw
from studio_runtime import find_tool

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'projects/lake-nyos/film'
video=P/'out/lake-nyos-full-v1-1080p.mp4'
ffmpeg=find_tool('ffmpeg');probe=find_tool('ffprobe')
meta=json.loads(subprocess.check_output([probe,'-v','error','-show_streams','-show_format','-of','json',str(video)]))
v=next(s for s in meta['streams'] if s['codec_type']=='video')
a=next(s for s in meta['streams'] if s['codec_type']=='audio')
assert int(v['nb_frames'])==9856
assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'30/1')
assert abs(float(v['duration'])-float(a['duration']))<1/30
review=P/'out/final-review';review.mkdir(exist_ok=True)
sheet=Image.new('RGB',(1280,4*388),(12,18,24));d=ImageDraw.Draw(sheet)
for i,t in enumerate([3,65,115,178,221,270,315,325]):
    path=review/f't{t:03d}.jpg'
    subprocess.run([ffmpeg,'-v','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1','-vf','scale=640:-2','-q:v','2',str(path)],check=True)
    x,y=(i%2)*640,(i//2)*388
    sheet.paste(Image.open(path),(x,y));d.text((x+12,y+365),f'Final MP4 / {t}s',fill='white')
sheet.save(P/'release/final-film-frames.jpg',quality=93)
measure=subprocess.run([ffmpeg,'-v','info','-i',str(video),'-vn','-af',
    'loudnorm=I=-15:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
match=re.search(r'\{\s*"input_i".*?\}',measure.stderr,re.S)
loudness=json.loads(match.group()) if match else None
sha=hashlib.sha256()
with video.open('rb') as f:
    while block:=f.read(1024*1024):sha.update(block)
report={'video':video.name,'width':v['width'],'height':v['height'],'fps':30,'frames':int(v['nb_frames']),
    'video_duration_seconds':float(v['duration']),'audio_duration_seconds':float(a['duration']),
    'size_bytes':video.stat().st_size,'sha256':sha.hexdigest(),
    'complete_decode':'passed in checkpoint renderer','final_stills_extracted':8,
    'captions':'68 validated cues; captions.en.srt','loudness_measurement':loudness,
    'publication_status':'not uploaded; no channel connected'}
(P/'release/final-checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
record=json.loads((P/'release/release-record.json').read_text())
record.update(status='render complete; ready for full human review; not uploaded',
              actual_duration_seconds=float(v['duration']),video_sha256=sha.hexdigest(),verification='final-checks.json')
(P/'release/release-record.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2),flush=True)
