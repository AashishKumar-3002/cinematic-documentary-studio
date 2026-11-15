"""Lake Nyos opening: archival evidence and explicitly schematic physical explanation.

Rendered by the primary cinematic-film Skia engine, one camera over one world.
"""
import math
import re
import skia
from engine import Film, Print, BigText, Item, paint, draw_text, ramp

WHITE=(237,239,232)
TEAL=(110,205,198)
MUTED=(147,166,176)
AMBER=(229,183,99)


class Terrain(Item):
    """Schematic valley cross section: deliberately no claimed real village geometry."""
    z=3
    def __init__(self,x,t_in,gas_at):
        super().__init__(t_in,sfx=False)
        self.x=x; self.gas_at=gas_at
    def bounds(self,res):
        return skia.Rect.MakeXYWH(self.x-2200,-1050,4400,2150)
    def draw(self,c,res,t):
        a=ramp(t,self.t_in,.6)
        c.save(); c.translate(self.x,0)
        for offset in range(0,650,110):
            path=skia.Path(); path.moveTo(-2150,-700+offset)
            path.cubicTo(-1200,-650+offset,-1350,460+offset,-400,400+offset)
            path.cubicTo(400,350+offset,800,250+offset,2150,530+offset)
            c.drawPath(path,paint((70,99,111),a*.4,stroke=3))
        ground=skia.Path(); ground.moveTo(-2150,-710)
        ground.cubicTo(-1200,-660,-1350,450,-400,400)
        ground.cubicTo(400,350,800,250,2150,530)
        ground.lineTo(2150,1000);ground.lineTo(-2150,1000);ground.close()
        c.drawPath(ground,paint((29,48,58),a))
        # Water at the schematic crater's upper left, not a geographic map.
        c.drawLine(-2000,-660,-1400,-660,paint(TEAL,a,stroke=15))
        g=ramp(t,self.gas_at,2.2)
        if g>0:
            cloud=skia.Path(); cloud.moveTo(-1500,-590)
            cloud.cubicTo(-1100,-400,-1100,170,-450,200)
            cloud.cubicTo(300,160,1000,160,2000,330)
            cloud.lineTo(2000,505)
            cloud.cubicTo(800,240,400,340,-400,390)
            cloud.cubicTo(-1200,400,-1200,-400,-1500,-590); cloud.close()
            c.save(); c.clipRect(skia.Rect.MakeLTRB(-1700,-900,-1700+g*3900,900))
            c.drawPath(cloud,paint(TEAL,.28*a)); c.restore()
            for j in range(14):
                u=((t-self.gas_at)*.1+j/14)%1
                xx=-1300+u*3200; yy=210+80*math.sin(u*3.14)
                c.drawCircle(xx,yy,6,paint(TEAL,g*a*.65))
        for xx,yy in [(550,335),(930,360),(1310,410)]:
            c.drawRect(skia.Rect.MakeXYWH(xx,yy-85,90,85),paint(MUTED,a*.6,stroke=4))
            roof=skia.Path();roof.moveTo(xx-12,yy-85);roof.lineTo(xx+45,yy-130);roof.lineTo(xx+102,yy-85)
            c.drawPath(roof,paint(MUTED,a*.6,stroke=4))
        draw_text(c,res,'SCHEMATIC / NOT TO SCALE',-1950,900,100,'labelm',MUTED,a)
        c.restore()


class Reservoir(Item):
    z=4
    def __init__(self,x,t_in):
        super().__init__(t_in,sfx=False);self.x=x
    def bounds(self,res):
        return skia.Rect.MakeXYWH(self.x-2100,-1100,4200,2250)
    def draw(self,c,res,t):
        a=ramp(t,self.t_in,.8);c.save();c.translate(self.x,0)
        basin=skia.Path();basin.moveTo(-1750,-550);basin.cubicTo(-1300,-100,-1400,800,0,850)
        basin.cubicTo(1400,800,1300,-100,1750,-550);basin.close()
        c.drawPath(basin,paint((23,67,83),a))
        c.save();c.clipPath(basin)
        for y in range(-400,1000,140):
            c.drawLine(-1800,y,1800,y,paint(TEAL,a*.14,stroke=3))
        # Sparse molecular markers denote dissolved gas, not a giant gas bubble.
        for j in range(50):
            xx=-1550+(j*431%3100); yy=70+(j*173%700)
            rr=9+4*math.sin(j*2+t*.5)
            c.drawCircle(xx,yy,rr,paint(TEAL,a*.5))
        c.restore()
        c.drawLine(-1800,-550,1800,-550,paint(TEAL,a,stroke=10))
        draw_text(c,res,'SURFACE',-1750,-640,110,'labelm',MUTED,a)
        draw_text(c,res,'DISSOLVED GAS',0,350,210,'cond',TEAL,a,align='center')
        draw_text(c,res,'SCHEMATIC / NOT TO SCALE',-1750,1120,100,'labelm',MUTED,a)
        c.restore()


