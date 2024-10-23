from placeable import Placeable
from coord import Coord
from pygame import Surface, transform

class Inventory:
    def __init__(self) -> None:
        '''list of owned items'''
        self.lst : list[Placeable] = []

        #showed placeables when opened
        self.showed_objects : list[Placeable] = []
        #false if closed, true if opened
        self.opened = False
        self._page = 0

    def open(self):
        self.showed_objects = self.lst[self._page*8:]
        self.opened = True

        for ind , obj in enumerate(self.showed_objects):
            #8 element at a time ( or else too big)
          
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
            
            self.showed_objects[ind] = Placeable(obj.name, Coord(obj.coord.room, minimized_rect.topleft), minimized_surf)

    def close(self):
        #to optimize if needed
        self.showed_objects = []
        self.opened = True

    def draw(self, win : Surface):
        if self.opened:
            win.blits([(plcb.surf, plcb.rect) for plcb in self.showed_objects])
        else:
            win.blit(Surface((60,60)), (0,60))



    def select_item(self, xy : Coord) -> int:
        """return the index of the item selected
        returns -1 if no items"""

        return
    
    def __repr__(self):
        return str(self.__dict__)

# tests
if __name__ == '__main__':
    pass