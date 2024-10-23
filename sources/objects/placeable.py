from pygame import Surface, Rect, transform, BLEND_RGBA_MAX
import sys
import os
#do not remove
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from coord import Coord

class Placeable:
    def __init__(self, name, coord : Coord, surf : Surface, placed : bool = False) -> None:
        self.name = name
        self.coord = coord
        self.coord.xy = self.coord.get_pixel_perfect()

        self.surf = surf

        self.rect : Rect = self.surf.get_rect()
        self.rect.x, self.rect.y = self.coord.xy
        self.placed = placed

    def draw(self,win):
        win.blit(self.surf, self.rect)
    
    def draw_outline(self, win):
        mask = self.surf.copy()
        mask = transform.scale(mask, (self.rect.width + 10, self.rect.height + 12))
        mask_rect = mask.get_rect(center=self.rect.center)
        mask.fill((200,200,255,0),special_flags=BLEND_RGBA_MAX)
        win.blit(mask, mask_rect)

    def __repr__(self) -> str:
        return str(self.__dict__)



# tests
if __name__ == '__main__':
    placeholder_surf = Surface((60,60))
    placeholder_surf.fill('red')
    painting = Placeable('skibidi', Coord(1, (650, 125)), placeholder_surf)
    print(painting)