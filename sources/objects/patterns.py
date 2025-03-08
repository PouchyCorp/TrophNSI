from utils.coord import Coord
import pygame as pg
from ui.button import Button
from ui.sprite import whiten, PATTERN_LIST, DRAWER_LIST, DRAWER_HOLDER
from typing_extensions import Optional
from ui.infopopup import InfoPopup

class Pattern:
    def __init__(self, coord, thumbnail : pg.Surface, price, beauty, color : tuple = (0,0,0,255)):
        self.thumbnail = thumbnail
        self.rect = self.thumbnail.get_rect(topleft = coord)
        self.color = color
        self.price = price
        self.beauty = beauty
    
    def draw(self, win : pg.Surface):
        win.blit(self.thumbnail, self.rect.topleft)

    def get_effect(self):
        return self.thumbnail.copy()
    
    def copy(self):
        return Pattern(self.rect.topleft, self.thumbnail, self.price, self.beauty, self.color)

class PatternHolder:
    def __init__(self, coord : Coord, canva):
        self.patterns : list[Pattern] = [Pattern(coord.xy, thumbnail, i+1, i+1) for i, thumbnail in enumerate(PATTERN_LIST)]
        self.coord = coord 
        self.surf = DRAWER_HOLDER.copy()
        self.drawers : list[Button] = self.init_buttons()
        self.holded_pattern : Optional[Pattern]= None

        from objects.canva import Canva
        self.canva : Canva = canva

    def init_buttons(self):
        buttons = []
        drawer_sprites = DRAWER_LIST # List of sprites for the drawers
        # Respective coordinates for each drawer
        drawer_coords = [(10*6,8*6), (36*6,8*6), (10*6,34*6), (43*6,34*6), (10*6,62*6), (35*6,62*6), (61*6,62*6), (10*6,85*6), (35*6,85*6), (61*6,85*6), (35*6,129*6), (10*6,108*6), (10*6,121*6), (35*6,108*6), (61*6,108*6)] # Respect the order of the sprites, please

        for i in range(15):
            button = Button(drawer_coords[i], self.hold_pattern, whiten(drawer_sprites[i]), drawer_sprites[i], [i]) # Create a button for each drawer
            buttons.append(button)

        return buttons

    def hold_pattern(self, pattern_id):
        """Transfers the pattern from the drawer to the cursor.
        The logic is passed to the Canva object because of a drawing order dilemma."""
        self.canva.game.sound_manager.items.play()
        self.canva.hold_pattern_from_drawer(self.patterns[pattern_id])

    def handle_event(self, event : pg.event.Event):
        for button in self.drawers:
            button.handle_event(event)
    
    def draw(self, win : pg.Surface):
        for button in self.drawers:
            button.draw(self.surf, button.rect.collidepoint(pg.mouse.get_pos()))
        win.blit(self.surf, self.coord.xy)
