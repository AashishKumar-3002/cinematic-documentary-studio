"""Prepare the approved cold open using the cinematic-film native pipeline."""
import json
from pathlib import Path
import soundfile as sf
from kokoro_onnx import Kokoro

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'projects/lake-nyos/opening'
timing=P/'audio/timing.json'
if timing.exists() and json.loads(timing.read_text(encoding='utf-8')).get('voice')=='af_heart':
    raise SystemExit('The user selected voice C. Preserve it; use tools/select_nyos_voice.py to rebuild its timing.')
for sub in ['audio/lines', 'assets/photos', 'fonts', 'out']:
    (P/sub).mkdir(parents=True, exist_ok=True)
story = json.loads((ROOT/'projects/lake-nyos/film/script.json').read_text(encoding='utf-8'))
lines = story['takes'][0]['lines']
(P/'script.json').write_text(json.dumps({'title': story['title'], 'takes': [story['takes'][0]]}, indent=2), encoding='utf-8')
(P/'photos.json').write_text(json.dumps({'grade':'natural', 'photos':[
    {'id':'P01','what':'Lake Nyos, 1986; archival photograph, not footage of the release',
     'kind':'photo','commons':'File:Lake Nyos 1986 001.jpg'}]}, indent=2), encoding='utf-8')
segments = [{'id':l['id'],'scene':'opening','caption':l['text'],'vo':l['spoken'],
             'gap_after':0.65 if l['id'] in [4,7] else 0.38} for l in lines]
(P/'audio/segments.json').write_text(json.dumps({'segments':segments}, indent=2), encoding='utf-8')
tts = Kokoro(str(ROOT/'models/kokoro-v1.0.onnx'), str(ROOT/'models/voices-v1.0.bin'))
for s in segments:
    dest=P/'audio/lines'/f"seg{s['id']:02d}.wav"
    if dest.exists():
        print(f"cached {dest.name}", flush=True)
        continue
    samples, rate=tts.create(s['vo'],voice='bm_george',speed=0.92,lang='en-gb')
    sf.write(str(dest),samples,rate)
    print(f"{dest.name}: {len(samples)/rate:.2f}s",flush=True)
