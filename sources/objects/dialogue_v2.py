import random as rand
import pygame as pg
import json
from utils.anim import Animation


pg.init()

class Dialogue:
    def __init__(self, text : list[str]):
        self.textes = text
        self.anim_chars = ""
        self.part_ind = 0
        self.showed_texte = self.textes[self.part_ind]
        self.format = pg.font.SysFont("Arial", 20)
    
    def get_text_surf(self):
        return self.format.render(self.anim_chars, True, (255,255,255))
    
    def update(self):
        if self.showed_texte != self.anim_chars:
            self.anim_chars += self.showed_texte[len(self.anim_chars)]
    
    def is_on_last_part(self):
        return True if self.part_ind == len(self.textes)-1 else False

    def skip_to_next_part(self):
        if not self.is_on_last_part():
            self.part_ind += 1
            self.anim_chars = ""
            self.showed_texte = self.textes[self.part_ind]

    def reset(self):
        self.anim_chars = ""
        self.showed_texte = self.textes[0]
        self.part_ind = 0

class DialogueManagement():
    def __init__(self, fichier):    #nécessite de donner le chemin exacte du fichier
        self.fichier=fichier
        self.dialogues : list[Dialogue] = self.init()
        self.selected_dialogue : Dialogue = None
        self.bot_anim : Animation = None #idle anim of the robot clicked

    def init(self) -> list[list[str]]:
        with open(self.fichier, encoding='utf8') as file:
            json_string = file.read()
            dialogues = []
            loaded_lists = json.loads(json_string)
            for lst in loaded_lists:
                dialogues.append(Dialogue(lst))
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
        self.selected_dialogue.update()

    def draw(self, screen : pg.Surface):
        screen.blit(pg.Surface((1000,125)), (200, 750)) 
        screen.blit(self.selected_dialogue.get_text_surf(),(450, 800))
        screen.blit(self.bot_anim.get_frame(), (200, 750))





