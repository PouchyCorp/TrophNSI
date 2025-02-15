import pygame as pg
from utils.coord import Coord
from objects.placeable import Placeable
from objects.patterns import Pattern
from ui.inputbox import InputBox
from ui.sprite import FRAME_PAINTING

class Canva:
    def __init__(self, coord : Coord): 
        self.coord = coord

        self.size = (672,1020)
        self.surf = pg.Surface(self.size)
        self.surf.fill(pg.Color(240,240,240))
        
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = self.coord.xy
        
        self.name_input = InputBox(1446, 210, 100, 50)
        self.confirm_button = pg.Rect(1556, 210, 100, 50)

        self.name = "peinture"
        self.placed_patterns : list[Pattern] = []
        self.holded_pattern : Pattern = None

    def get_placeable(self) -> Placeable:
        for pattern in self.placed_patterns:
            self.draw_pattern(pattern)

        scaled_surf = pg.transform.scale_by(self.surf,0.5).convert()
        FRAME_PAINTING.blit(scaled_surf,(12,12))
        placeable = Placeable(self.name, self.coord, FRAME_PAINTING)
        return placeable
    
    def reset(self):
        self.surf.fill(pg.Color(240,240,240))
        self.placed_patterns.clear()
    
    def draw_pattern(self, pattern : Pattern):
        """Imprints the pattern on the canva."""
        relative_pos = (pattern.rect.x - self.coord.x,
                        pattern.rect.y - self.coord.y)

        self.surf.blit(pattern.get_effect(), relative_pos)

    def place_pattern(self, pattern : Pattern):
        """Place a moveable pattern."""
        self.placed_patterns.append(pattern)

    def hold_pattern(self, pattern):
        self.placed_patterns.remove(pattern)
        self.holded_pattern = pattern
        self.holded_pattern.rect.center = pg.mouse.get_pos()
    
    def drop_pattern(self, pos):
        if self.rect.collidepoint(pos):
            self.holded_pattern.rect.center = pos
            self.place_pattern(self.holded_pattern)
        self.holded_pattern = None
    
    def draw(self, win):
        win.blit(self.surf, self.coord.xy)

        for placed_pattern in self.placed_patterns:
            placed_pattern.draw(win)
        
        if self.holded_pattern:
            self.holded_pattern.draw(win)

        self.name_input.draw(win)
        pg.draw.rect(win, pg.Color(170, 170, 230), self.confirm_button)

    def handle_event(self, event):
        mouse_pos = pg.mouse.get_pos()

        self.name_input.handle_event(event)

        if event.type == pg.MOUSEBUTTONUP and self.confirm_button.collidepoint(mouse_pos):
            self.name = self.name_input.text
            self.placed_patterns = []
            return True
        
        eventual_collided_pattern = [pattern for pattern in self.placed_patterns if pattern.rect.collidepoint(mouse_pos)]
        if event.type == pg.MOUSEBUTTONDOWN and eventual_collided_pattern:
            self.hold_pattern(eventual_collided_pattern[0])
        
        if self.holded_pattern:
            if event.type == pg.MOUSEBUTTONUP:
                self.drop_pattern(mouse_pos)

            if event.type == pg.MOUSEMOTION:
                self.holded_pattern.rect.center = mouse_pos

        return False
            