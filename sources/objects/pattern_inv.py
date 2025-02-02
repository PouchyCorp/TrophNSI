from placeable import Placeable
from utils.coord import Coord
import pygame as pg
from ui.sprite import SPRITESHEET_CHIP, CHIP_BUTTON
from utils.anim import Animation, Spritesheet

class Pattern:
    def __init__(self, pattern : pg.Surface, xy : tuple):
        self.surf : pg.Surface = self.pattern_init(pattern)
        self.button = CHIP_BUTTON
        self.rect = self.button.get_rect()
        self.rect.x, self.rect.y = xy

        self.anim_right = Animation(SPRITESHEET_CHIP, 0, 4, 2)
        self.anim_left = Animation(SPRITESHEET_CHIP, 1, 4, 2)
        self.anim_down = Animation(SPRITESHEET_CHIP, 2, 4, 2)
    
    def pattern_init(self,pattern):
        self.surf = pg.transform.scale_by(pattern, 2)
        return self.surf


class PatternInv:
    def __init__(self,p_list) -> None:
        self.inv = []
        self.color_list = []
        for p in range(len(p_list)):
            self.inv.append(Pattern(p_list[p],self.color_list[p]))


    def draw(self, win : pg.Surface):
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