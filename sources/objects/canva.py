import pygame as pg
from coord import Coord
from chip import Chip
from PIL import Image

class Painting:

    def __init__(self):
        self.canva = Image.new('RGB', (48, 64))
        self.coord = Coord(-1,(210,30))
        self.surface = pg.Surface.convert(self.canva)
        self.name = None

    def draw(self,win,start : Coord,chip : Chip):
        drawing == False
        for y in range(64):
            for x in range(48):
                if (x,y) == start.xy:
                    drawing == True
                    row,col = 0,0
                if drawing:
                    im.putpixel((row+1,col+1),(chip.patern[row][col]))
        win.blit((2,2),(self.coord.x+x,self.coord.y+y))

pg.init()
WIN = pg.display.set_mode((1920, 1080))