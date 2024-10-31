from coord import Coord
import pygame as pg
from sprite import CHIP
from canva import Painting

class Chip:
    def __init__(self, patern, coord,):
        self.patern : list = patern
        self.coord : Coord = coord
        self.sprite = CHIP

    def draw(self,win):
        win.blit(self.sprite,self.coord.xy)
    
    def paint(self, clic : Coord, canva : Painting,win,room):
        drawing = True
        for y, line in enumerate(canva.pixels):
            for x, row in enumerate(line):
                self.coord.xy = (x-2,y-3)
                if y == 2 or x == 3:
                    drawing = False
                if drawing and self.patern[y][x] != "":
                    canva.pixels[y][x] = self.patern[y][x]
        canva.draw(win)
        self.draw(win)

