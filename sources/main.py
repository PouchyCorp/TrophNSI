import pygame as pg
import sys
from room_config import R1, R2, R3
from objects.popup import Popup

pg.init()

WIN = pg.display.set_mode((1920, 1080))
CLOCK = pg.time.Clock()



def draw_grid():
    for x in range(320):
        for y in range(180):
            if x % 2 == 0 and y % 2 != 0:
                pg.draw.rect(WIN, (70, 70, 70), pg.Rect(x * 6, y * 6, 6, 6))
            elif x % 2 != 0 and y % 2 == 0:
                pg.draw.rect(WIN, (70, 70, 70), pg.Rect(x * 6, y * 6, 6, 6))

def render_popups():
    global popups
    for popup in popups:
        if popup.lifetime <= 0:
            popups.remove(popup)
        else:
            popup.draw(WIN)
            popup.lifetime -= 1

current_room = R1
popups : list[Popup] = []

while True:
    CLOCK.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.MOUSEBUTTONUP:
            pos = pg.mouse.get_pos()
            for placeable in current_room.placed:
                if placeable.rect.collidepoint(pos[0], pos[1]):
                    match placeable.name:
                        case 'R1_stairs':
                            current_room = R2
                        case 'R2_stairs':
                            current_room = R3
                        case "test":
                            popups.append(Popup(str(CLOCK.get_fps())))
                        case _:
                            popups.append(Popup('bip boup erreur erreur'))
                            popup_active = True


    WIN.blit(current_room.bg_surf, (0,0))
    WIN.blits([(placeable.surf, placeable.coord.xy) for placeable in current_room.placed])
    render_popups()

    pg.display.flip()
