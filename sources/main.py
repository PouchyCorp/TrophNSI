import pygame as pg
import sys
from objects.placeable import Placeable
from objects.coord import Coord

WIN = pg.display.set_mode((1920,1080))
CLOCK = pg.time.Clock()

def draw_grid():
    for x in range(320):
        for y in range(180):
            if x%2 == 0 and y%2 != 0:
                pg.draw.rect(WIN,(70,70,70),pg.Rect(x*6,y*6,6,6))
            elif x%2 != 0 and y%2 == 0:
                pg.draw.rect(WIN,(70,70,70),pg.Rect(x*6,y*6,6,6))

placeable_lst = [Placeable('placeholder', Coord(1,(600,600)),pg.Surface((50,100),masks='red'))]

while True:

    CLOCK.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.MOUSEBUTTONUP:
            pos = pg.mouse.get_pos()
            for placeable in placeable_lst:
                if placeable.rect.collidepoint(pos[0],pos[1]):
                    print('uwu')


    WIN.fill((50,50,50))
    draw_grid()
    WIN.blits([(placeable.surf, placeable.coord.xy) for placeable in placeable_lst])
    
    pg.display.flip()
