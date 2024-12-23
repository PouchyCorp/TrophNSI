import pygame as pg
from utils.coord import Coord
from placeable import Placeable

class Canva:
    def __init__(self):
        self.coord = Coord(0,(600,60))
        self.surf = pg.Surface((600,900))
        self.surf.fill(pg.Color(0,255,0))
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = self.coord.xy
        self.name = None

    def draw(self,win):
        win.blit(self.surf,self.coord.xy)

    def save(self, name, inv):
        self.name = name
        self.surf.blit(self.surf.copy(),(0,0))
        inv.append(Placeable(self.name,self.coord,pg.transform.scale(self.surf.copy(),(300,450)),'decoration'))

