import random as rand
import pygame as pg
import json
from utils.anim import Animation
import ui.sprite as sprite
from utils.fonts import TERMINAL_FONT


pg.init()

class Dialogue:
    def __init__(self, text : list[str]):
        self.textes = text
        self.anim_chars = ""
        self.bliting_list : list[pg.Surface]= []
        self.part_ind = 0
        self.showed_texte = self.textes[self.part_ind]
    
    def get_text_surf(self, bot_name):
        return TERMINAL_FONT.render(f"{bot_name}@botOS:~$ {self.anim_chars}" , False, 'green')
    
    def update(self, bot_name):
        if self.showed_texte != self.anim_chars:
            self.anim_chars += self.showed_texte[len(self.anim_chars)]

        if len(self.bliting_list)-1 < self.part_ind:
            self.bliting_list.append(self.get_text_surf(bot_name))
        else:
            self.bliting_list[self.part_ind] = self.get_text_surf(bot_name)
    
    def is_on_last_part(self):
        return True if self.part_ind == len(self.textes)-1 else False

    def skip_to_next_part(self):
        if not self.is_on_last_part() and self.showed_texte == self.anim_chars:
            self.part_ind += 1
            self.anim_chars = ""
            self.showed_texte = self.textes[self.part_ind]

    def reset(self):
        self.anim_chars = ""
        self.showed_texte = self.textes[0]
        self.bliting_list = []
        self.part_ind = 0

class DialogueManagement():
    def __init__(self, fichier):    #nécessite de donner le chemin exacte du fichier
        self.fichier=fichier
        self.dialogues : list[Dialogue] = self.init()
        self.selected_dialogue : Dialogue = None
        self.bot_anim : Animation = None #idle anim of the robot clicked
        self.background = sprite.DIALBOX#sprite.nine_slice_scaling(sprite.WINDOW, (1300, 252), 12)

    def init(self) -> list[list[str]]:
        with open(self.fichier, encoding='utf8') as file:
            json_string = file.read()
            dialogues = []
            loaded_dicts = json.loads(json_string)
            for dict in loaded_dicts: 
                for dialogue in dict['dialogues']:
                    dialogues.append(Dialogue(dialogue))
            return dialogues
    
    def random_dialogue(self):
        if self.selected_dialogue:
            self.selected_dialogue.reset()

        self.selected_dialogue = rand.choice(self.dialogues)

    def click_interaction(self):
        if self.selected_dialogue.is_on_last_part():
            return True
        else:
            self.selected_dialogue.skip_to_next_part()
            return False

    def update(self):
        bot_name = "anonyme"
        self.selected_dialogue.update(bot_name)

    def draw(self, screen : pg.Surface):
        
        screen.blit(self.background, (300, 750)) 
        for i, surf in enumerate(self.selected_dialogue.bliting_list):
            line_height = 812 + 27 * i
            screen.blit(surf,(650, line_height))
        scaled_bot_surface = pg.transform.scale2x(self.bot_anim.get_frame())
        scaled_bot_rect = scaled_bot_surface.get_rect(bottomright=(504, 1050))
        screen.blit(scaled_bot_surface, scaled_bot_rect)





