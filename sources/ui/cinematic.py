from objects.dialogue import DialogueManager
from utils.anim import Animation
import pygame as pg
from typing_extensions import TYPE_CHECKING

# Very ugly, but it's the only way to avoid circular imports
if TYPE_CHECKING:
    from core.logic import Game 

class CinematicPlayer:
    def __init__(self, anim : Animation, dialogue_name):
        self.anim = anim

        self.dialogue = DialogueManager()
        self.dialogue.special_dialogue(dialogue_name)

        self.surf = self.anim.reset_frame()
        self.is_finished = False
    
    def get_status_event(self, event, game):
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.is_finished = True
        elif event.type == pg.QUIT:
            game.quit()
    
    def get_dialogue_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            return self.dialogue.click_interaction()
            
    def play_anim(self, game : 'Game'):
        band_size = (game.win.get_width(), 140)
        black_band = pg.Surface(band_size)
        clock = pg.time.Clock()
        while not self.anim.is_finished() and not self.is_finished:
            clock.tick(60)
            for event in pg.event.get():
                self.get_status_event(event, game)

            self.surf = self.anim.get_frame()
            self.surf.blit(black_band, (0,0))
            self.surf.blit(black_band, (0,1080-band_size[1]))
            
            game.draw_background()
            game.win.blit(self.surf, (0,0))
            pg.display.flip()
        
        self.surf = pg.transform.grayscale(self.surf)
    
    def play_dialogue(self, game : 'Game'):
        clock = pg.time.Clock()
        while not self.dialogue.selected_dialogue.is_on_last_part() and not self.is_finished:
            clock.tick(60)
            for event in pg.event.get():
                self.get_status_event(event, game)
                self.get_dialogue_event(event)
            
            self.dialogue.update()
            game.draw_background()
            game.win.blit(self.surf, (0,0))
            self.dialogue.draw(game.win)
            pg.display.flip()

    def play(self, game : 'Game'):
        self.play_anim(game)
        self.play_dialogue(game)
        self.is_finished = True
    
