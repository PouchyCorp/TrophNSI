from coord import Coord
import pygame as pg
from sprite import CHIP
from objects.canva import Canva
from random import choice

class Chip:
    def __init__(self, patern, colors):
        self.colors : list = colors
        self.patern : pg.Surface = self.patern_init(patern)
        self.sprite = CHIP
        self.coord = Coord(0,((0,0)))
        self.drawing = False

    def draw(self,win):
        win.blit(self.sprite,self.coord.xy)
    
    def paint(self, clic : Coord, canva : Canva):
        canva.surf.blit(self.patern,(clic.x-600,clic.y-60))
    
    def patern_init(self,patern):
        color = choice(self.colors)
        new_patern = pg.Surface(patern.get_size())
        new_patern.fill(color)
        patern.set_colorkey(pg.Color(0,0,0))
        new_patern.blit(patern, (0,0))
        return new_patern

