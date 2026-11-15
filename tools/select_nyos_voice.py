"""Use the approved C take intact and align its eight sentences to the native film clock."""
import json
import re
import shutil
import subprocess
from pathlib import Path
import soundfile as sf
from studio_runtime import find_tool

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'projects/lake-nyos/opening'
audio=P/'audio'
archive=audio/'archive-george-v1'
archive.mkdir(exist_ok=True)
for name in ['narration.m4a','timing.json','segments.json']:
    if (audio/name).exists() and not (archive/name).exists():
        shutil.copy2(audio/name,archive/name)
src=audio/'auditions/C-heart.wav'
recognition=json.loads((audio/'auditions/C-selected-alignment.json').read_text(encoding='utf-8'))
lines=json.loads((P/'script.json').read_text(encoding='utf-8'))['takes'][0]['lines']
assert len(recognition['segments'])==len(lines)==8, 'Review sentence alignment before continuing'
lead,tail=.6,1.5
info=sf.info(str(src))
duration=lead+info.duration+tail
segments=[]
for line,rec in zip(lines,recognition['segments']):
    segments.append({'id':line['id'],'scene':'opening','caption':line['text'],'vo':line['spoken'],
                     'start':round(rec['start']+lead,3),'end':round(rec['end']+lead,3),
                     'duration':round(rec['end']-rec['start'],3),
                     'words':[{'word':w['word'].strip(),'start':round(w['start']+lead,3),
                               'end':round(w['end']+lead,3)} for w in rec['words']]})
subprocess.run([find_tool('ffmpeg'),'-y','-v','error','-i',str(src),
                '-af',f'adelay=600:all=1,apad=pad_dur={tail},loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000',
                '-c:a','aac','-b:a','192k',str(audio/'narration.m4a')],check=True)
(audio/'timing.json').write_text(json.dumps({'total_duration':round(duration,3),'lead_in':lead,
    'tail_out':tail,'tempo':1.0,'voice':'af_heart','source':'auditions/C-heart.wav',
    'alignment':'faster-whisper tiny.en word timestamps; automated, approximate','segments':segments},indent=2),encoding='utf-8')
def stamp(t):
    ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(P/'out/opening-captions.srt').write_text('\n\n'.join(f"{i}\n{stamp(s['start'])} --> {stamp(s['end'])}\n{s['caption']}" for i,s in enumerate(segments,1))+'\n',encoding='utf-8')
print(f'Approved C take preserved intact; {duration:.3f}s including lead/tail; 8 aligned lines')
