"""Create local, reviewable release metadata and original thumbnail designs. Never uploads."""
import json
import shutil
import textwrap
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageEnhance

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'projects/lake-nyos/film'
R=P/'release';R.mkdir(exist_ok=True)
timing=json.loads((P/'audio/timing.json').read_text())
sources=json.loads((P/'sources.json').read_text())
names=['The invisible disaster','A reservoir beneath the water','When pressure falls',
       'A cloud follows the land','What the evidence tells us','Letting the lake breathe']
def clock(sec):
    s=int(sec);return f'{s//60:02d}:{s%60:02d}'
chapter_rows=[f"{'00:00' if i==0 else clock(c['start'])} {name}" for i,(c,name) in enumerate(zip(timing['chapters'],names))]
description='''On 21 August 1986, Lake Nyos in Cameroon released carbon dioxide, killing more than 1,700 people. How could a lake make the surrounding air deadly?

This animated documentary follows the hidden gas reservoir, the physics of a limnic eruption, the role of the landscape, and the controlled degassing response. It separates the known mechanism from uncertainty about the precise trigger.

CHAPTERS
'''+ '\n'.join(chapter_rows)+'''

SOURCES
'''+ '\n'.join(s['title']+'\n'+s['url'] for s in sources.values())+'''

IMAGE AND MAP CREDITS
Lake Nyos, 1986: Jack Lockwood / USGS, public domain, via Wikimedia Commons.
Degassing installation, 2001: Bill Evans / USGS, public domain, via Wikimedia Commons.
Landsat-7 imagery, 5 February 2001: NASA/Goddard Space Flight Center Scientific Visualization Studio, https://svs.gsfc.nasa.gov/2348/
Geographic locator: Natural Earth, public-domain boundary data.

PRODUCTION NOTES
Narration is synthesized with Kokoro Heart. Diagrams, animation and transition sounds are created in code. Gas shading makes an invisible process understandable; it is not footage of a visible cloud. The bottle is a pressure analogy, and diagrams are not to scale. This film describes historical research and engineering, not the lake's current safety status.

#LakeNyos #Documentary #Science
'''
assert len(description)<=5000,len(description)
(R/'description.txt').write_text(description,encoding='utf-8')
(R/'chapters.txt').write_text('\n'.join(chapter_rows)+'\n',encoding='utf-8')
metadata={'title':'How Can a Lake Kill Without Flooding? | Lake Nyos',
          'description':description,'tags':['Lake Nyos','limnic eruption','animated documentary','Cameroon','carbon dioxide','science documentary'],
          'categoryId':'27','madeForKids':False,'containsSyntheticMedia':True}
(R/'upload.json').write_text(json.dumps(metadata,indent=2,ensure_ascii=False),encoding='utf-8')
(R/'release-record.json').write_text(json.dumps({'status':'local preparation; not uploaded','video':'../out/lake-nyos-full-v1-1080p.mp4',
    'captions':'captions.en.srt','thumbnail_options':['thumbnail-A.jpg','thumbnail-B.jpg'],
    'expected_channel':None,'visibility':'private until explicitly changed','timezone':'Asia/Calcutta',
    'language':'en','duration_seconds':timing['total_duration'],'narrator':'Kokoro af_heart',
    'disclosure_rationale':'Draft yes: human-like synthesized narration. Diagrams are labelled schematics and no real person is impersonated. Review the actual AI-use question at upload.',
    'video_id':None},indent=2),encoding='utf-8')
shutil.copy2(P/'out/captions.srt',R/'captions.en.srt')
shutil.copy2(P/'credits.md',R/'image-credits.md')
shutil.copy2(P/'sources.json',R/'sources.json')
(R/'source-notes.md').write_text('# Research and evidence notes\n\n'+ '\n\n'.join(f"## {key}: {s['title']}\n\n{s['supports']}\n\n{s['url']}" for key,s in sources.items())+
    '\n\nMap boundaries: Natural Earth, https://www.naturalearthdata.com/about/terms-of-use/ . The locator is not a hazard boundary.\n',encoding='utf-8')

