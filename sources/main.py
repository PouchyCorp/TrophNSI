import pygame as pg
import sys
from enum import Enum, auto

pg.init()

WIN = pg.display.set_mode((1920, 1080))
CLOCK = pg.time.Clock()

from objects.placeable import Placeable
import objects.placeablesubclass as subplaceable
from objects.anim import Animation
from objects.chip import Chip
from objects.canva import Canva
from objects.bot import Hivemind
from objects.build_mode import BuildMode, DestructionMode
from objects.coord import Coord
from objects.inventory import Inventory
from sources.objects.chipInv import ChipInv
from objects.popup import Popup
from room_config import R0, R1, R2, R3, ROOMS
from objects.timermanager import _Timer_manager
import objects.sprite as sprite


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

TIMER = _Timer_manager()

current_room = R1
gui_state = State.INTERACTION
popups: list[Popup] = []

# test hivemind
hivemind = Hivemind(60, 600)
anim = Animation(sprite.SPRITESHEET_BOT, 0, 7)

inventory: Inventory = Inventory()
inventory.inv.append(Placeable('6545dqw231',Coord(1,(121,50)), sprite.P3))
inventory.inv.append(Placeable('6545dqwz31',Coord(1,(121,50)), sprite.PROP_STATUE, tag= "decoration",y_constraint= 620))

chip_inventory : ChipInv = ChipInv()

build_mode: BuildMode = BuildMode()
destruction_mode: DestructionMode = DestructionMode()

test_painting = Canva()

moulaga = 0
money_per_robot = 10

if __name__ == '__main__':
    while True:
        CLOCK.tick(60)
        WIN.blit(current_room.bg_surf, (0, 0))
        mouse_x, mouse_y = pg.mouse.get_pos()
        mouse_pos: Coord = Coord(current_room.num, pg.mouse.get_pos())

                    
                    
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
                        elif gui_state is State.INVENTORY:
                            gui_state = State.INTERACTION

                    case pg.K_BACKSPACE:
                        if gui_state is State.INTERACTION:
                            gui_state = State.DESTRUCTION
                        else:
                            gui_state = State.INTERACTION

                    case pg.K_UP:
                        if current_room.num+1 < len(ROOMS): 
                            # exit painting mode
                            if current_room == R0:
                                gui_state = State.INTERACTION

                            current_room = ROOMS[current_room.num+1]
                        else:
                            popups.append(Popup("you can't go up anymore"))

                    case pg.K_DOWN:
                        if current_room.num-1 >= 0: 
                            current_room = ROOMS[current_room.num-1]

                            # enter painting mode
                            if current_room == R0:
                                gui_state = State.PAINTING
                        else:
                            popups.append(Popup("you can't go down anymore"))
                    case pg.K_b:
                        hivemind.add_bot()

                    case pg.K_n:
                        hivemind.free_last_bot()

            if event.type == pg.MOUSEBUTTONUP:

                # to keep before the inventory click check
                match gui_state:
                    case State.BUILD:
                        if build_mode.can_place(current_room):
                            current_room.placed.append(
                                build_mode.place(current_room.num))
                            gui_state = State.INTERACTION

                    case State.INVENTORY:
                        clicked_showed_obj_id = inventory.select_item(mouse_pos)
                        if clicked_showed_obj_id:
                            clicked_obj = inventory.search_by_id(
                                clicked_showed_obj_id)

                            # check if object already placed
                            if not clicked_obj.placed:
                                # enter build mode
                                build_mode.selected_placeable = clicked_obj
                                gui_state = State.BUILD

                    case State.DESTRUCTION:
                        for placeable in current_room.placed:
                            if placeable.rect.collidepoint(mouse_pos.x, mouse_pos.y):
                                destruction_mode.remove_from_room(
                                    placeable, current_room)

                    case State.INTERACTION:
                        for placeable in current_room.placed:
                            if placeable.rect.collidepoint(mouse_pos.x, mouse_pos.y):
                                match placeable.name:
                                    case 'R1_stairs':
                                        current_room = R2
                                    case 'R2_stairs':
                                        current_room = R3
                                    case 'R2_stairs_down':
                                        current_room = R1
                                    case 'R1_stairs_down':
                                        current_room = R0
                                    case 'bot_placeable':
                                        hivemind.free_last_bot()
                                        moulaga += money_per_robot
                                        current_room.placed.remove(placeable)
                                        current_room.blacklist.remove(placeable)
                                    case _:
                                        popups.append(
                                            Popup('bip boup erreur erreur'))

                    case State.PAINTING:
                        chip = Chip(chip_inventory.select_chip(mouse_pos),["black"])
                        if chip != None:
                            gui_state = State.PLACING_CHIP

                    case State.PLACING_CHIP:
                        if test_painting.rect.collidepoint(mouse_pos.xy):
                            chip.draw(WIN)
                            chip.paint(Coord(666,(mouse_pos.x,mouse_pos.y)),test_painting)
                            gui_state = State.PAINTING
                            chip = None
        #timer update
        TIMER.update()
        #print(TIMER.timers)

        #placeable iter
        for placeable in current_room.placed:
            if placeable.rect.collidepoint(mouse_pos.xy):
                color = (150, 150, 255) if gui_state != State.DESTRUCTION else (255, 0, 0)
                
                if type(placeable) in [subplaceable.Door_up, subplaceable.Door_down] and placeable.anim_close.is_finished():
                    placeable.anim = placeable.anim_open
                    placeable.anim_close.reset_frame()

                placeable.draw_outline(WIN, color)


            elif type(placeable) in [subplaceable.Door_up, subplaceable.Door_down] and placeable.anim_open.is_finished():
                placeable.anim = placeable.anim_close
                placeable.anim_open.reset_frame()


        # fps counter / state debug
        WIN.blit(Popup(
            f'gui state : {gui_state} / fps : {round(CLOCK.get_fps())} / mouse : {mouse_pos.xy} / $ : {moulaga}').text_surf, (0, 0))
        inventory.draw(WIN, mouse_pos, gui_state == State.INVENTORY)
        # use blits because more performant
        current_room.draw_placed(WIN)


        match gui_state:
            case State.BUILD:
                mouse_pos_coord = Coord(current_room.num, (mouse_x - build_mode.get_width() // 2, mouse_y - build_mode.get_height() // 2))
                build_mode.show_hologram(WIN, mouse_pos_coord)

                build_mode.show_room_holograms(WIN, current_room)

            case w if w in (State.PAINTING, State.PLACING_CHIP):
                chip_inventory.draw(WIN)
                test_painting.draw(WIN)
            
            case State.INTERACTION:
                hivemind.create_last_bot_clickable()

        hivemind.order_inline_bots()
        hivemind.update_bots_ai(ROOMS, TIMER)
        hivemind.draw(WIN, current_room_num=current_room.num)


        # drawed last
        render_popups()
        pg.display.flip()
