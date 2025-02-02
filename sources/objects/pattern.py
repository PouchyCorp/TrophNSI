from utils.coord import Coord
import pygame as pg
from objects.canva import Canva
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