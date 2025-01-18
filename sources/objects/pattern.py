from utils.coord import Coord
import pygame as pg
from objects.canva import Canva
from random import choice

class Pattern:
    def __init__(self, pattern, colors):
        self.colors : list = colors
        self.surf : pg.Surface = self.pattern_init(pattern)
        self.coord = Coord(0,(0,0))

    
    def paint(self, clic : Coord, canva : Canva):
        coord = Coord(canva.coord.room_num,(clic.x-canva.coord.x,clic.y-canva.coord.y))
        coord.xy = coord.get_pixel_perfect(0,12)
        canva.surf.blit(self.surf,coord.xy)
    
    def pattern_init(self,pattern):
        self.surf = pg.transform.scale_by(pattern, 2)
        self.surf.fill(choice(self.colors)+tuple([0]), special_flags=pg.BLEND_RGBA_MAX)
        return self.surf

