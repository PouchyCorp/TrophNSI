from placeable import Placeable
from utils.coord import Coord
from pygame import Surface
from utils.coord import Coord
from pattern import Pattern

class PatternInv:
    def __init__(self,p_list) -> None:
        self.inv = []
        self.color_list = []
        for p in range(len(p_list)):
            self.inv.append(Pattern(p_list[p],self.color_list[p]))


    def draw(self, win : Surface):
        x,y = 100,100
        for pattern in self.inv:
            win.blit(pattern.button,(x,y))
            pattern.rect.x, pattern.rect.y = x,y
            if x < 500 :
                x += 200
            else:
                y += 100
                x = 100


    def select_pattern(self, mouse_pos : Coord) -> str | None:
        for pattern in self.inv:
            if pattern.rect.collidepoint(mouse_pos.xy):
                return pattern.button.copy()
        return None
    

    def __repr__(self):
        return str(self.__dict__)