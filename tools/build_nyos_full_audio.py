"""Produce section-length Heart takes and align the approved script without recutting delivery."""
import difflib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro
from faster_whisper import WhisperModel
from studio_runtime import find_tool

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'projects/lake-nyos/film'
A=P/'audio'
(P/'out').mkdir(parents=True,exist_ok=True)
(A/'takes').mkdir(parents=True,exist_ok=True)
(A/'alignment').mkdir(exist_ok=True)
script=json.loads((P/'script.json').read_text(encoding='utf-8'))
tts=Kokoro(str(ROOT/'models/kokoro-v1.0.onnx'),str(ROOT/'models/voices-v1.0.bin'))
for i,take in enumerate(script['takes']):
    dest=A/'takes'/f"{take['take']}.wav"
    if not dest.exists():
        approved_take=ROOT/'projects/lake-nyos/opening/audio/auditions/C-heart.wav'
        if i==0 and approved_take.exists():
            shutil.copy2(approved_take,dest)
        else:
            text='\n\n'.join(l['spoken'] for l in take['lines'])
            (dest.with_suffix('.txt')).write_text(text,encoding='utf-8')
            samples,rate=tts.create(text,voice='af_heart',speed=.90,lang='en-us',
                continuous=True,sentence_pause=.42,clause_pause=.13)
            sf.write(str(dest),samples,rate)
    print(f'{take["take"]}: {sf.info(str(dest)).duration:.2f}s',flush=True)

model=WhisperModel('tiny.en',device='cpu',compute_type='int8',download_root=str(ROOT/'models/whisper'))
for take in script['takes']:
    target=A/'alignment'/f"{take['take']}.json"
    if target.exists():continue
    segs,_=model.transcribe(str(A/'takes'/f"{take['take']}.wav"),language='en',word_timestamps=True)
    words=[{'word':w.word.strip(),'start':w.start,'end':w.end,'probability':w.probability}
           for s in segs for w in s.words or []]
    target.write_text(json.dumps(words,indent=2),encoding='utf-8')
    print(f'aligned {take["take"]}: {len(words)} words',flush=True)

def normalize(text):
    text=text.lower().replace('kilometres','kilometers').replace('travelled','traveled')
    for a,b in [('nineteen eighty-six','1986'),('seventeen hundred','1700'),
                ('two thousand and one','2001'),('twenty-five','25'),('carbon dioxide','carbon dioxide')]:
        text=text.replace(a,b)
    return re.findall(r'[a-z0-9]+',text)

rate=24000
lead=.6
parts=[np.zeros(round(lead*rate),np.float32)]
cursor=lead
timeline=[]; report=[]; chapters=[]
for ci,take in enumerate(script['takes']):
    wav=A/'takes'/f"{take['take']}.wav"
    samples,sr=sf.read(str(wav),dtype='float32');assert sr==rate
    words=json.loads((A/'alignment'/f"{take['take']}.json").read_text())
    expected=[]; spans=[]
    for l in take['lines']:
        ts=normalize(l['spoken']);spans.append((len(expected),len(expected)+len(ts)));expected.extend(ts)
    heard=[];word_indices=[]
    for wi,w in enumerate(words):
        tok=normalize(w['word']);heard.extend(tok);word_indices.extend([wi]*len(tok))
    matching=difflib.SequenceMatcher(None,expected,heard,autojunk=False)
    mapping={a+k:b+k for a,b,n in matching.get_matching_blocks() for k in range(n)}
    coverage=len(mapping)/len(expected)
    if coverage<.90:
        raise RuntimeError(f'{take["take"]}: only {coverage:.1%} aligned; review transcription')
    for l,(a,b) in zip(take['lines'],spans):
        matches=[mapping[k] for k in range(a,b) if k in mapping]
        assert matches, l['id']
        w0,w1=word_indices[min(matches)],word_indices[max(matches)]
        selected=words[w0:w1+1]
        start,end=selected[0]['start']+cursor,selected[-1]['end']+cursor
        timeline.append({'id':l['id'],'scene':take['take'],'caption':l['text'],'vo':l['spoken'],
            'start':round(start,3),'end':round(end,3),'duration':round(end-start,3),
            'words':[{'word':w['word'],'start':round(w['start']+cursor,3),'end':round(w['end']+cursor,3)} for w in selected]})
    chapters.append({'chapter':ci+1,'take':take['take'],'start':round(cursor,3),'end':round(cursor+len(samples)/rate,3),
                     'first_line':take['lines'][0]['id'],'last_line':take['lines'][-1]['id']})
    report.append({'take':take['take'],'matched_word_fraction':round(coverage,4),'seconds':round(len(samples)/rate,3)})
    parts.append(samples);cursor+=len(samples)/rate
    gap=1.5 if ci<len(script['takes'])-1 else 7
    parts.append(np.zeros(round(gap*rate),np.float32));cursor+=gap
sf.write(str(A/'narration-continuous.wav'),np.concatenate(parts),rate)
subprocess.run([find_tool('ffmpeg'),'-y','-v','error','-i',str(A/'narration-continuous.wav'),
    '-af','loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000','-c:a','aac','-b:a','192k',str(A/'narration.m4a')],check=True)
(A/'timing.json').write_text(json.dumps({'total_duration':round(cursor,3),'lead_in':lead,'tail_out':7,'tempo':1.,
    'voice':'af_heart','alignment':'faster-whisper tiny.en + normalized token matching; approximate',
    'segments':timeline,'chapters':chapters},indent=2),encoding='utf-8')
(A/'alignment-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
def stamp(t):
    ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(P/'out/captions.srt').write_text('\n\n'.join(f"{i}\n{stamp(s['start'])} --> {stamp(s['end'])}\n{s['caption']}" for i,s in enumerate(timeline,1))+'\n',encoding='utf-8')
print(f'FULL NARRATION: {cursor:.2f}s / {len(timeline)} lines; all sections >=90% token alignment',flush=True)
