import pygame as pg
import sys
from enum import Enum, auto

pg.init()

# Set up the display window with specified resolution
WIN = pg.display.set_mode((0,0),pg.FULLSCREEN)
CLOCK = pg.time.Clock()

from objects.placeable import Placeable
import objects.placeablesubclass as subplaceable
from utils.anim import Animation
from objects.pattern import Pattern
from objects.canva import Canva
from objects.bot import Hivemind, BotDistributor
from core.buildmode import BuildMode, DestructionMode
from utils.coord import Coord
from ui.inventory import Inventory
from objects.pattern_inv import PatternInv
from ui.popup import Popup
from room_config import R0, R1, ROOMS
from utils.timermanager import TimerManager
import ui.sprite as sprite
from objects.dialogue import Dialogue
from math import pi

def render_popups():  
    global popups
    # Iterate over existing popups to render and manage their lifetime
    for popup in popups:
        if popup.lifetime <= 0:
            popups.remove(popup)  # Remove expired popups
        else:
            popup.draw(WIN)  # Render the popup on the window
            popup.lifetime -= 1  # Decrement popup's lifetime

class State(Enum):
    INTERACTION = auto()
    BUILD = auto()
    DESTRUCTION = auto()
    INVENTORY = auto()
    PAINTING = auto()
    PLACING_PATTERN = auto()
    DIALOG = auto()
    TRANSITION = auto()

TIMER = TimerManager()

current_room = R1  # Initialize the current room to R1
gui_state = State.INTERACTION  # Start with the interaction GUI state
popups: list[Popup] = []  # List to manage popups

incr_fondu = 0  # Variable for transition effects

# Initialize Hivemind instance to manage bots
hivemind = Hivemind(60, 600, TIMER)
anim = Animation(sprite.SPRITESHEET_BOT, 0, 7)

# Initialize inventory and add placeable items
inventory: Inventory = Inventory()
inventory.inv.append(Placeable('6545dqw231', Coord(1, (121, 50)), sprite.P3))
inventory.inv.append(Placeable('6545dqwz31', Coord(1, (121, 50)), sprite.PROP_STATUE, tag="decoration", y_constraint=620))

p_list = sprite.PATTERN_LIST  # Pattern list for painting
pattern_inventory: PatternInv = PatternInv(p_list)  # Pattern inventory instance

# Instantiate build and destruction modes
build_mode: BuildMode = BuildMode()
destruction_mode: DestructionMode = DestructionMode()

#Test implementation of the dialogue class (to be integrated later)
test = Dialogue('data\dialogue.txt')
test.load_save()
dialoguet2 = Dialogue('data\dialogue_t2.txt')
dialoguet2.load_save()

#tests 'temporary'
bot_distributor = BotDistributor()
TIMER.create_timer(0.25, bot_distributor.add_to_theorical_gold, True)
TIMER.create_timer(1, bot_distributor.distribute_to_bot, True, [TIMER, hivemind], repeat_time_interval=[0.75,3])


# Initialize the painting canvas
test_painting = Canva()
filtre = pg.Surface((1920, 1080))  # Surface for effects
filtre.fill((0, 0, 0))  # Fill with black
filtre.set_alpha(0)  # Set initial transparency to 0

moulaga = 0  # Currency variable
money_per_robot = 10  # Rewards per robot

def go_up_one_floor():
    global current_room, ROOMS
    current_room = ROOMS[current_room.num + 1]  # Move to the next floor/room

def go_down_one_floor():
    global current_room, ROOMS
    current_room = ROOMS[current_room.num - 1]  # Move to the previous floor/room


def launch_dialogue(bot_sprite):
    """# Function to initiate dialogue easily passed to other functions"""
    global gui_state, test
    gui_state = State.DIALOG
    test.random_dialogue()  # Trigger a random dialogue
    test.bot_surf = bot_sprite.copy()  # Copy the bot's surface for display


def launch_transition():
    global gui_state, incr_fondu
    gui_state = State.TRANSITION  # Set the GUI to the transition state
    incr_fondu = 0  # Reset the transition variable

