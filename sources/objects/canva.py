
import pygame as pg
from coord import Coord

class Painting:
    def __init__(self):
        self.coord = Coord(666,(600,60))
        self.pixels = [["#FFFFFF" for col in range(48)] for row in range(64)]
        self.name = None

    def draw(self,win):
        for y,line in enumerate(self.pixels):
            for x,row in enumerate(line):
                if True:
                    pxl = 12
                else:
                    pxl = 6
                surf = pg.Surface((pxl,pxl))
                surf.fill(row)
                win.blit(surf,(x*pxl+600,y*pxl+60))



