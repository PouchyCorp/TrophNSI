from coord import Coord
import pygame as pg
from sprite import CHIP

class Chip:
    def __init__(self, patern, color, coord, surface,start):
        self.patern : list = patern
        self.color : list = color
        self.coord : Coord = coord
        self.start : Coord = start
        self.surface : pg.Surface = surface 
        self.rect : pg.Rect = self.surf.get_rect()
        self.sprite = CHIP
