from placeable import Placeable
from coord import Coord
from pygame import Surface
from coord import Coord
from pattern import Pattern

class PatternInv:
    def __init__(self,p_list) -> None:
        self.inv = []
        self.color_list = [[(0,0,0)],
                           [(50,50,50),(25,25,25)],
                           [(50,0,0),(75,0,0),(100,0,0),(125,0,0)],
                           [(0,100,100),(0,50,50),(0,150,150),(0,220,220)],
                           [(50,200,100),(170,50,50),(200,200,150)],
                           [(100,200,50),(50,170,50),(150,150,200)],
                           [(250,0,0),(0,250,0),(0,0,250)],
                           [(250,250,0),(0,250,250),(250,0,250)],
                           [(230,150,100),(60,20,140),(70,180,140),(190,60,100),(210,90,150)]]
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
                return pattern.button.surf.copy()
        return None
    

    def __repr__(self):
        return str(self.__dict__)