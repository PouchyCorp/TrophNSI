from pygame import Surface, Rect, transform, BLEND_RGBA_MAX, BLEND_RGBA_MIN, SRCALPHA
import sys
import os
from random import randint
#do not remove
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from coord import Coord
from anim import Animation
from sprite import get_outline

class Placeable:
    def __init__(self, name : str, coord : Coord, surf : Surface, tag : str | None = None, anim : Animation | None = None, y_constraint : int | None = None) -> None:
        self.name = name
        self.id = randint(0,10000000)
        self.coord = coord
        self.coord.xy = self.coord.get_pixel_perfect()
        self.coord.x, self.coord.y = self.coord.xy

        if anim:
            self.surf = anim.get_frame()
        else:
            self.surf = surf
        self.anim = anim

        self.tag = tag


        self.rect : Rect = self.surf.get_rect()
        self.rect.x, self.rect.y = self.coord.xy
        
        #snap to x axis
        self.y_constraint = y_constraint
        self.placed = False

    def draw(self,win):
        win.blit(self.surf,self.rect)
    
    def update_anim(self):
        if self.anim:
            self.surf = self.anim.get_frame()


    def draw_outline(self, win : Surface, color : tuple):
        win.blit(get_outline(self.surf, color), (self.rect.x-3, self.rect.y-3))
    
    def move(self, coord : Coord):
        self.coord = coord
        self.coord.xy = coord.get_pixel_perfect()
        self.rect.topleft = self.coord.xy

    def pixelise(self):
        """makeshift pixel art shader for 6*6 pixels"""
        self.surf = transform.scale_by(self.surf, 1/6)
        self.surf = transform.scale_by(self.surf, 6)

    def __repr__(self) -> str:
        return str(self.__dict__)



# tests
if __name__ == '__main__':
    placeholder_surf = Surface((60,60))
    placeholder_surf.fill('red')
    painting = Placeable('skibidi', Coord(1, (650, 125)), placeholder_surf)
    print(painting)