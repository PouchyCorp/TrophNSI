from random import *
import pygame 

pygame.init()
class Dialogue():
    def __init__(self, fichier, ):
        self.fichier=fichier
        #self.screen=screen    screen
        self.avatar= pygame.image.load('data\image_dialogue.png').convert_alpha()
        self.format = pygame.font.SysFont("Arial", 40)
        self.texte=[]
        self.number=None

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

    def show(self):
        a=self.random_dialogue()
        txtsurf = self.format.render(self.texte[a], True, (255,255,255))
        self.screen.blit(self.avatar, (200, 600)) #a recadrer
        self.screen.blit(txtsurf,(500, 900)) #a recadrer
        
        pygame.display.flip()
    
    def random_dialogue(self):
        self.number=randint(0, len(self.texte)) 
        return self.number




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