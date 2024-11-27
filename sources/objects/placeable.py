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
        self.temp_surf = self.surf.copy()

        self.tag = tag


        self.rect : Rect = self.surf.get_rect()
        self.rect.x, self.rect.y = self.coord.xy
        self.temp_rect = self.rect.copy()
        
        #snap to x axis
        self.y_constraint = y_constraint
        self.placed = False

    def get_blit_args(self):
        return self.temp_surf, self.temp_rect

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
    
    def interaction(self, args):
        #doesn't do anything (used for subclasses)
        pass

    def update_sprite(self, is_hovered : bool, color : tuple = (150, 150, 255)):
        if self.anim:
            self.surf = self.anim.get_frame()

        if is_hovered:
            self.temp_surf = get_outline(self.surf, color)
            self.temp_surf.blit(self.surf, (3,3))
            self.temp_rect = self.rect.copy()
            self.temp_rect.x -= 3
            self.temp_rect.y -= 3
        else:
            self.temp_surf = self.surf.copy()
            self.temp_rect = self.rect.copy()



# tests
if __name__ == '__main__':
    placeholder_surf = Surface((60,60))
    placeholder_surf.fill('red')
    painting = Placeable('skibidi', Coord(1, (650, 125)), placeholder_surf)
    print(painting)