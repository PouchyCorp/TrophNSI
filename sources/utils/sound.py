import pygame
import time
from random import *

class SoundManager():
    def __init__(self, name, time=0):
        self.name=name
        self.time=time
        

    def played(self):
        PLAYING=pygame.mixer.Sound(self.name)
        pygame.mixer.Sound.fadeout(150)
        PLAYING.play(1, self.time*1000)
        pygame.mixer.Sound.unload()

    
    
class Sound():
    def __init__(self):
        self.noise_blank=['data/sounds/rain.mp3',
                        'data/sounds/wind.mp3' #a compléter...
        ]
        self.robot=['data/sounds/robot.mp3',
                    'data/sounds/robot1.wav',
                    'data/sounds/robot2.wav',
                    'data/sounds/robot3.wav',
                    'data/sounds/robot4.wav',
                    'data/sounds/robot5.wav',
                    'data/sounds/robot6.wav',
                    'data/sounds/robot7.mp3',
                    'data/sounds/robots.mp3']

    def potential_background(self):
        a=randint(0,100)
        if a==69:
            return randint(0, len(self.noise_blank))
        return False

    def sound_dialogue(self):
        a=randint(0, len(self.robot))
        return SoundManager(self.robot[a]).played()