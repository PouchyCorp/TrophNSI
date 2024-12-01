from random import *
import pygame
from anim import Animation, Spritesheet
#import sprite

pygame.init()
class Dialogue():
    def __init__(self, fichier):    #nécessite de donner le chemin exacte du fichier
        self.fichier=fichier
        #self.screen=screen    screen
        self.avatar= pygame.image.load('data\Fond.png')
        self.texte=[]
        self.number=None
        self.format = pygame.font.SysFont("Arial", 20)
    

    def load_save(self):
        self.texte=[]  #debogage
        fich_ouvert=open(self.fichier, encoding='utf8') 
        for lines in fich_ouvert:
            mot=''
            intermediate=[]
            for k in range(len(lines)-1):
                mot+=lines[k]
            intermediate.append(mot)
            self.texte.append(intermediate)

    def load_dialogue(self, number):
        talked=""
        for letter in self.texte[number]:
            talked+=letter
        return talked

# A pour vocation de disparaitre
   
    def show(self, screen, talked, robot):
        
        txtsurf = self.format.render(talked, True, (255,255,255))
        screen.blit(self.avatar, (200, 200)) #a recadrer
        screen.blit(robot, (200, 200)) #a recadrer
        screen.blit(txtsurf,(200, 200)) #a recadrer
        
        pygame.display.flip()
    
    def random_dialogue(self):
        self.number=randint(0, len(self.texte)) 
        return self.number

    
         


"""
test=Dialogue('data\dialogue.txt')
test.load_save()

""""""Initialisateur pygame"""""" 

ecran = pygame.display.set_mode((1000, 800))
bg = (127,127,127)
done = False
format = pygame.font.SysFont("Arial", 40)
#SPRITESHEET_BOT = anim.Spritesheet(load_image('data/test_robot.png'), (48*6, 48*6))

while not done:
   for event in pygame.event.get():
      ecran.fill(bg)
      if event.type == pygame.QUIT:
         done = True

      if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_SPACE:
                            a=test.random_dialogue()
                            dit=test.load_dialogue(a)
                            test.show(ecran, dit)
                            """
                        
#SPRITESHEET_BOT = Spritesheet(pygame.image.load('data/test_robot.png'), (48*6, 48*6))
#animated = Animation(sprite.SPRITESHEET_BOT, 0, 7)




###Tests

"""
dialogue=init('data\dialogue.txt')
print(dialogue)


screen = pygame.display.set_mode((1920, 1080))
done = False

format = pygame.font.SysFont("Arial", 40)
'''fond = pygame.image.load('bg_test_approfondis.png').convert


screen.blit(fond, (0, 0))'''

avatar = pygame.image.load('data\image_dialogue.png').convert_alpha()

bg = (127,127,127)

while not done:
   for event in pygame.event.get():
      screen.fill(bg)
      if event.type == pygame.QUIT:
         done = True
      
      if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_SPACE:
                        txtsurf = format.render("Hello, World", True, (255,255,255))
                        screen.blit(avatar, (200, 600)) #a recadrer
                        screen.blit(txtsurf,(500, 900)) #a recadrer
                        
                        pygame.display.flip()
#def affichage():
"""