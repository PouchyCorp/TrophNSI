import pygame as pg
import sys
import objects.placeable
from room_config import R0, R1, R2, R3
from objects.popup import Popup
from objects.placeable import Placeable
from objects.inventory import Inventory
from objects.coord import Coord

pg.init()

WIN = pg.display.set_mode((1920, 1080))
CLOCK = pg.time.Clock()

'''
def draw_grid():
    for x in range(320):
        for y in range(180):
            if x % 2 == 0 and y % 2 != 0:
                pg.draw.rect(WIN, (70, 70, 70), pg.Rect(x * 6, y * 6, 6, 6))
            elif x % 2 != 0 and y % 2 == 0:
                pg.draw.rect(WIN, (70, 70, 70), pg.Rect(x * 6, y * 6, 6, 6))
'''
                
def render_popups():
    global popups
    for popup in popups:
        if popup.lifetime <= 0:
            popups.remove(popup)
        else:
            popup.draw(WIN)
            popup.lifetime -= 1

if __name__ == '__main__':

    current_room = R1
    popups : list[Popup] = []
    inventory : Inventory = Inventory()
    inventory.lst.append(Placeable('1',Coord(1,(121,50)),pg.image.load('data/p1.png')))
    inventory.lst.append(Placeable('1',Coord(1,(121,50)),pg.image.load('data/p2.png')))
    inventory.lst.append(Placeable('1',Coord(1,(121,50)),pg.image.load('data/p3.png')))

    while True:
        CLOCK.tick (30)
        WIN.blit(current_room.bg_surf, (0,0))
        mouse_pos : Coord = Coord(current_room.num , pg.mouse.get_pos())

        for placeable in current_room.placed:
            if placeable.rect.collidepoint(mouse_pos.xy):
                placeable.draw_outline(WIN)
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            else:
                #to optimize if needed
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        
        events = pg.event.get()
        keys = pg.key.get_pressed()

        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    inventory.toggle()
                    print(inventory.opened)

            if event.type == pg.MOUSEBUTTONUP:
                for placeable in current_room.placed:
                    if placeable.rect.collidepoint(mouse_pos.x, mouse_pos.y):
                        match placeable.name:
                            case 'R1_stairs':
                                current_room = R2
                            case 'R2_stairs':
                                current_room = R3
                            case "test":
                                popups.append(Popup(str(CLOCK.get_fps())))
                            case _:
                                popups.append(Popup('bip boup erreur erreur'))
        
        #fps counter
        WIN.blit(Popup(str(round(CLOCK.get_fps()))).text_surf,(0,0))

        #use blits because more performant
        current_room.draw_placed(WIN)
        inventory.draw(WIN, mouse_pos)
        render_popups()

        pg.display.flip()
