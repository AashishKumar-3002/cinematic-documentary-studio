"""Full native cinematic-film composition: dated archives and schematic physics."""
import importlib.util
import json
import math
from pathlib import Path
import skia
from engine import Item, Print, BigText, paint, draw_text, text_width, ramp
from fast_board import FastBoard

WHITE=(237,239,232); TEAL=(110,205,198); MUTED=(147,166,176); AMBER=(229,183,99)

def txt(c,res,text,x,y,size=160,rgb=WHITE,a=1,maxw=3900):
    size=min(size,size*maxw/max(1,text_width(res,text,size,'cond')))
    draw_text(c,res,text,x,y,size,'cond',rgb,a,align='center')

def arrow(c,x0,y0,x1,y1,rgb=TEAL,a=1,width=12):
    c.drawLine(x0,y0,x1,y1,paint(rgb,a,stroke=width))
    ang=math.atan2(y1-y0,x1-x0)
    for d in [-.55,.55]:
        c.drawLine(x1,y1,x1-65*math.cos(ang+d),y1-65*math.sin(ang+d),paint(rgb,a,stroke=width))

class Plate(Item):
    z=7
    def __init__(self,doc,x,ids,kind,footer='SCHEMATIC / NOT TO SCALE',source=''):
        super().__init__(doc.L(ids[0])-.35,sfx=False)
        self.doc,self.x,self.ids,self.kind,self.footer,self.source=doc,x,ids,kind,footer,source
        self.lines={l['id']:l for take in json.loads((doc.dir/'script.json').read_text(encoding='utf-8'))['takes'] for l in take['lines']}
        if kind=='locator':
            data=json.loads((doc.dir/'assets/data/natural-earth-countries.geojson').read_text(encoding='utf-8'))
            self.geo=[]
            for f in data['features']:
                if f['properties'].get('CONTINENT')!='Africa':continue
                g=f['geometry'];polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
                path=skia.Path()
                for poly in polys:
                    for ring in poly:
                        for j,(lon,lat,*_) in enumerate(ring):
                            xx=(lon-17)*26;yy=-lat*26
                            if j==0:path.moveTo(xx,yy)
                            else:path.lineTo(xx,yy)
                        path.close()
                self.geo.append((f['properties']['ADMIN'],path))
    def bounds(self,res):return skia.Rect.MakeXYWH(self.x-2500,-1700,5000,3400)
    def draw(self,c,res,t):
        a=ramp(t,self.t_in,.5)
        n=max((i for i in self.ids if t>=self.doc.L(i)-.05),default=self.ids[0])
        k=self.kind
        c.save();c.translate(self.x,0)
        txt(c,res,self.lines[n]['typed'],0,-1120,250,TEAL,a)
        if k=='locator':
            for name,path in self.geo:
                c.drawPath(path,paint(TEAL if name=='Cameroon' else (44,67,78),a))
                c.drawPath(path,paint(MUTED,.35*a,stroke=2))
            xx=(10.3-17)*26;yy=-6.44*26
            c.drawCircle(xx,yy,28,paint(AMBER,a));c.drawCircle(xx,yy,55+10*math.sin(t*2),paint(AMBER,a*.5,stroke=4))
            arrow(c,xx+50,yy,920,-320,AMBER,a,5)
            txt(c,res,'NYOS',1190,-340,220,AMBER,a,maxw=800)
            txt(c,res,'NORTHWESTERN CAMEROON',1120,-100,100,MUTED,a,maxw=1450)
            txt(c,res,'AFRICA',-1200,730,210,MUTED,a,maxw=900)
        elif k in ['supply','pressure','layers','rise','feedback','pipe','reservoir']:
            self.lake(c,res,t,n,a,k)
        elif k=='bottle':
            cap_y=-790-(170*ramp(t,self.doc.L(25),.7) if 25 in self.ids else 0)
            bottle=skia.Path();bottle.moveTo(-230,-720);bottle.lineTo(230,-720);bottle.lineTo(230,-420)
            bottle.cubicTo(230,-260,650,-240,650,30);bottle.lineTo(650,800)
            bottle.quadTo(0,990,-650,800);bottle.lineTo(-650,30);bottle.cubicTo(-650,-240,-230,-260,-230,-420);bottle.close()
            c.drawPath(bottle,paint((26,64,77),a));c.drawPath(bottle,paint(TEAL,a,stroke=10))
            c.drawRect(skia.Rect.MakeXYWH(-260,cap_y,520,95),paint(AMBER,a))
            c.save();c.clipPath(bottle)
            for j in range(32):
                xx=-560+(j*317%1120);yy=-100+(j*197%950);r=9
                if n==25:yy=850-((t-self.doc.L(n))*340+j*91)%1550;r=15+(j%4)*6
                c.drawCircle(xx,yy,r,paint(TEAL,a*.75,stroke=3 if n==25 else None))
            c.restore()
            txt(c,res,'WATER',0,550,190,WHITE,a,maxw=1000)
            txt(c,res,'ANALOGY',-1450,50,200,AMBER,a,maxw=1100)
            txt(c,res,'NOT AN IDENTICAL SYSTEM',-1400,270,100,MUTED,a,maxw=1600)
        elif k=='contrast':
            for xx,lab,val in [(-1050,'ORDINARY AIR',9),(1050,'HIGH CONCENTRATION',95)]:
                c.drawRoundRect(skia.Rect.MakeXYWH(xx-800,-650,1600,1400),30,30,paint((35,55,66),a))
                for j in range(val):
                    c.drawCircle(xx-690+(j*137%1380),-520+(j*227%1050),12,paint(TEAL,a*.8))
                txt(c,res,lab,xx,940,150,WHITE,a,maxw=1750)
            txt(c,res,'ILLUSTRATIVE DENSITIES / NO THRESHOLD DEPICTED',0,-820,100,MUTED,a)
        elif k=='distance':
            arrow(c,-1800,150,1800,150,TEAL,a)
            for xx in [-1800,1800]:c.drawLine(xx,40,xx,270,paint(AMBER,a,stroke=10))
            txt(c,res,'UP TO 25 KM',0,-150,510,AMBER,a)
            txt(c,res,'REPORTED DEADLY EFFECTS',0,590,190,WHITE,a)
            txt(c,res,'EXTENT REPORTED BY NASA / NOT A PRECISE BOUNDARY',0,940,105,MUTED,a)
        elif k=='impact':
            txt(c,res,'MORE THAN 1,700 LIVES',0,60,410,WHITE,a)
            txt(c,res,'COMMUNITIES BEYOND THE SHORE',0,550,200,MUTED,a)
            for xx in [-700,0,700]:
                c.drawCircle(xx,-470,75,paint(TEAL,a*.7,stroke=6))
                c.drawLine(xx,-350,xx,-200,paint(TEAL,a*.7,stroke=6))
        elif k in ['evidence','measure']:
            labels=['WATER','GAS','GEOLOGY'] if k=='evidence' else ['MEASURE','CHECK','MONITOR']
            for j,lab in enumerate(labels):
                xx=(j-1)*1270
                c.drawRoundRect(skia.Rect.MakeXYWH(xx-530,-600,1060,1300),45,45,paint((35,55,66),a))
                if j==0:
                    c.drawRoundRect(skia.Rect.MakeXYWH(xx-130,-380,260,460),30,30,paint(TEAL,a,stroke=8))
                    c.drawLine(xx-120,-80,xx+120,-80,paint(TEAL,a,stroke=30))
                elif j==1:
                    for dx,dy in [(-110,-180),(110,-180),(0,20)]:c.drawCircle(xx+dx,dy,55,paint(TEAL,a,stroke=7))
                else:
                    for yy in range(-300,170,130):c.drawLine(xx-230,yy,xx+230,yy+80,paint(TEAL,a,stroke=8))
                txt(c,res,lab,xx,510,190,WHITE,a,maxw=1000)
            txt(c,res,'SCIENTIFIC FINDINGS / SEE SOURCE NOTES',0,970,110,MUTED,a)
        elif k=='trigger':
            txt(c,res,'?',0,390,1250,AMBER,a)
            txt(c,res,'THE SOURCE IS IDENTIFIED',0,740,180,WHITE,a)
            txt(c,res,'THE PRECISE TRIGGER IS NOT ESTABLISHED',0,1040,155,MUTED,a)
        elif k=='known':
            for xx,head,rows,col in [(-1100,'SUPPORTED',['CO2 RESERVOIR','GAS RELEASE'],TEAL),
                                     (1100,'UNCERTAIN',['THE FIRST DISTURBANCE','THE EXACT SEQUENCE'],AMBER)]:
                txt(c,res,head,xx,-470,270,col,a,maxw=1900)
                for j,row in enumerate(rows):txt(c,res,row,xx,100+j*420,160,WHITE,a,maxw=1950)
            c.drawLine(0,-740,0,850,paint(MUTED,a*.4,stroke=3))
        elif k=='question':
            txt(c,res,'HOW DO YOU REMOVE',0,-310,380,WHITE,a)
            txt(c,res,'A HIDDEN HAZARD?',0,260,470,TEAL,a)
            arrow(c,-1000,730,1000,730,TEAL,a)
        elif k=='term':
            txt(c,res,'LIMNIC',0,-40,670,WHITE,a)
            txt(c,res,'ERUPTION',0,670,670,TEAL,a)
            txt(c,res,'A RELEASE OF STORED LAKE GAS',0,1040,140,MUTED,a)
        elif k=='summary':
            for j,lab in enumerate(['SUPPLY','STORAGE','RELEASE','TERRAIN']):
                xx=-1500+j*1000
                c.drawCircle(xx,30,290,paint((32,61,73),a))
                txt(c,res,str(j+1),xx,180,430,TEAL,a,maxw=500)
                txt(c,res,lab,xx,690,155,WHITE,a,maxw=900)
                if j<3:arrow(c,xx+340,30,xx+650,30,TEAL,a,8)
        if self.footer:txt(c,res,self.footer,0,1360,100,MUTED,a,maxw=4300)
        if self.source:txt(c,res,self.source,0,1550,90,MUTED,a*.8,maxw=4400)
        c.restore()

    def lake(self,c,res,t,n,a,k):
        basin=skia.Path();basin.moveTo(-1740,-600);basin.cubicTo(-1350,-100,-1450,870,0,920)
        basin.cubicTo(1450,870,1350,-100,1740,-600);basin.close()
        c.drawPath(basin,paint((28,65,82),a))
        c.drawLine(-1800,-600,1800,-600,paint(TEAL,a,stroke=9))
        txt(c,res,'SURFACE',-1330,-700,110,MUTED,a,maxw=900)
        c.save();c.clipPath(basin)
        for yy in range(-420,950,160):c.drawLine(-1800,yy,1800,yy,paint(TEAL,a*.13,stroke=3))
        for j in range(90 if n>=18 else 48):
            c.drawCircle(-1550+(j*433%3100),50+(j*173%780),8,paint(TEAL,a*.55))
        if k=='layers':
            c.drawRect(skia.Rect.MakeXYWH(-1800,-590,3600,520),paint(TEAL,a*.12))
            c.drawLine(-1800,-70,1800,-70,paint(AMBER,a*.6,stroke=4))
            for xx in [-1000,-400,200,800]:
                shift=math.sin(t+xx)*60
                arrow(c,xx-160+shift,-320,xx+160+shift,-320,TEAL,a*.8,8)
        if k in ['rise','feedback','pipe']:
            c.drawRect(skia.Rect.MakeXYWH(-1800 if k=='rise' else -180,-600,360 if k!='rise' else 3600,1530),paint(TEAL,a*.06))
            for j in range(14 if k!='rise' or n>=24 else 0):
                u=((t-self.t_in)*.23+j/14)%1
                c.drawCircle(math.sin(j*5)*90,830-u*1550,9+u*34,paint(TEAL,a*.8,stroke=4))
            if k=='rise' and n<24:
                yy=550-ramp(t,self.doc.L(self.ids[0]),max(.1,self.doc.E(23)-self.doc.L(22)))*800
                c.drawRoundRect(skia.Rect.MakeXYWH(-250,yy-100,500,200),20,20,paint(AMBER,a,stroke=8))
            for yy in [-200,250,650]:arrow(c,450,yy+90,450,yy-90,TEAL,a*.7,8)
        c.restore()
        if k=='pipe':
            for xx in [-200,200]:c.drawLine(xx,850,xx,-730,paint(WHITE,a,stroke=13))
            c.drawLine(-200,850,200,850,paint(WHITE,a,stroke=13))
            for j in range(9):
                u=((t-self.t_in)*.45+j/9)%1
                c.drawCircle((j-4)*55*u,-760-300*math.sin(u*3.14),9,paint(TEAL,a*.7))
            txt(c,res,'CONTROLLED PATH',1100,150,155,WHITE,a,maxw=1300)
            txt(c,res,'DEEP INTAKE',-1050,800,145,WHITE,a,maxw=1400)
        elif k=='pressure':
            for j,xx in enumerate([-1050,0,1050]):arrow(c,xx,-400,xx,220+j*160,AMBER,a,15)
            txt(c,res,'GREATER DEPTH / GREATER PRESSURE',0,1140,140,WHITE,a)
        elif k=='supply':
            for xx in [-750,750]:arrow(c,xx,1250,xx,850,AMBER,a,12)
            txt(c,res,'GAS-BEARING GROUNDWATER',0,1140,155,WHITE,a)
        elif k=='layers':
            txt(c,res,'UPPER WATER',0,-220,145,WHITE,a)
            txt(c,res,'ISOLATED DEEP WATER',0,560,180,TEAL,a)
        elif k=='feedback':
            txt(c,res,'RISE',-1250,0,180,WHITE,a,maxw=900)
            txt(c,res,'EXPAND',1250,0,180,WHITE,a,maxw=1000)
            arrow(c,-900,-250,900,-250,AMBER,a,10);arrow(c,900,450,-900,450,AMBER,a,10)
            txt(c,res,'LOWER PRESSURE / MORE GAS',0,1140,140,WHITE,a)
        else:txt(c,res,'DISSOLVED CO2 RESERVOIR',0,1150,155,TEAL,a)

