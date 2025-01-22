import pygame as pg
from utils.fonts import TERMINAL_FONT

COLOR_ACTIVE = (60,60,60)
COLOR_INACTIVE = (50,50,50)
class Button:
    def __init__(self, coord : tuple, effect, surf_active = None, surf_inactive = None, param : list = None):
        assert surf_active or surf_inactive, "initalize at least one of the two surface attributes"
        self.surf_active = surf_active
        self.surf_inactive = surf_inactive
        self.surf : pg.Surface = surf_inactive if surf_inactive else surf_active
        self.rect : pg.Rect = self.surf.get_rect(topleft=coord)
        self.effect = effect
        self.param = param if param else []

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Activates the button's effect when pressed 
                self.effect(*self.param)

    def draw(self, win : pg.Surface, is_hovered : bool):
        # Changes the sprite if the button is hovered
        if is_hovered:
            self.surf = self.surf_active if self.surf_active else self.surf
        else:
            self.surf = self.surf_inactive if self.surf_inactive else self.surf
            
        # Blit the text.
        win.blit(self.surf, self.rect)