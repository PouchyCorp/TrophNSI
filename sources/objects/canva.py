import pygame as pg
from utils.coord import Coord
from objects.placeable import Placeable
from objects.patterns import Pattern
from ui.inputbox import InputBox


class Canva:
    def __init__(self, coord : Coord): 
        self.coord = coord

        self.size = (678,1020)
        self.surf = pg.Surface(self.size)
        self.surf.fill(pg.Color(240,240,240))
        
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = self.coord.xy
        
        self.name_input = InputBox(1446, 210, 100, 50)
        self.confirm_button = pg.Rect(1556, 210, 100, 50)

        self.name = "peinture"
        self.placed_patterns = []

    def get_placeable(self) -> Placeable:
        scaled_surf = pg.transform.scale_by(self.surf,0.5).convert()
        placeable = Placeable(self.name, self.coord, scaled_surf)
        return placeable
    
    def reset(self):
        self.surf.fill(pg.Color(240,240,240))
        self.placed_patterns.clear()
    
    def draw_pattern(self, pattern : Pattern):
        relative_pos = (pattern.rect.x - self.coord.x,
                        pattern.rect.y - self.coord.y)

        self.surf.blit(pattern.get_effect(), relative_pos)

    def place(self,mouse_pos : Coord, pattern : Pattern):
        x, y = mouse_pos.copy().get_pixel_perfect(0,12)
        
        self.placed_patterns.append(pattern)
    
    def draw(self, win):
        win.blit(self.surf, self.coord.xy)
        self.name_input.draw(win)
        pg.draw.rect(win, pg.Color(170, 170, 230), self.confirm_button)

    def handle_event(self, event):
        self.name_input.handle_event(event)
        if event.type == pg.MOUSEBUTTONUP and self.confirm_button.collidepoint(event.pos):
            self.name = self.name_input.text
            self.placed_patterns = []
            return True
        return False
            