def build_film(doc):
    spec=importlib.util.spec_from_file_location('approved_nyos_opening',doc.dir.parent/'opening/scene.py')
    opening=importlib.util.module_from_spec(spec);spec.loader.exec_module(opening)
    class OpeningDoc:
        duration=doc.timing['chapters'][1]['start'] if len(doc.timing.get('chapters',[]))>1 else doc.E(8)+1.5
        def __getattr__(self,name):return getattr(doc,name)
    film=opening.build_film(OpeningDoc());film.duration=doc.duration;film.auto_whoosh=False
    # The isolated heroes already fill the frame. Broad light changes no foreground
    # pixels in the 68-beat comparison (at most one channel level in dark corners).
    film.look['skip_broad_spotlight']=True
    old_board=film.board
    film.board=FastBoard()
    film.items=[film.board if it is old_board else it for it in film.items]
    L,E=doc.L,doc.E
    def label(text,x,y,size,t,rgb=WHITE,t_out=None):
        film.add(BigText(text,x,y,size,t,rgb=rgb,grunge=False,shadow=False,track=.015,type_on=.3,sfx=False,t_out=t_out))
    def move(ids,x,zoom=.63,y=0):
        first=ids[0]
        film.shot(L(first)+.55,x,y,zoom,radius=4500,strength=.12)
        for n in ids:film.shot(E(n)-.12,x+(n-first)*15,y+10,zoom+.008*((n-first)%3),radius=4500,strength=.12)
    def plate(ids,x,kind,source='',footer='SCHEMATIC / NOT TO SCALE',zoom=.63):
        film.add(Plate(doc,x,ids,kind,footer,source));move(ids,x,zoom)
    def photo(ids,x,key,title,credit,w=3200):
        film.add(Print(key,x,-60,w,t_in=L(ids[0])-.25,border=.008,pin=False,sfx=False))
        label(title,x,-1370,185,L(ids[0]),TEAL);label(credit,x,1460,110,L(ids[0]),MUTED);move(ids,x,.60)
    plate([9],36000,'locator','MAP: NATURAL EARTH / PUBLIC DOMAIN','GEOGRAPHIC LOCATOR')
    photo([10],41200,'P03','LAKE NYOS / LANDSAT / 5 FEBRUARY 2001','NASA / GODDARD SCIENTIFIC VISUALIZATION STUDIO')
    plate([11,12],46400,'supply','NASA SCIENCE / ZHANG, NATURE 1996')
    plate([13,14],51600,'bottle','PRESSURE ANALOGY / ZHANG 1996')
    plate([15],56800,'pressure','ZHANG, NATURE 1996')
    plate([16,17,18],62000,'layers','KLING, EVANS & TANYILEKE 2015')
    plate([19,20],67200,'supply','KLING, EVANS & TANYILEKE 2015')
    photo([21],72400,'P03','THE SURFACE HID A RESERVOIR','LANDSAT: 2001-02-05 / NASA GODDARD SVS')
    plate([22,23,24],77600,'rise','ZHANG 1996 / CHAN, KWOK & MAK 1996')
    plate([25],82800,'bottle','PRESSURE ANALOGY / ZHANG 1996')
    plate([26,27,28,29,30],88000,'feedback','CHAN, KWOK & MAK 1996')
    plate([31,32],93200,'term','SCIENTIFIC TERM / NOT A LAVA FLOW','EXPLANATORY DIAGRAM')
    plate([33],98400,'evidence','KLING ET AL., SCIENCE 1987','ILLUSTRATIVE SCIENCE ICONS')
    plate([34],103600,'reservoir','KLING ET AL., SCIENCE 1987')
    film.add(opening.Terrain(108800,L(35)-.3,L(36)))
    for n in [35,36,37,38]:
        label({35:'ABOVE THE WATER',36:'DENSER THAN AIR',37:'DOWNHILL',38:'TERRAIN GUIDES THE FLOW'}[n],108800,-860,240,L(n),TEAL,t_out=L(n+1)-.35)
    move([35,36,37,38],108800,.72)
    plate([39],114000,'contrast','IPCC / CO2 STORAGE REPORT, CHAPTER 6','ILLUSTRATIVE CONCENTRATIONS')
    plate([40,41],119200,'impact','KLING ET AL. 1987 / NASA SVS','SYMBOLIC COMMUNITY MARKERS')
    plate([42,43],124400,'distance','NASA SVS, LAKE NYOS ZOOM-IN (2002)','REPORTED EXTENT / NOT TO SCALE')
    film.add(opening.Terrain(129600,L(44)-.3,L(44)-3));label('THE GAS ITSELF WAS INVISIBLE',129600,-860,240,L(44),TEAL);move([44],129600,.72)
    plate([45,46,47],134800,'evidence','KLING ET AL., SCIENCE 1987','ILLUSTRATIVE SCIENCE ICONS')
    plate([48,49,50],140000,'trigger','KLING ET AL. 1987 / COTEL 1999','HYPOTHESES ARE NOT A WITNESSED RECONSTRUCTION')
    plate([51,52,53],145200,'known','RESEARCH EVIDENCE / TRIGGER UNCERTAINTY','NO SPECIFIC TRIGGER DEPICTED AS FACT')
    plate([54],150400,'question','KLING ET AL., PNAS 2005','FROM INVESTIGATION TO ENGINEERING')
    photo([55],155600,'P02','CONTROLLED DEGASSING / 2001','BILL EVANS / USGS / HISTORICAL PHOTOGRAPH',3000)
    plate([56,57,58,59,60],160800,'pipe','KLING ET AL., PNAS 2005')
    plate([61,62],166000,'measure','KLING ET AL. 2005 / COMPARATIVE LIMNOLOGY 2015','MEASURED RESULTS / DATED STUDIES')
    plate([63],171200,'supply','CONTINUING GAS INPUT / KLING ET AL. 2005')
    plate([64],176400,'measure','HISTORICAL RESEARCH / NO CURRENT SAFETY ASSESSMENT','HISTORICAL ACCOUNT')
    photo([65],181600,'P01','THE ANSWER WAS IN THE WATER','JACK LOCKWOOD / USGS / 1986')
    plate([66,67],186800,'summary','SEE THE SOURCE NOTES ACCOMPANYING THIS FILM','CONCEPTUAL PROCESS / NOT TO SCALE')
    photo([68],192000,'P01','LAKE NYOS','REMEMBERING THOSE LOST / 21 AUGUST 1986')
    end=E(68);cx=197200
    label('THE LAKE THAT EXHALED',cx,-850,340,end+.1,TEAL)
    for text,yy in [('Research: NASA / USGS / cited scientific papers',-230),
                    ('Archive: Jack Lockwood / Bill Evans / NASA Goddard SVS',100),
                    ('Map: Natural Earth / Voice: Kokoro Heart',430),
                    ('Diagrams, animation and sound: created in code',760),
                    ('Full sources and image credits accompany this film',1120)]:label(text,cx,yy,135,end+.1,MUTED)
    film.shot(end+1,cx,80,.63,radius=4500,strength=.08);film.shot(doc.duration,cx+30,80,.63,radius=4500,strength=.08)
    for n in [9,22,35,45,55]:film.cue('whoosh',max(0,L(n)-.25),.16,dur=.7)
    film.cue('boom',L(7)+.4,.12)
    return film