def build_film(doc):
    L,E=doc.L,doc.E
    def W(i,word):
        # ASR is approximate, but better than proportional letter timing for emphasis.
        aliases={'seventeen':'1700'}
        target=aliases.get(word,word)
        for entry in doc.seg[i].get('words',[]):
            if re.sub(r'[^a-z0-9]','',entry['word'].lower())==target:
                return entry['start']
        return doc.W(i,word)
    film=Film(doc.duration,fps=30,look='slate')
    film.look.update(grain=.012,glow=.08,vignette=.38,curve=.15)
    def label(text,x,y,size,t,rgb=WHITE,**kw):
        return film.add(BigText(text,x,y,size,t,rgb=rgb,grunge=False,shadow=False,
                                track=.025,type_on=.25,sfx=False,**kw))
    film.add(Print('P01',0,-30,3200,t_in=0,border=.008,pin=False,sfx=False))
    label('CAMEROON / 1986',0,-1190,190,.15,TEAL)
    label('LAKE NYOS',0,1350,260,L(1))
    label('ARCHIVE: JACK LOCKWOOD / USGS',0,1570,105,L(1),MUTED)
    film.add(Terrain(5300,L(2)-.25,W(3,'travelled')-.2))
    label('BEYOND THE SHORE',5300,-860,260,L(2),TEAL,t_out=L(3)-.2)
    label('AN INVISIBLE HAZARD',5300,-860,260,L(3),TEAL)
    label('ILLUSTRATIVE RECONSTRUCTION',5300,-600,105,L(3),MUTED)
    label('MORE THAN',10500,-950,180,L(4),MUTED)
    label('1,700',10500,170,980,W(4,'seventeen')-.15,AMBER)
    label('LIVES LOST',10500,640,270,L(4)+.7)
    label('21 AUGUST 1986',10500,1030,140,L(4),MUTED)
    # A restrained word panel before the physical explanation.
    label('THE KILLER WAS A GAS',15100,-780,320,L(5))
    label('NOT FLOODWATER',15100,-260,190,W(5,'floodwater')-.1,MUTED)
    label('NOT FIRE',15100,160,190,W(5,'fire')-.1,MUTED)
    label('NOT A LAVA FLOW',15100,580,190,W(5,'lava')-.1,MUTED)
    film.add(Reservoir(20000,L(6)-.3))
    label('CO2',20000,-810,300,W(6,'carbon')-.15,TEAL)
    label('THE LAKE',25400,-250,690,L(7))
    label('THAT EXHALED',25400,500,690,L(7)+.4,TEAL)
    label('A LAKE NYOS DOCUMENTARY',25400,1060,140,L(7)+.6,MUTED)
    film.add(Reservoir(30800,L(8)-.2))
    label('BELOW THE SURFACE',30800,-870,230,L(8),TEAL)
    shots=[(1,0,0,.64),(2,5300,-30,.73),(3,5350,50,.73),(4,10500,0,.76),
           (5,15100,-50,.82),(6,20000,0,.72),(7,25400,100,.70),(8,30800,80,.72)]
    film.shot(0,0,0,.62,radius=4500,strength=.08)
    for n,x,y,z in shots:
        # Hold near each hero; travel only through the preceding inter-line pause.
        if n>1:
            film.shot(L(n)+.45,x,y,z,radius=3900,strength=.12)
        film.shot(E(n)-.12,x+55,y+20,z+.018,radius=3900,strength=.12)
    film.shot(doc.duration,30860,160,.74,radius=3900,strength=.12)
    return film