font_path=Path('C:/Windows/Fonts/impact.ttf')
small_path=Path('C:/Windows/Fonts/arialbd.ttf')
def font(size,small=False):
    candidates=[small_path if small else font_path,
        P/'fonts'/('label.ttf' if small else 'cond.ttf'),
        Path('/System/Library/Fonts/Supplemental/Arial Bold.ttf' if small else '/System/Library/Fonts/Supplemental/Impact.ttf'),
        Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'),
        Path('/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf')]
    for candidate in candidates:
        if candidate.is_file():return ImageFont.truetype(str(candidate),size)
    return ImageFont.load_default(size=size)
photo=Image.open(P/'assets/photos/P01_Lake_Nyos_1986_001.jpg').convert('RGB')
for variant in ['A','B']:
    im=Image.new('RGB',(1280,720),(10,20,27))
    h=720;w=round(photo.width*h/photo.height)
    scaled=ImageEnhance.Color(photo.resize((w,h),Image.Resampling.LANCZOS)).enhance(.72)
    im.paste(scaled,(-145,0))
    overlay=Image.new('RGBA',im.size,(0,0,0,0));d=ImageDraw.Draw(overlay)
    # A designed dark panel, without fabricating gas in the archival image.
    for x in range(490,1280):
        alpha=round(240*min(1,(x-490)/270))
        d.line((x,0,x,720),fill=(8,18,25,alpha))
    im=Image.alpha_composite(im.convert('RGBA'),overlay);d=ImageDraw.Draw(im)
    d.rounded_rectangle((42,38,307,95),radius=7,fill=(9,29,36,240))
    d.text((60,46),'LAKE NYOS',font=font(39),fill=(117,221,209))
    words=['DEADLY','AIR'] if variant=='A' else ['HIDDEN','BELOW']
    sizes=[138,178] if variant=='A' else [127,127]
    ys=[205,375] if variant=='A' else [230,390]
    for word,size,y in zip(words,sizes,ys):
        while size>40 and d.textbbox((0,0),word,font=font(size))[2]>480:size-=2
        f=font(size);box=d.textbbox((0,0),word,font=f);tw=box[2]-box[0]
        d.text((1000-tw/2,y),word,font=f,fill=(244,239,224) if y==ys[0] else (117,221,209),stroke_width=2,stroke_fill=(8,18,25))
    d.text((48,652),'CAMEROON / 1986',font=font(28,True),fill=(244,239,224))
    im.convert('RGB').save(R/f'thumbnail-{variant}.jpg',quality=95)
shutil.copy2(R/'thumbnail-A.jpg',R/'thumbnail.jpg')
record=json.loads((R/'release-record.json').read_text())
record['selected_thumbnail']='thumbnail.jpg'
record['thumbnail_choice']='A / Deadly Air; user delegated the choice; chosen for a clear link between lake and gas hazard, not a promised performance result'
(R/'release-record.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
(R/'README.md').write_text('''# Lake Nyos release package

Full local video: `../out/lake-nyos-full-v1-1080p.mp4`.

`upload.json` is a prepared metadata draft, not a publishing instruction. `description.txt` contains chapters, sources and credits. Upload `captions.en.srt` as an English caption track alongside the clean video. Two original thumbnails use the credited archival lake image; neither depicts invented event footage.

General-audience science documentary; drafted as not made for children. Synthetic narration is disclosed in the description, and the metadata AI-use flag is drafted as yes because this film uses human-like synthesized narration. This is an editorial disclosure choice; check the actual upload question. Current platform reference: https://support.google.com/youtube/answer/14328491 .

No Google account is connected and no video has been uploaded. After the complete film and thumbnail have been reviewed, connect the intended channel, verify its channel ID, and perform a private upload first. Keep account credentials outside this package.

Review remaining before publication: listen to the complete film (including the pronunciation of Nyos and limnic), choose a thumbnail, confirm the channel and publishing settings. Automated speech matching is a coverage check, not a substitute for a listening pass.
''',encoding='utf-8')
print(f'Release package: {R}; description {len(description)} characters; 2 thumbnails; {len(chapter_rows)} chapters')
