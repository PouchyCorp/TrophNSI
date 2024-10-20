import pygame as pg
pg.init()
class Pop_up:
    def __init__(self, text, coord, font, width=200, height=100):
        self.text = text
        self.coord = coord
        self.width = width
        self.height = height
        self.font = font

        
        self.posx,self.posy =self.coord.get_pixel_perfect()
        self.rect = pg.Rect(self.posx, self.posy, self.width, self.height)
        self.text = self.font.render(self.text, True, (0, 0, 0))

    def draw(self, screen):
        pg.draw.rect(screen, (200, 200, 200), self.rect)  #fond du popup


        text_rect = self.text.get_rect(center=self.rect.center)
        screen.blit(self.text, text_rect)
