from coord import Coord
import pygame as pg
from sprite import CHIP
from canva import Painting
from time import sleep

class Chip:
    def __init__(self, patern):
        self.patern : list = patern
        self.patern_line, self.patern_col = len(self.patern), len(self.patern[0])
        self.sprite = CHIP
        self.coord = Coord(666,((598,57)))
        self.drawing = False
        self.start = False

    def draw(self,win):
        win.blit(self.sprite,self.coord.xy)
    
    def paint(self, clic : Coord, canva : Painting,win):
        clic.xy = clic.get_pixel_perfect(0,12)
        clic.x,clic.y = clic.xy
        X,Y = 0,0
        self.patern_line, self.patern_col = len(self.patern), len(self.patern[0])

        for y in range(63):
            for x in range(47):
                self.check(clic,canva,x,y,X,Y)
                #sleep(0.0016)
                if self.drawing:
                    X += 1
            if self.drawing:
                Y += 1
                if self.patern_col != 0:
                    self.patern_col = 0
                    self.drawing = False
            X = 0
    
    def check(self,clic,canva,x,y,X,Y):
        if clic.xy == (x*12,y*12):
            self.drawing = True
            self.start = True

        if self.start:
            if clic.x == x*12 and self.patern_line != 0:
                self.drawing = True
                Y = 0

            if Y >= len(self.patern):
                self.drawing = False

            if self.drawing:
                if self.patern[Y][X] != "":
                    canva.pixels[y][x] = self.patern[Y][X]
                self.patern_col -= 1

            if self.patern_col == 0:
                self.patern_col = len(self.patern[0])
                self.patern_line -= 1
                self.drawing = False
            
            if self.patern_line == 0:
                self.drawing = False
