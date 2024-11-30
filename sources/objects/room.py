import pygame as pg
from placeable import Placeable

class Room:
    def __init__(self, num, bg_surf) -> None:
        self.size_px = (320,180)
        self.num = num
        self.placed : list[Placeable] = []
        self.bg_surf = bg_surf
        #permanent objects that can not be edited (still place in placed to render the object)
        self.blacklist : list[Placeable] = []

    def in_blacklist(self, plcbl : Placeable) -> bool:
        return (plcbl in self.blacklist)
    
    def name_exists_in_placed(self, name : str) -> bool:
        for obj in self.placed:
            if obj.name == name:
                return True
        return False
    
    def draw_placed(self, win):
        #map(self.check_coords, self.placed)
        win.blits([placeable.get_blit_args() for placeable in self.placed])
        for placeable in self.placed:
            if placeable.temporary:
                self.placed.remove(placeable)