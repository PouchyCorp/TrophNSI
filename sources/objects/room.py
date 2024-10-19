import pygame as pg
from placeable import Placeable

class Room:
    def __init__(self, num) -> None:
        self.sizePx = (320,180)
        self.num = num
        self.placed : list[Placeable] = []
        
