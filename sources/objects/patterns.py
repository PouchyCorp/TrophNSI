from utils.coord import Coord
import pygame as pg
from ui.button import Button
from ui.sprite import whiten, PATTERN_LIST
from typing_extensions import Optional
import patterneffect

class Pattern:
    def __init__(self, coord, thumbnail : pg.Surface, price, beauty, effect = None, color : tuple = (0,0,0,255)):
        self.thumbnail = thumbnail
        self.rect = self.thumbnail.get_rect(topleft = coord)
        self.effect = effect
        self.color = color
        self.price = price
        self.beauty = beauty
    
    def draw(self, win : pg.Surface):
        win.blit(self.thumbnail, self.rect.topleft)

    def get_effect(self):
        if self.effect:
            return self.effect(self.thumbnail)
    
    def copy(self):
        return Pattern(self.rect.topleft, self.thumbnail, self.price, self.beauty, self.effect, self.color)

class PatternHolder:
    def __init__(self, coord : Coord, canva):
        self.patterns : list[Pattern] = [Pattern(coord.xy, thumbnail, i+1, i+1,  patterneffect.placeholder) for i, thumbnail in enumerate(PATTERN_LIST)]
        self.coord = coord 
        self.buttons : list[Button] = self.init_buttons()
        self.holded_pattern : Optional[Pattern]= None
        self.canva = canva

    def init_buttons(self):
        buttons = []
        y = self.coord.y
        x = self.coord.x
        for i, pattern in enumerate(self.patterns):
            button = Button((0,0), self.activate_pattern, whiten(pattern.thumbnail), pattern.thumbnail, [i])
            x += button.rect.width * 1.5
            if i and i % 4 == 0:
                x = self.coord.x
                y += button.rect.height * 1.5

            button.rect.x = x
            button.rect.y = y
            buttons.append(button)
        return buttons

    def activate_pattern(self, pattern_id):
        self.holded_pattern = self.patterns[pattern_id]
        self.holded_pattern.rect.center = pg.mouse.get_pos()

    def handle_event(self, event : pg.event.Event):
        for button in self.buttons:
            button.handle_event(event)
        
        if self.holded_pattern:
            if event.type == pg.MOUSEBUTTONUP:
                self.drop_pattern(event.pos)

            if event.type == pg.MOUSEMOTION:
                self.holded_pattern.rect.center = (int(event.pos[0]), int(event.pos[1]))
    
    def drop_pattern(self, pos):
        if self.canva.rect.collidepoint(pos):
            self.holded_pattern.rect.center = pos
            self.canva.place_pattern(self.holded_pattern.copy())
        self.holded_pattern = None
    
    def draw(self, win : pg.Surface):
        for button in self.buttons:
            button.draw(win, False)
        if self.holded_pattern:
            self.holded_pattern.draw(win)
