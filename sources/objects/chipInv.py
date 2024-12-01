from placeable import Placeable
from coord import Coord
from pygame import Surface
#from sprite import PATTERN_LIST
from coord import Coord

class Pattern:
    def __init__(self,pattern,coord):
        self.surf = pattern
        self.coord : Coord = coord
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = self.coord.xy


class ChipInv:
    def __init__(self) -> None:
        self.inv = []
        x,y = 100, 100
        for p in []: #PATTERN_LIST:
            self.inv.append(Pattern(p,Coord(0,(x,y))))
            if x < 400:
                x += 150
            else:
                y += 150
                x = 100


    def draw(self, win : Surface):
        for pattern in self.inv:
            win.blit(pattern.surf,pattern.coord.xy)


    def mouse_highlight(self, win : Surface, mouse_pos : Coord):
        for placeable in self.showed_objects:
            if placeable.rect.collidepoint(mouse_pos.xy):
                placeable.draw_outline(win,(150,150,255))


    def select_chip(self, mouse_pos : Coord) -> str | None:
        for button in self.inv:
            if button.rect.collidepoint(mouse_pos.xy):
                return button.surf.copy()
        return None
    

    def __repr__(self):
        return str(self.__dict__)