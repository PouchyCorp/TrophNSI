import pygame as pg
import sys
import time
from enum import Enum, auto

pg.init()

WIN = pg.display.set_mode((1920, 1080))
CLOCK = pg.time.Clock()

import objects.sprite as sprite
from room_config import R0, R1, R2, R3
from objects.popup import Popup
from objects.placeable import Placeable
from objects.inventory import Inventory
from objects.coord import Coord
from objects.build_mode import Build_mode, Destruction_mode
from objects.bot import Bot, Hivemind
from objects.canva import Painting
from objects.chip import Chip


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


class State(Enum):
    INTERACTION = auto()
    BUILD = auto()
    DESTRUCTION = auto()
    INVENTORY = auto()
    PAINTING = auto()
    PLACING_CHIP = auto()



current_room = R1
gui_state = State.INTERACTION
popups : list[Popup] = []

#test hivemind
hivemind = Hivemind(60,1200)
hivemind.add_bot()

inventory : Inventory = Inventory()
#inventory.inv.append(Placeable('654564231',Coord(1,(121,50)), sprite.P1))
#inventory.inv.append(Placeable('6545dqw231',Coord(1,(121,50)), sprite.P2))
inventory.inv.append(Placeable('6gqeeqd4231',Coord(1,(121,50)), sprite.P3, 600))

build_mode : Build_mode = Build_mode()
destruction_mode : Destruction_mode = Destruction_mode()

test_painting = Painting()
test_surf = pg.Surface((100,100))
test_surf.fill("blue")

if __name__ == '__main__':
    while True:
        CLOCK.tick (30)
        WIN.blit(current_room.bg_surf, (0,0))
        mouse_pos : Coord = Coord(current_room.num , pg.mouse.get_pos())

        for placeable in current_room.placed:
            if placeable.rect.collidepoint(mouse_pos.xy):
                color = (150,150,255) if not destruction_mode.in_destruction_mode else (255,0,0)
                placeable.draw_outline(WIN, color)
        
        events = pg.event.get()
        keys = pg.key.get_pressed()

        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_SPACE:
                        if gui_state is State.INTERACTION:
                            gui_state = State.INVENTORY
                            inventory.open()
                        else:
                            gui_state = State.INTERACTION

                    case pg.K_BACKSPACE:
                        if gui_state is State.INTERACTION:
                            gui_state = State.DESTRUCTION
                        else:
                            gui_state = State.INTERACTION

                    case pg.K_UP:
                        try:
                            #exit painting mode
                            if current_room == R0:
                                gui_state = State.INTERACTION

                            current_room = eval('R'+str(current_room.num+1))
                        except:
                            popups.append(Popup("you can't go up anymore"))

                    case pg.K_UP:
                        try:
                            #exit painting mode
                            if current_room == R0:
                                gui_state = State.INTERACTION

                            current_room = eval('R'+str(current_room.num+1))
                        except:
                            popups.append(Popup("you can't go up anymore"))

                    case pg.K_DOWN:
                        try:
                            current_room = eval('R'+str(current_room.num-1))
                            
                            #enter painting mode
                            if current_room == R0:
                                gui_state = State.PAINTING
                        except:
                            popups.append(Popup("you can't go down anymore"))

                    case pg.K_RIGHT:
                        if gui_state == State.PAINTING:
                            gui_state = State.INTERACTION
                    
                    case pg.K_b:
                        hivemind.add_bot()
                    
                    case pg.K_n:
                        hivemind.free_last_bot()

            if event.type == pg.MOUSEBUTTONUP:
                
                #to keep before the inventory click check
                match gui_state:
                    case State.BUILD:
                        if build_mode.can_place(current_room):
                            current_room.placed.append(build_mode.place(current_room.num))
                            gui_state = State.INTERACTION

                    case State.INVENTORY:
                        clicked_obj_name = inventory.select_item(mouse_pos)
                        if clicked_obj_name:
                            clicked_obj = inventory.search_by_name(clicked_obj_name) 
                            
                            #check if object already placed
                            if not clicked_obj.placed:

                                #enter build mode
                                build_mode.selected_placeable = clicked_obj
                                gui_state = State.BUILD
                                

                    case State.DESTRUCTION:
                        for placeable in current_room.placed:
                            if placeable.rect.collidepoint(mouse_pos.x, mouse_pos.y):
                                destruction_mode.remove_from_room(placeable, current_room)
                
                    case State.INTERACTION:
                        for placeable in current_room.placed:
                            if placeable.rect.collidepoint(mouse_pos.x, mouse_pos.y):
                                match placeable.name:
                                    case 'R1_stairs':
                                        current_room = R2
                                    case 'R2_stairs':
                                        current_room = R3
                                    case _:
                                        popups.append(Popup('bip boup erreur erreur'))
                    
                    case State.PAINTING:
                        if 500 <= mouse_pos.x <= 600 and 400 <= mouse_pos.y <= 500:
                            gui_state = State.PLACING_CHIP

                    
                    case State.PLACING_CHIP:
                        if test_painting.coord.x <= mouse_pos.x <= test_painting.coord.x+576 and test_painting.coord.y <= mouse_pos.y <= test_painting.coord.y+768:
                            ch = Chip([["#000000" for k in range(4)] for k in range(4)])
                            ch.paint(Coord(666,(mouse_pos.x-test_painting.coord.x, mouse_pos.y-test_painting.coord.y)),test_painting,WIN)
                            gui_state = State.PAINTING 

        #cntr = time.time()
 
        #fps counter / state debug
        WIN.blit(Popup(f'gui state : {gui_state} / fps : {round(CLOCK.get_fps())}').text_surf,(0,0))

        inventory.draw(WIN, mouse_pos, gui_state == State.INVENTORY)
        #use blits because more performant
        current_room.draw_placed(WIN)

        if gui_state is State.BUILD:
            build_mode.show_hologram(WIN, mouse_pos)
            build_mode.show_room_holograms(WIN, current_room)
        
        if gui_state is State.PAINTING or gui_state is State.PLACING_CHIP:
            test_painting.draw(WIN)
            WIN.blit(test_surf,(500,400))

        #temporary test
        #WIN.blit(sprite.ROUNDED_WINDOW_TEST, (500, 500))

        hivemind.order_bots()
        hivemind.update_bot_orders()
        hivemind.draw(WIN)

        #drawed last
        render_popups()
        pg.display.flip()

        #print(time.time()-cntr)