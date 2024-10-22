from pygame import Surface, Rect
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

    def __repr__(self) -> str:
        return str(self.__dict__)



# tests
if __name__ == '__main__':
    placeholder_surf = Surface((60,60))
    placeholder_surf.fill('red')
    painting = Placeable('skibidi', Coord(1, (650, 125)), placeholder_surf)
    print(painting)