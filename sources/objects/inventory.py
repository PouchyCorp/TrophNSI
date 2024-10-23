from placeable import Placeable
from coord import Coord
from pygame import Surface, transform

class Inventory:
    def __init__(self) -> None:
        '''list of owned items'''
        self.lst : list[Placeable] = []

        #false if closed, true if opened
        self.state = False
        self._page = 0

    def draw(self, win : Surface):
        surfs_rects_to_blit : list[tuple] = []

        for ind , obj in enumerate(self.lst):
            #8 element at a time ( or else too big)
            if ind >= 8:
                return
            
            biggest_side = max([obj.rect.width, obj.rect.height])
            scale_ratio = 180/biggest_side
            minimized_surf = transform.scale_by(obj.surf, scale_ratio)
            minimized_rect = minimized_surf.get_rect()

            #placement
            if ind % 2 == 0:
                minimized_rect.x = 50
            else:
                minimized_rect.x = 50+180+20

            minimized_rect.y = 50+(200*(ind//2))

            surfs_rects_to_blit.append((minimized_surf, minimized_rect))

        win.blits(surfs_rects_to_blit)



    def select_item(self, xy : Coord) -> int:
        """return the index of the item selected
        returns -1 if no items"""

        return
    
    def __repr__(self):
        return str(self.__dict__)

# tests
if __name__ == '__main__':
    pass