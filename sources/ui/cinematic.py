from objects.dialogue import DialogueManager
from utils.anim import Animation
import pygame as pg
from typing_extensions import TYPE_CHECKING
from math import pi, sin
from utils.coord import Coord

# Very ugly, but it's the only way to avoid circular imports
if TYPE_CHECKING:
    from core.logic import Game 

class CinematicPlayer:
    def __init__(self, anim : Animation, dialogue_name, introspection_dialogue_name = None):
        self.anim = anim

        self.dialogue = DialogueManager()
        self.dialogue_name = dialogue_name
        self.introspection_dialogue = introspection_dialogue_name

        self.cutscene_surf = self.anim.reset_frame()
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

            self.cutscene_surf = self.anim.get_frame()
            self.cutscene_surf.blit(black_band, (0,0))
            self.cutscene_surf.blit(black_band, (0,1080-band_size[1]))
            
            game.draw_background()
            game.win.blit(self.cutscene_surf, (0,0))
            pg.display.flip()
        
        self.cutscene_surf = pg.transform.grayscale(self.cutscene_surf)
    
    def play_dialogue(self, game : 'Game'):
        clock = pg.time.Clock()
        finised_reading = False
        while not finised_reading and not self.is_finished:
            clock.tick(60)
            for event in pg.event.get():
                self.get_status_event(event, game)
                finised_reading = self.get_dialogue_event(event)
            
            self.dialogue.update()
            game.draw_background()
            game.win.blit(self.cutscene_surf, (0,0))
            self.dialogue.draw(game.win)
            pg.display.flip()
    
    def play_introspection_dialogue(self, game : 'Game'):
        clock = pg.time.Clock()
        while not self.dialogue.selected_dialogue.is_on_last_part() and not self.is_finished:
            clock.tick(60)
            for event in pg.event.get():
                self.get_status_event(event, game)
                self.get_dialogue_event(event)
            
            self.dialogue.update()
            game.draw(Coord(0,(0,0)))
            self.dialogue.draw(game.win)
            pg.display.flip()

    def play_transition(self, game : 'Game'):
        """Play a easy fade out transition"""
        clock = pg.time.Clock()
        mask = pg.Surface((game.win.get_width(), game.win.get_height()))
        mask.fill((0,0,0))
        incr = 0
        step_count = 2*60
        while incr < pi and not self.is_finished:
            clock.tick(60)
            incr += pi/step_count

            for event in pg.event.get():
                self.get_status_event(event, game)

            if incr < pi/2:
                game.draw_background()
                game.win.blit(self.cutscene_surf, (0,0))
                self.dialogue.draw(game.win)
            else:
                game.draw(Coord(0,(0,0))) 
            
            mask.set_alpha(sin(incr)*255)
            print(mask.get_alpha())
            game.win.blit(mask, (0,0))

            pg.display.flip()

    def play(self, game : 'Game'):
        self.play_anim(game)

        if self.dialogue_name:
            self.dialogue.special_dialogue(self.dialogue_name)
            self.play_dialogue(game)

        self.play_transition(game)

        if self.introspection_dialogue:
            self.dialogue.special_dialogue(self.introspection_dialogue)
            self.play_introspection_dialogue(game)

        self.is_finished = True
    
