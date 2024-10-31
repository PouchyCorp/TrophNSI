
import pygame as pg
from coord import Coord

class Painting:
    def __init__(self):
        self.coord = Coord(666,(100,10))
        self.pixels = [["#FFFFFF" for col in range(48)] for row in range(64)]
        self.name = None

    def draw(self,win):
        for y,line in enumerate(self.pixels):
            for x,row in enumerate(line):
                if True:
                    surf = pg.Surface((2,2))
                else:
                    surf = pg.Surface((1,1))
                surf.fill(row)
                win.blit(surf,(x*2+200,y*2+30))