if __name__ == '__main__':
    fps = 60  # Frame rate
    while True:
        CLOCK.tick(fps)  # Maintain frame rate
        WIN.blit(current_room.bg_surf, (0, 0))  # Draw the background of the current room
        mouse_x, mouse_y = pg.mouse.get_pos()  # Get mouse position
        mouse_pos: Coord = Coord(current_room.num, pg.mouse.get_pos())  # Create a coordinate object for the mouse position
        clicked = False  # Track if a mouse button was clicked
        events = pg.event.get()  # Get all events from the event queue
        keys = pg.key.get_pressed()  # Get the current state of all keyboard keys

        for event in events:
            if event.type == pg.QUIT:  # Check for quit event
                pg.quit()  # Quit Pygame
                sys.exit()  # Exit the program

            if event.type == pg.KEYDOWN:  # Check for key down events
                match event.key:
                    case pg.K_SPACE:  # Spacebar to toggle between inventory and interaction
                        if gui_state is State.INTERACTION:
                            gui_state = State.INVENTORY  # Open inventory
                            inventory.open()
                        elif gui_state is State.INVENTORY:
                            gui_state = State.INTERACTION  # Return to interaction

                    case pg.K_BACKSPACE:  # Backspace to switch to destruction mode
                        if gui_state is State.INTERACTION:
                            gui_state = State.DESTRUCTION
                        else:
                            gui_state = State.INTERACTION  # Return to interaction

                    case pg.K_UP:  # Move up a floor
                        if current_room.num + 1 < len(ROOMS):
                            # Exit painting mode when moving up from room R0
                            if current_room == R0:
                                gui_state = State.INTERACTION

                            go_up_one_floor()  # Move to the next room
                        else:
                            popups.append(Popup("you can't go up anymore"))  # Show popup if trying to go above limits

                    case pg.K_DOWN:  # Move down a floor
                        if current_room.num - 1 >= 0:
                            go_down_one_floor()  # Move to the previous room

                            # Enter painting mode when moving down to room R0
                            if current_room == R0:
                                gui_state = State.PAINTING
                        else:
                            popups.append(Popup("you can't go down anymore"))  # Show popup if trying to go below limits

                    case pg.K_b:  # Add a bot
                        hivemind.add_bot()

                    case pg.K_n:  # Free the last bot in the current room
                        hivemind.free_last_bot(current_room)

                    case pg.K_LEFTBRACKET:  # Decrease FPS
                        fps -= 5  
                    case pg.K_RIGHTBRACKET:  # Increase FPS
                        fps += 5  

            if event.type == pg.MOUSEBUTTONUP:  # Handle mouse button release
                clicked = True
                # Handle interactions based on the current GUI state
                match gui_state:
                    case State.BUILD:
                        if build_mode.can_place(current_room):
                            current_room.placed.append(
                                build_mode.place(current_room.num))  # Place the object in the current room
                            gui_state = State.INTERACTION  # Return to interaction mode

                    case State.INVENTORY:
                        clicked_showed_obj_id = inventory.select_item(mouse_pos)  # Check if an inventory item was clicked
                        if clicked_showed_obj_id:
                            clicked_obj = inventory.search_by_id(
                                clicked_showed_obj_id)  # Retrieve the object by its ID

                            # Check if the object is already placed
                            if not clicked_obj.placed:
                                # Prepare to enter build mode with the selected placeable
                                build_mode.selected_placeable = clicked_obj
                                gui_state = State.BUILD

                    case State.DESTRUCTION:
                        for placeable in current_room.placed:
                            if placeable.rect.collidepoint(mouse_pos.x, mouse_pos.y):
                                destruction_mode.remove_from_room(
                                    placeable, current_room)  # Remove the selected placeable from the room

                    case State.INTERACTION:
                        for placeable in current_room.placed:
                            if placeable.rect.collidepoint(mouse_pos.x, mouse_pos.y):  # Check if mouse is over a placeable
                                match type(placeable):
                                    case subplaceable.DoorDown:  # Handle interaction with DoorDown type
                                       # fondu(filtre,1000) # [Warning]
                                        TIMER.create_timer(0.75, go_down_one_floor)  # Create a timer to move down
                                        launch_transition()  # Start transition
                                        placeable.interaction(TIMER)  # Trigger interaction

                                    case subplaceable.DoorUp:  # Handle interaction with DoorUp type
                                        TIMER.create_timer(0.75, go_up_one_floor)  # Create a timer to move up
                                        launch_transition()  # Start transition
                                        placeable.interaction(TIMER)  # Trigger interaction

                                    case subplaceable.BotPlaceable:  # Handle interaction with BotPlaceable type
                                        if placeable.name == 'bot_placeable':
                                            hivemind.free_last_bot(current_room)  # Free the last bot
                                            moulaga += money_per_robot  # Increment currency

                                    case _:
                                        popups.append(
                                            Popup('bip boup erreur erreur'))  # Add error popup if matching type fails
                                        
                    case State.DIALOG:
                        gui_state = State.INTERACTION  # Return to interaction mode after dialog

                    case State.PAINTING:  # Handle painting mode
                        pattern = Pattern(pattern_inventory.select_pattern(mouse_pos), [(0, 0, 0)])  # Select pattern based on mouse position
                        if pattern != None:
                            gui_state = State.PLACING_PATTERN  # Move to pattern placing state

                    case State.PLACING_PATTERN:
                        if test_painting.rect.collidepoint(mouse_pos.xy):  # Check if mouse is over the painting area
                            pattern.paint(Coord(666, (mouse_pos.x, mouse_pos.y)), test_painting)  # Paint the selected pattern at mouse position
                            gui_state = State.PAINTING  # Return to painting mode

        # Update timers
        TIMER.update()

        # Iterate through the placed objects in the current room
        for placeable in current_room.placed:
            # If the mouse is hovering over it
            if placeable.rect.collidepoint(mouse_pos.xy):
                color = (150, 150, 255) if gui_state != State.DESTRUCTION else (255, 0, 0)  # Change color based on state
                placeable.update_sprite(True, color)  # Update sprite to indicate hover
            # If not hovered
            else:
                placeable.update_sprite(False)  # Reset sprite

        # Draw all placed objects in the current room
        current_room.draw_placed(WIN)

        # FPS counter and GUI state debug display
        WIN.blit(Popup(
            f'gui state : {gui_state} / fps : {round(CLOCK.get_fps())} / mouse : {mouse_pos.xy} / $ : {moulaga}').text_surf, (0, 0))
        inventory.draw(WIN, mouse_pos, gui_state == State.INVENTORY)  # Draw inventory

        # Manage bot behavior
        hivemind.order_inline_bots()  # Arrange bots in a line
        hivemind.update_bots_ai(ROOMS, TIMER, clicked, mouse_pos, launch_dialogue)  # Update bot AI
        hivemind.draw(WIN, current_room_num=current_room.num)  # Draw bots in the current room

        # Handle GUI state specific drawing
        match gui_state:
            case State.BUILD:
                mouse_pos_coord = Coord(current_room.num, (mouse_x - build_mode.get_width() // 2, mouse_y - build_mode.get_height() // 2))  # Center the mouse on the hologram
                build_mode.show_hologram(WIN, mouse_pos_coord)  # Show the hologram for placing

                build_mode.show_room_holograms(WIN, current_room)  # Show room holograms

            case w if w in (State.PAINTING, State.PLACING_PATTERN):
                pattern_inventory.draw(WIN)  # Draw the pattern inventory
                test_painting.draw(WIN)  # Draw the painting canvas
            
            case State.INTERACTION:
                hivemind.create_last_bot_clickable()  # Make the last bot clickable
            
            case State.DIALOG:
                pg.transform.grayscale(WIN, WIN)  # Apply grayscale effect on the window
                
                test.show(WIN)  # Show dialogue on screen
            
            case State.TRANSITION:
                if incr_fondu <= pi:
                    incr_fondu = sprite.fondu(WIN, incr_fondu, 0.0125)  # Manage transition effect
                else:
                    gui_state = State.INTERACTION  # Return to interaction state after transition

        # Render popups after all other drawings
        render_popups()

        pg.display.flip()  # Update the display
