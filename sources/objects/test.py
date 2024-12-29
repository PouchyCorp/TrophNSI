import pygame, sys
from pygame.locals import *

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

pygame.init()
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

def display_text_animation(string):
    text = ''
    for i in range(len(string)):
        DISPLAYSURF.fill(WHITE)
        text += string[i]
        text_rect = text_surface.get_rect()
        text_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        DISPLAYSURF.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.wait(100)

def main():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

display_text_animation('Hello World!')
main()