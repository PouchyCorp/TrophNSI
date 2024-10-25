import pygame as pg
from placeable import Placeable

class Room:
    def __init__(self, num, bg_surf) -> None:
        self.sizePx = (320,180)
        self.num = num
        self.placed : list[Placeable] = []
        self.bg_surf = pg.transform.scale_by(bg_surf, 6)
        #permanent objects that can not be edited (still place in placed to render the object)
        self.blacklist : list[Placeable] = []

    def in_blacklist(self, plcbl : Placeable) -> bool:
        return (plcbl in self.blacklist)
    
    """
    def check_coords(self, placeable : Placeable):
        '''removes object if it's room number doesn't match with the room'''
        if placeable.coord.room_num != self.num:
            self.placed.remove(placeable)
    """
    def draw_placed(self, win):
        #map(self.check_coords, self.placed)
        win.blits([(placeable.surf, placeable.coord.xy) for placeable in self.placed])
        
# tests
if __name__ == '__main__':
    pass