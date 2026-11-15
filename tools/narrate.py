"""Local Kokoro narration, with no paid service or user-home downloads."""
from pathlib import Path
import argparse
import soundfile as sf
from kokoro_onnx import Kokoro

root = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument('text', help='Text to speak, or a UTF-8 text file')
p.add_argument('--voice', default='af_heart')
p.add_argument('--output', type=Path, default=root/'output/narration.wav')
p.add_argument('--speed', type=float, default=0.90)
a = p.parse_args()
text = Path(a.text).read_text(encoding='utf-8') if Path(a.text).is_file() else a.text
tts = Kokoro(str(root/'models/kokoro-v1.0.onnx'), str(root/'models/voices-v1.0.bin'))
samples, rate = tts.create(text, voice=a.voice, speed=a.speed, lang='en-gb' if a.voice.startswith('b') else 'en-us',
                          continuous=True, sentence_pause=0.42, clause_pause=0.13)
a.output.parent.mkdir(parents=True, exist_ok=True)
sf.write(str(a.output), samples, rate)
print(f'{a.output}: {len(samples)/rate:.2f}s at {rate} Hz')
