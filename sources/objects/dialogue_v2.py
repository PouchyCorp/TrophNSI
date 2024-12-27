import random as rand
import pygame
import json
#from anim import Animation, Spritesheet
#import sprite

pygame.init()
class DialogueManagement():
    def __init__(self, fichier):    #nécessite de donner le chemin exacte du fichier
        self.fichier=fichier
        #self.screen=screen    screen
        self.texte=[]
        self.number=None
        self.format = pygame.font.SysFont("Arial", 20)
        self.bot_surf = None
    

    def load_save(self):
        with open(self.fichier, encoding='utf8') as file:
            json_string = file.read()
            self.texte = json.loads(json_string)

    def load_dialogue(self, number):
        talked=""
        for letter in self.texte[number]:
            talked+=letter
        return talked
       
    def show(self, screen):
        txtsurf = self.format.render(self.load_dialogue(self.number), True, (255,255,255))
        screen.blit(pygame.Surface((1000,125)), (200, 750)) #a recadrer
        screen.blit(self.bot_surf, (200, 750)) #a recadrer
        screen.blit(txtsurf,(450, 800)) #a recadrer
        
    def random_dialogue(self):
        self.number=rand.randint(0, (len(self.texte)-1)) 


#test=Dialogue('data\dialoguetest.json')
#test.load_save()
#print(test.texte)


