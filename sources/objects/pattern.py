from utils.coord import Coord
import pygame as pg
from objects.canva import Canva
from ui.sprite import SPRITESHEET_CHIP, CHIP_BUTTON

class Pattern:
    def __init__(self, pattern : pg.Surface, xy : tuple):
        self.surf : pg.Surface = self.pattern_init(pattern)
        self.button = CHIP_BUTTON
        self.rect = self.button.get_rect()
        self.rect.x, self.rect.y = xy
    
    def paint(self, clic : Coord, canva : Canva):
        coord = Coord(canva.coord.room_num,(clic.x-canva.coord.x,clic.y-canva.coord.y))
        coord.xy = coord.get_pixel_perfect(0,12)
        canva.surf.blit(self.surf,coord.xy)
    
    def pattern_init(self,pattern):
        self.surf = pg.transform.scale_by(pattern, 6)
        return self.surf
    
    def draw(self, win):
        win.blit(self.button, self.rect.xy)

