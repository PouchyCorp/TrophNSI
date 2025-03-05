r"""
      _ _       _                         
     | (_)     | |                        
   __| |_  __ _| | ___   __ _ _   _  ___  
  / _` | |/ _` | |/ _ \ / _` | | | |/ _ \ 
 | (_| | | (_| | | (_) | (_| | |_| |  __/ 
  \__,_|_|\__,_|_|\___/ \__, |\__,_|\___| 
                         __/ |            
                        |___/             

Key Features:
-------------
- Dialogue instance containing one dialogue option. 
- Handles text for each dialogue line.
- Updates the dialogue text progressively with animation effects.


      _ _       _                                                                      
     | (_)     | |                                                                     
   __| |_  __ _| | ___   __ _ _   _  ___   _ __ ___   __ _ _ __   __ _  __ _  ___ _ __ 
  / _` | |/ _` | |/ _ \ / _` | | | |/ _ \ | '_ ` _ \ / _` | '_ \ / _` |/ _` |/ _ \ '__|
 | (_| | | (_| | | (_) | (_| | |_| |  __/ | | | | | | (_| | | | | (_| | (_| |  __/ |   
  \__,_|_|\__,_|_|\___/ \__, |\__,_|\___| |_| |_| |_|\__,_|_| |_|\__,_|\__, |\___|_|   
                         __/ |                                          __/ |          
                        |___/                                          |___/           

Key Features:
-------------
- Manages multiple dialogues instances (above) loaded from a JSON file.
- Allows random selection of dialogues for interaction.
- Enhance the interaction with a robot character.
"""


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
        self.page = 0
        self.page_size = 5
    
    def get_text_surf(self, bot_name):
        return TERMINAL_FONT.render(f"{bot_name}@botOS:~$ {self.anim_chars}" , False, 'green')
    
    def update(self, bot_name):
        if self.showed_texte != self.anim_chars:
            self.anim_chars += self.showed_texte[len(self.anim_chars)]

        if self.page != self.part_ind//self.page_size: # If page changed
            self.page = self.part_ind//self.page_size
            self.bliting_list = [] # Reset showed texts

        if len(self.bliting_list)+(self.page*self.page_size)-1 < self.part_ind: # If dialogue text animation finished
            self.bliting_list.append(self.get_text_surf(bot_name)) # Add new line
        else:
            self.bliting_list[self.part_ind-(self.page*self.page_size)] = self.get_text_surf(bot_name) # Update line
    
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

class DialogueManager():
    def __init__(self):    #nécessite de donner le chemin exacte du fichier
        self.dialogues : list[Dialogue] = self.__init()
        self.special_dialogues = self.__special_init()
        self.selected_dialogue : Dialogue = Dialogue(["You shouldn't see this message"])
        self.bot_anim : Animation = None #idle anim of the robot clicked
        self.background = sprite.DIALBOX

    def __init(self) -> list[Dialogue]:
        with open("data/dialogue.json", encoding='utf8') as file:
            json_string = file.read()
            dialogues = []
            loaded_dicts = json.loads(json_string)
            for dict in loaded_dicts: 
                for dialogue in dict['dialogues']:
                    dialogues.append(Dialogue(dialogue))
            return dialogues
    
    def __special_init(self) -> dict[str, Dialogue]:
        with open("data/special_dialogue.json", encoding='utf8') as file:
            json_string = file.read()
            special_dialogues = {}
            loaded_dict = json.loads(json_string)
            for key in loaded_dict:
                special_dialogues[key] = Dialogue(loaded_dict[key])
            return special_dialogues
    
    def random_dialogue(self):
        if self.selected_dialogue:
            self.selected_dialogue.reset()

        self.selected_dialogue = rand.choice(self.dialogues)

    def special_dialogue(self, dialogue_name):
        if self.selected_dialogue:
            self.selected_dialogue.reset()
        
        self.selected_dialogue = self.special_dialogues[dialogue_name]

    def click_interaction(self):
        """Return True if the dialogue is finished"""
        if self.selected_dialogue.is_on_last_part():
            return True
        else:
            self.selected_dialogue.skip_to_next_part()
            return False

    def update(self):
        bot_name = "anon"
        self.selected_dialogue.update(bot_name)

    def draw(self, screen : pg.Surface):
        
        screen.blit(self.background, (300+46*6, 750)) 
        for i, surf in enumerate(self.selected_dialogue.bliting_list):
            line_height = 812 + 27 * i
            screen.blit(surf,(650, line_height))
        
        if self.bot_anim:
            scaled_bot_surface = pg.transform.scale2x(self.bot_anim.get_frame())
            scaled_bot_rect = scaled_bot_surface.get_rect(bottomright=(504, 1050))
            screen.blit(scaled_bot_surface, scaled_bot_rect)





