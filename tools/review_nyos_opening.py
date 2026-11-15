"""Render a frame for each narration line and strips across all inter-cluster moves."""
import sys
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.agents/skills/cinematic-film/scripts'))
from render import make
P=ROOT/'projects/lake-nyos/opening'
film,r,_=make(P,'1280x720')
timed=list(__import__('json').loads((P/'audio/timing.json').read_text())['segments'])
ts=[s['start']+(s['end']-s['start'])*.76 for s in timed]
sheet=Image.new('RGB',(1280,1552),(12,18,24))
d=ImageDraw.Draw(sheet)
for i,t in enumerate(ts):
    im=Image.fromarray(r.frame(round(t*film.fps)))
    im.save(P/'out/probe'/f't{t:07.2f}.png')
    x,y=(i%2)*640,(i//2)*388
    sheet.paste(im.resize((640,360)),(x,y));d.text((x+16,y+365),f'{t:.2f}s',fill='white')
sheet.save(P/'out/look-review.jpg',quality=94)
film,r,doc=make(P,'640x360')
strips=Image.new('RGB',(1920,6*205),(12,18,24));d=ImageDraw.Draw(strips)
for row,n in enumerate([2,4,5,6,7,8]):
    t0,t1=doc.E(n-1)-.1,doc.L(n)+.65
    for j in range(6):
        t=t0+(t1-t0)*j/5
        im=Image.fromarray(r.frame(round(t*film.fps))).resize((320,180))
        strips.paste(im,(j*320,row*205));d.text((j*320+10,row*205+183),f'{t:.2f}s',fill='white')
    print(f'reviewed move to line {n}',flush=True)
strips.save(P/'out/camera-review.jpg',quality=92)
print('look-review.jpg and camera-review.jpg ready',flush=True)
