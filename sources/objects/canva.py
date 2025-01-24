import pygame as pg
from utils.coord import Coord
from objects.placeable import Placeable

class Canva:
    def __init__(self): 
        self.coord = Coord(0,(620,28))
        self.surf = pg.Surface((680,1024))
        self.surf.fill(pg.Color(0,255,0))
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = self.coord.xy
        self.name = None
        self.pattern_num = 0

    def save(self,inv):
        inv.append(Placeable("painting",self.coord,pg.transform.scale_by(self.surf,0.5)))
        self.surf.fill(pg.Color(0,255,0))
        return self.canva.surf.copy()

