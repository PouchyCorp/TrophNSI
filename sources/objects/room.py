import pygame as pg
from placeable import Placeable

class Room:
    def __init__(self, num) -> None:
        self.sizePx = (320,180)
        self.num = num
        self.placed : list[Placeable] = []

        #permanent objects that can not be edited (still place in placed to render the object)
        self.native_placed : list[Placeable] = []

    def in_native_placed(self, plcbl : Placeable) -> bool:
        return (plcbl in self.native_placed)
        
