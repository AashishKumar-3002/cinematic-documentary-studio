"""Continuous-section voice auditions; preserve approved narration and original scratch audio."""
import json
import subprocess
from pathlib import Path
import soundfile as sf
from kokoro_onnx import Kokoro
from studio_runtime import find_tool

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'projects/lake-nyos/opening'
OUT=P/'audio/auditions'
OUT.mkdir(parents=True,exist_ok=True)
story=json.loads((P/'script.json').read_text(encoding='utf-8'))
lines=story['takes'][0]['lines']
text='\n\n'.join(l['spoken'] for l in lines)
(OUT/'read.txt').write_text(text+'\n',encoding='utf-8')
tts=Kokoro(str(ROOT/'models/kokoro-v1.0.onnx'),str(ROOT/'models/voices-v1.0.bin'))
voices=[('A-daniel','bm_daniel','en-gb',.85),
        ('B-michael','am_michael','en-us',.90),
        ('C-heart','af_heart','en-us',.90)]
results=[]
for label,voice,lang,speed in voices:
    wav=OUT/f'{label}.wav'
    samples,rate=tts.create(text,voice=voice,speed=speed,lang=lang,
                            continuous=True,sentence_pause=.42,clause_pause=.13)
    sf.write(str(wav),samples,rate)
    dest=OUT/f'{label}.m4a'
    subprocess.run([find_tool('ffmpeg'),'-y','-v','error','-i',str(wav),
                    '-af','loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000',
                    '-c:a','aac','-b:a','192k',str(dest)],check=True)
    results.append({'file':dest.name,'voice':voice,'language':lang,'speed':speed,
                    'seconds':round(len(samples)/rate,3),'method':'one continuous call for the complete section'})
    print(f'{label}: {len(samples)/rate:.2f}s',flush=True)
(OUT/'manifest.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
