"""Review every beat and every major camera move before the full render."""
import json
import math
import sys
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.agents/skills/cinematic-film/scripts'))
from render import make
P=ROOT/'projects/lake-nyos/film'
OUT=P/'out/review';OUT.mkdir(parents=True,exist_ok=True)
film,r,doc=make(P,'1280x720')
segments=list(doc.seg.values())
for page in range(math.ceil(len(segments)/16)):
    sheet=Image.new('RGB',(1280,4*205),(12,18,24));d=ImageDraw.Draw(sheet)
    for j,s in enumerate(segments[page*16:(page+1)*16]):
        t=s['start']+(s['end']-s['start'])*.72
        im=Image.fromarray(r.frame(round(t*film.fps)))
        im.save(OUT/f"line{s['id']:02d}.jpg",quality=92)
        x,y=(j%4)*320,(j//4)*205
        sheet.paste(im.resize((320,180)),(x,y));d.text((x+8,y+183),f"Line {s['id']} / {t:.2f}s",fill='white')
    sheet.save(OUT/f'beats-{page+1}.jpg',quality=94)
    print(f'beat sheet {page+1}',flush=True)
film,r,doc=make(P,'640x360')
keys=sorted(film.cam_keys)
moves=[(a[0],b[0]) for a,b in zip(keys,keys[1:]) if math.hypot(a[1]-b[1],a[2]-b[2])>1500]
for page in range(math.ceil(len(moves)/6)):
    sheet=Image.new('RGB',(1600,6*205),(12,18,24));d=ImageDraw.Draw(sheet)
    for row,(t0,t1) in enumerate(moves[page*6:(page+1)*6]):
        for j in range(5):
            t=t0+(t1-t0)*j/4
            im=Image.fromarray(r.frame(round(t*film.fps)))
            sheet.paste(im.resize((320,180)),(j*320,row*205));d.text((j*320+8,row*205+183),f'{t:.2f}s',fill='white')
    sheet.save(OUT/f'moves-{page+1}.jpg',quality=92)
    print(f'move sheet {page+1}',flush=True)
print(f'{len(segments)} beats and {len(moves)} major camera moves ready',flush=True)
