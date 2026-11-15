"""A cached slate backdrop; native cinematic-film still draws camera, diagrams and finish."""
import math
from collections import OrderedDict
import numpy as np
from PIL import Image
import skia
from engine import Item

class FastBoard(Item):
    z=-100
    def __init__(self,texture='slate.png',tile=2458):
        super().__init__(-1,sfx=False)
        self.texture,self.tile=texture,tile
        self.tiles=OrderedDict()
    def draw(self,c,res,t):
        matrix=c.getTotalMatrix();scale=res.screen_scale
        pixel_tile=self.tile*scale;side=math.ceil(pixel_tile)+1
        if side not in self.tiles:
            source=res.image(self.texture,1024).toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)
            arr=np.ascontiguousarray(np.asarray(Image.fromarray(source).resize((side,side),Image.Resampling.BILINEAR)))
            self.tiles[side]=skia.Image.fromarray(arr,colorType=skia.ColorType.kRGBA_8888_ColorType,
                                               alphaType=skia.AlphaType.kOpaque_AlphaType)
            while len(self.tiles)>8:self.tiles.popitem(last=False)
        image=self.tiles[side];self.tiles.move_to_end(side)
        tx,ty=matrix.getTranslateX(),matrix.getTranslateY()
        left=math.floor(res.view.left()/self.tile)*self.tile
        top=math.floor(res.view.top()/self.tile)*self.tile
        # Fine-grain slate is resampled once per size, and translated in screen space.
        # The sub-degree handheld roll remains on foreground items and the lighting.
        c.save();c.resetMatrix()
        y=top*scale+ty
        while y<c.getBaseLayerSize().height():
            x=left*scale+tx
            while x<c.getBaseLayerSize().width():
                c.drawImage(image,round(x),round(y));x+=pixel_tile
            y+=pixel_tile
        c.restore()
