import pygame as pg
import sys
import time

pg.init()

WIN = pg.display.set_mode((1920, 1080))
CLOCK = pg.time.Clock()

import objects.sprite as sprite
from room_config import R0, R1, R2, R3
from objects.popup import Popup
from objects.placeable import Placeable
from objects.inventory import Inventory
from objects.coord import Coord
from objects.build_mode import Build_mode

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
    inventory.inv.append(Placeable('654564231',Coord(1,(121,50)), sprite.P1))
    inventory.inv.append(Placeable('6545dqw231',Coord(1,(121,50)), sprite.P2))
    inventory.inv.append(Placeable('6gqeeqd4231',Coord(1,(121,50)), sprite.P3))
    
    build_mode : Build_mode = Build_mode(Placeable('R1_stairs', Coord(1,(1000,300)), pg.transform.scale_by(pg.image.load("data/p3.png"),6)))
    #build_mode.in_build_mode = True

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
                match event.key:
                    case pg.K_SPACE:
                        inventory.toggle()
                    case pg.K_UP:
                        current_room = eval('R'+str(current_room.num+1))
                    case pg.K_DOWN:
                        current_room = eval('R'+str(current_room.num-1))

            if event.type == pg.MOUSEBUTTONUP:
                
                #to keep before the inventory click check
                if build_mode.in_build_mode:
                    current_room.placed.append(build_mode.place(mouse_pos))

                if inventory.is_open:
                    clicked_obj_name = inventory.select_item(mouse_pos)
                    if clicked_obj_name:
                        
                        clicked_obj = inventory.search_by_name(clicked_obj_name) 
                        build_mode.selected_placeable = clicked_obj

                        inventory.is_open = False
                        build_mode.in_build_mode = True

                for placeable in current_room.placed:
                    if placeable.rect.collidepoint(mouse_pos.x, mouse_pos.y) and not (build_mode.in_build_mode or inventory.is_open):
                        match placeable.name:
                            case 'R1_stairs':
                                current_room = R2
                            case 'R2_stairs':
                                current_room = R3
                            case "test":
                                popups.append(Popup(str(CLOCK.get_fps())))
                            case _:
                                popups.append(Popup('bip boup erreur erreur'))

        cntr = time.time()

        #fps counter
        WIN.blit(Popup(str(round(CLOCK.get_fps()))).text_surf,(0,0))

        
        #use blits because more performant
        current_room.draw_placed(WIN)

        inventory.draw(WIN, mouse_pos)

        if build_mode.in_build_mode:
            build_mode.show_hologram(WIN, mouse_pos)

        #drawed last
        render_popups()
        pg.display.flip()

        print(time.time()-cntr)