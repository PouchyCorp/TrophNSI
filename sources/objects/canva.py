import pygame as pg
from utils.coord import Coord
from objects.placeable import Placeable
from objects.patterns import Pattern
from ui.inputbox import InputBox
from ui.sprite import FRAME_PAINTING, invert_alpha, YES_BUTTON, NO_BUTTON, whiten
from ui.button import Button
from ui.confirmationpopup import ConfirmationPopup
from ui.infopopup import InfoPopup
from utils.fonts import TERMINAL_FONT

class Canva:
    def __init__(self, coord : Coord, game): 
        self.coord = coord

        self.size = (672,1020)
        self.surf = pg.Surface(self.size)
        self.bg_color = (236, 235, 222)
        self.surf.fill(self.bg_color)
        
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = self.coord.xy
        
        self.name_input = InputBox(1446, 210, 100, 50)
        self.confirm_button = Button((1556, 210), int, whiten(NO_BUTTON), NO_BUTTON) # Int is a callable placeholder.
        self.paint_button = Button((1556, 310), self.start_painting, whiten(YES_BUTTON), YES_BUTTON)
        
        from core.logic import Game
        self.game : Game = game

        self.name = "peinture"
        self.placed_patterns : list[Pattern] = []
        self.holded_pattern : Pattern = None

        self.total_price = 0
        self.total_beauty = 0

    def get_placeable(self) -> Placeable:
        scaled_surf = pg.transform.scale_by(self.surf.copy(),0.5).convert()
        FRAME_PAINTING.blit(scaled_surf,(12,12))
        placeable = Placeable(self.name, self.coord, FRAME_PAINTING, beauty=self.total_beauty, tag="decoration")
        self.reset()
        return placeable
    
    def check_price(self, price):
        if self.game.money - price >= 0:
            self.game.money -= price
            return True
        else:
            self.game.popups.append(InfoPopup("Vous n'avez pas assez d'argent pour peindre :("))
            self.game.sound_manager.incorrect.play()
            return False

    def get_price(self):
        self.total_price = 0
        for pattern in self.placed_patterns:
            self.total_price += pattern.price
        return self.total_price

    def add_to_beauty(self, patterns : list[Pattern]):
        for pattern in patterns:
            self.total_beauty += pattern.beauty
    
    def reset(self):
        self.__init__(self.coord, self.game)
    
    def get_next_stage(self):
        temp_surf = pg.Surface(self.size)
        temp_surf = temp_surf.convert_alpha()
        temp_surf.fill((0,0,0,0))

        for pattern in self.placed_patterns:
            self.draw_pattern(temp_surf, pattern)

        invert_alpha(temp_surf)
        temp_surf.fill((200,50,50,0), special_flags=pg.BLEND_RGBA_MAX)

        self.surf.blit(temp_surf, (0,0))

    def start_painting(self):
        if self.check_price(self.get_price()):
            self.get_next_stage()
            self.add_to_beauty(self.placed_patterns)
    
    def draw_pattern(self, surf, pattern : Pattern):
        """Imprints the pattern on the canva."""
        relative_pos = (pattern.rect.x - self.coord.x,
                        pattern.rect.y - self.coord.y)

        surf.blit(pattern.get_effect(), relative_pos)

    def place_pattern(self, pattern : Pattern):
        """Place a moveable pattern."""
        self.placed_patterns.append(pattern)
        self.get_price()

    def hold_pattern(self, pattern):
        self.placed_patterns.remove(pattern)
        self.get_price()
        self.holded_pattern = pattern
        self.holded_pattern.rect.center = pg.mouse.get_pos()
        self.game.sound_manager.items.play()
    
    def drop_pattern(self, pos):
        if self.rect.collidepoint(pos):
            self.holded_pattern.rect.center = pos
            self.place_pattern(self.holded_pattern)
            self.game.sound_manager.items.play()
        else:
            self.game.popups.append(InfoPopup("Vous reposez le pochoir dans l'armoire."))
        self.holded_pattern = None
    
    def draw(self, win):
        win.blit(self.surf, self.coord.xy)

        for placed_pattern in self.placed_patterns:
            placed_pattern.draw(win)
        
        if self.holded_pattern:
            self.holded_pattern.draw(win)
        
        win.blit(TERMINAL_FONT.render(f"Prix : {self.total_price} / Beauté totale : {self.total_beauty}", True, 'blue'), (1356, 110))

        self.name_input.draw(win)
        self.confirm_button.draw(win, self.confirm_button.rect.collidepoint(pg.mouse.get_pos()))
        self.paint_button.draw(win, self.paint_button.rect.collidepoint(pg.mouse.get_pos()))

    def handle_event(self, event):
        mouse_pos = pg.mouse.get_pos()

        self.name_input.handle_event(event)
        self.paint_button.handle_event(event)
        if self.confirm_button.handle_event(event):
            self.name = self.name_input.text
            self.game.confirmation_popups.append(ConfirmationPopup(self.game.win, "are you sure you want to save the canva ?", self.game.save_canva))
        
        eventual_collided_pattern = [pattern for pattern in self.placed_patterns if pattern.rect.collidepoint(mouse_pos)]
        if event.type == pg.MOUSEBUTTONDOWN and eventual_collided_pattern:
            self.hold_pattern(eventual_collided_pattern[0])

        
        if self.holded_pattern:
            if event.type == pg.MOUSEBUTTONUP:
                self.drop_pattern(mouse_pos)

            if event.type == pg.MOUSEMOTION:
                self.holded_pattern.rect.center = mouse_pos

        return False
            