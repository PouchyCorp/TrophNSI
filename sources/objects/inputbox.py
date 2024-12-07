import pygame as pg

class Inputbox:

    def __init__(self):
        self.rect = pg.Rect(100,80,120,20)
        self.txt = ''
        self.font = pg.font.SysFont('Silkscreen',30,0)
        self.txt_surf = self.font.render(self.txt, True, pg.Color('black'))
    
    def write(self,event,inv,canva):
        if event.type == pg.KEYDOWN : 

            if event.key == pg.K_RETURN:
                canva.save(self.txt,inv)
                self.txt = ''
                return False
            
            elif event.key == pg.K_BACKSPACE:
                self.txt = self.txt[:-1]

            else:
                self.txt += event.unicode
            self.txt_surf = self.font.render(self.txt, True, pg.Color('black'))
            return True

    def update(self):
        self.rect.w = max(180, self.txt_surf.get_rect().w)
    
    def draw(self,win):
        win.blit(self.txt_surf, (self.rect.x,self.rect.y))