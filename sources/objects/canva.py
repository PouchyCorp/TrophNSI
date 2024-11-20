
import pygame as pg
from coord import Coord

class Canva:
    def __init__(self):
        self.coord = Coord(666,(600,60))
        self.surf = pg.Surface((600,900))
        self.surf.fill(pg.Color(255,255,255))
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = self.coord.xy
        self.name = None

    def draw(self,win):
        win.blit(self.surf,self.coord.xy)

    def save(self, name):
        self.name = name


