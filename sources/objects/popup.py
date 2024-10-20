import pygame as pg
from coord import Coord

class Popup:
    def __init__(self, text):
        self.text : str = text

        self.font = pg.font.SysFont(None,30,False,False)
        self.text_surf = self.font.render(self.text, True, (0, 0, 0), (255,255,255))
        self.rect = self.text_surf.get_rect()

        self.lifetime : int = 60
        #set centered coordinates
        self.rect.y = 50
        self.rect.x = (1920/2)-(self.rect.width/2)

    def draw(self, screen):
        screen.blit(self.text_surf, self.rect)