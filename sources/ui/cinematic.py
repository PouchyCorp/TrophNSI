from objects.dialogue import DialogueManager
from utils.anim import Animation
from utils.coord import Coord
import pygame as pg

class CinematicPlayer:
    def __init__(self, anim : Animation, dialogue : DialogueManager):
        self.anim = anim
        self.surf = self.anim.reset_frame()
        self.is_finished = False

    def play(self, game):
        from core.logic import Game
        game : Game = game
        band_size = (game.win.get_width(), 180)
        black_band = pg.Surface(band_size)
        clock = pg.time.Clock()
        while not self.anim.is_finished():
            clock.tick(60)

            self.surf = self.anim.get_frame()
            self.surf.blit(black_band, (0,0))
            self.surf.blit(black_band, (0,1080-band_size[1]))
            

            game.draw(Coord(0,(0,0)))
            game.win.blit(self.surf, (0,0))
            pg.display.flip()
            self.is_finished = True
            
