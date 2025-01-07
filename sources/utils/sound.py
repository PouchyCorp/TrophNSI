import pygame
import time

class SoundManager():
    def __init__(self, name, time = 0):
        self.name=name
        self.time=time

    def played(self):
        PLAYING=pygame.mixer.Sound(self.name)
        pygame.mixer.music.fadeout(150)
        PLAYING.play(1, self.time*1000)
        pygame.mixer.music.unload()

    def background(self):
        print('UwU')
