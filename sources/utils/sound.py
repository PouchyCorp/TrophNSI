import pygame

from random import *

class SoundManager():
    def __init__(self, name, time=0):
        self.name=name
        self.time=time
        

    def played(self, fade, vlm, loop):
        PLAYING.fadeout(fade)
        PLAYING.set_volume(vlm)
        PLAYING.play(loop)
    
    def stop(self):
        PLAYING=pygame.mixer.Sound(self.name)
        PLAYING.stop()
    
class Sound():
    def __init__(self):
        self.accrocher = pygame.mixer.Sound('data/sound/accrocher_tableau.mp3')
        self.accrocher2 = pygame.mixer.Sound('data/sound/accrocher.mp3')
        self.achieve = pygame.mixer.Sound('data/sound/achieve.mp3')
        self.blank_sound = pygame.mixer.Sound('data/sound/blank_sound.mp3')
        self.bott = pygame.mixer.Sound('data/sound/bot or mites.mp3')
        self.doordown = pygame.mixer.Sound('data/sound/Doordown.mp3')
        self.elevator = pygame.mixer.Sound('data/sound/Doordown.mp3')
        self.floorcracking = pygame.mixer.Sound('data/sound/floorcracking.mp3')
        self.incorrect = pygame.mixer.Sound('data/sound/incorrect.mp3')
        self.items = pygame.mixer.Sound('data/sound/items.mp3')
        self.mite = pygame.mixer.Sound('data/sound/mite.mp3')
        self.mites = pygame.mixer.Sound('data/sound/mites.mp3')
        self.mites2 = pygame.mixer.Sound('data/sound/mites2.mp3')
        self.mites3 = pygame.mixer.Sound('data/sound/mites3.mp3')
        self.mites4 = pygame.mixer.Sound('data/sound/mites4.mp3')
        self.mites5 = pygame.mixer.Sound('data/sound/mites5.mp3')
        self.noise = pygame.mixer.Sound('data/sound/noise.mp3')
        self.rain = pygame.mixer.Sound('data/sound/rain.mp3')
        self.robot_moving = pygame.mixer.Sound('data/sound/robot_moving.mp3')
        self.robot = pygame.mixer.Sound('data/sound/robot.mp3')
        self.robot1 = pygame.mixer.Sound('data/sound/robot1.wav')
        self.robot2 = pygame.mixer.Sound('data/sound/robot2.wav')
        self.robot3 = pygame.mixer.Sound('data/sound/robot3.wav')
        self.robot4 = pygame.mixer.Sound('data/sound/robot4.wav')
        self.robot5 = pygame.mixer.Sound('data/sound/robot5.wav')
        self.robot6 = pygame.mixer.Sound('data/sound/robot6.wav')
        self.robot7 = pygame.mixer.Sound('data/sound/robot7.mp3')
        self.robots = pygame.mixer.Sound('data/sound/robots.mp3')
        self.shop = pygame.mixer.Sound('data/sound/shop.wav')
        self.walk = pygame.mixer.Sound('data/sound/walk.wav')
        self.wind = pygame.mixer.Sound('data/sound/wind.mp3')



        self.noise_blank=['data/sounds/rain.mp3',
                        'data/sounds/wind.mp3',
                        'data/sounds/floorcracking.mp3',
                         #a compléter...
        ]
        self.robot=['data/sounds/robot.mp3',
                    'data/sounds/robot1.wav',
                    'data/sounds/robot2.wav',
                    'data/sounds/robot3.wav',
                    'data/sounds/robot4.wav',
                    'data/sounds/robot5.wav',
                    'data/sounds/robot6.wav',
                    'data/sounds/robot7.mp3',
                    'data/sounds/robots.mp3''a']

    def potential_background(self):
        a=randint(0,100)
        if a==69:
            return randint(0, len(self.noise_blank))
        return False

    def sound_dialogue(self):
        a=randint(0, len(self.robot))
        return SoundManager(self.robot[a]).played()