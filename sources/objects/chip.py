from coord import Coord
import pygame as pg
from sprite import CHIP
from objects.canva import Canva
from random import choice

class Chip:
    def __init__(self, pattern, colors):
        self.colors : list = colors
        self.pattern : pg.Surface = self.pattern_init(pattern)
        self.sprite = CHIP
        self.coord = Coord(0,((0,0)))
        self.drawing = False

    def draw(self,win):
        win.blit(self.sprite,self.coord.xy)
    
    def paint(self, clic : Coord, canva : Canva):
        canva.surf.blit(self.pattern,(clic.x-600,clic.y-60))
    
    def pattern_init(self,pattern):
        color = choice(self.colors)
        new_pattern = pg.Surface(pattern.get_size())
        new_pattern.fill(color)
        pattern.set_colorkey(pg.Color(0,0,0))
        new_pattern.blit(pattern, (0,0))
        return new_pattern

