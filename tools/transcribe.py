"""CPU transcription with word timings; model files stay in this project."""
from pathlib import Path
import argparse, json, os
root = Path(__file__).resolve().parents[1]
os.environ['HF_HOME'] = str(root/'.cache/huggingface')
from faster_whisper import WhisperModel
p = argparse.ArgumentParser()
p.add_argument('audio')
p.add_argument('--model', default='tiny.en')
p.add_argument('--output', type=Path, default=root/'output/transcript.json')
a = p.parse_args()
model = WhisperModel(a.model, device='cpu', compute_type='int8', download_root=str(root/'models/whisper'))
segments, info = model.transcribe(a.audio, language='en', word_timestamps=True)
rows = []
for s in segments:
    rows.append({'start':s.start,'end':s.end,'text':s.text,'words':[{'word':w.word,'start':w.start,'end':w.end,'probability':w.probability} for w in s.words or []]})
a.output.parent.mkdir(parents=True,exist_ok=True)
a.output.write_text(json.dumps({'language':info.language,'segments':rows},indent=2),encoding='utf-8')
print(a.output)
