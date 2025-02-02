import pygame as pg
from utils.coord import Coord
from objects.placeable import Placeable

class Canva:
    def __init__(self): 
        self.coord = Coord(0,(621,30))
        self.surf = pg.Surface((678,1020))
        self.surf.fill(pg.Color(0,255,0))
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = self.coord.xy
        self.name = None
        self.pattern_num = 0

    def save(self,inv):
        inv.append(Placeable("painting",self.coord,pg.transform.scale_by(self.surf,0.5)))
        self.surf.fill(pg.Color(0,255,0))
        return self.surf.copy()

    def paint(self,mouse_pos,pattern,color):
        mouse_pos.xy = mouse_pos.get_pixel_perfect(0,12)
        

        for x in range(pattern.surf.get_rect().w):
            for y in range(pattern.surf.get_rect().h):
                if pattern.surf.get_at((x,y))[:3] == (255,255,255)[:3]:
                    pattern.surf.set_at((x, y), color)
        
        self.surf.blit(pattern.surf.copy(),(mouse_pos.x-self.coord.x, mouse_pos.y-self.coord.y))