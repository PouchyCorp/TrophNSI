from pygame import Surface, Rect, transform, BLEND_RGBA_MAX
import sys
import os
#do not remove
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from coord import Coord
from anim import Animation

class Placeable:
    def __init__(self, name, coord : Coord, surf : Surface, anim : Animation | None = None,y_constraint : int | None = None) -> None:
        self.name = name
        self.coord = coord
        self.coord.xy = self.coord.get_pixel_perfect()
        self.coord.x, self.coord.y = self.coord.xy

        if anim:
            self.surf = anim.get_frame()
        else:
            self.surf = surf
        
        self.anim = anim


        self.rect : Rect = self.surf.get_rect()
        self.rect.x, self.rect.y = self.coord.xy
        
        #snap to x axis
        self.y_constraint = y_constraint
        self.placed = False

    def draw(self,win):
        win.blit(self.surf, self.rect)
    
    def update_anim(self):
        if self.anim:
            self.surf = self.anim.get_frame()
    
    def draw_outline(self, win : Surface, color : tuple):
        mask = self.surf.copy()
        mask = transform.scale(mask, (self.rect.width + 10, self.rect.height + 12))
        mask_rect = mask.get_rect(center=self.rect.center)
        mask.fill(color+tuple([0]),special_flags=BLEND_RGBA_MAX)
        win.blit(mask, mask_rect)
    
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