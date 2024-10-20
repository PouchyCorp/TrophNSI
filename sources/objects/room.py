import pygame as pg
from placeable import Placeable

class Room:
    def __init__(self, num, bg_surf) -> None:
        self.sizePx = (320,180)
        self.num = num
        self.placed : list[Placeable] = []
        self.bg_surf  = bg_surf
        #permanent objects that can not be edited (still place in placed to render the object)
        self.blacklist : list[Placeable] = []

    def in_native_placed(self, plcbl : Placeable) -> bool:
        return (plcbl in self.native_placed)
        
