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

        for ind , obj in enumerate(self.lst):
            #8 element at a time ( or else too big)
            if ind >= 8:
                return
            
            minimized_surf = transform.scale(obj.surf, (180,180))
            minimized_rect = minimized_surf.get_rect()

            #placement
            if ind % 2 == 0:
                minimized_rect.x = 50
            else:
                minimized_rect.x = 50+180+20

            minimized_rect.y = 50+(200*(ind//2))

            win.blit(minimized_surf, minimized_rect)



    def select_item(self, xy : Coord) -> int:
        """return the index of the item selected
        returns -1 if no items"""

        return -1
    
    def __repr__(self):
        return str(self.__dict__)

# tests
if __name__ == '__main__':
    pass