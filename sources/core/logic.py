from enum import Enum, auto
import pygame as pg
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
from room_config import R0, R1, ROOMS, Room
from utils.timermanager import TimerManager
import ui.sprite as sprite
from objects.dialogue import DialogueManager
from math import pi
class State(Enum):
    INTERACTION = auto()
    BUILD = auto()
    DESTRUCTION = auto()
    INVENTORY = auto()
    PAINTING = auto()
    PLACING_PATTERN = auto()
    DIALOG = auto()
    TRANSITION = auto()

class Game:
    def __init__(self, win, clock, timer, hivemind, inventory, build_mode, destruction_mode, bot_distributor, dialogue_manager, gold):
        self.timer : TimerManager = timer
        self.win : pg.Surface = win
        self.clock : pg.Clock = clock
        self.popups : list[Popup] = []
        self.gui_state = State.INTERACTION
        self.hivemind : Hivemind = hivemind
        self.inventory : Inventory = inventory
        self.build_mode : BuildMode= build_mode
        self.destruction_mode : DestructionMode= destruction_mode
        self.bot_distributor : BotDistributor = bot_distributor
        self.dialogue_manager : DialogueManager = dialogue_manager
        self.current_room : Room = R1
        self.incr_fondu = 0
        self.clicked_this_frame = False
        self.gold : int = gold
    
    def change_floor(self, direction):
        """to move up : 1
           to move down : -1"""
        if self.current_room.num + direction >= 0:
            self.current_room = ROOMS[self.current_room.num + direction]  # Move to the previous room

            # Enter painting mode when moving down to room R0
            if self.current_room == R0:
                self.gui_state = State.PAINTING
        else:
            self.popups.append(Popup("you can't go off limits"))  # Show popup if trying to go below limits

    def launch_dialogue(self, bot_sprite):
        """# Function to initiate dialogue easily passed to other functions"""
        self.gui_state = State.DIALOG
        self.dialogue_manager.random_dialogue()  # Trigger a random dialogue
        self.dialogue_manager.bot_surf = bot_sprite.copy()  # Copy the bot's surface for display


    def launch_transition(self):
        self.gui_state = State.TRANSITION  # Set the GUI to the transition state
        self.incr_fondu = 0  # Reset the transition variable
    
    def render_popups(self):  
        # Iterate over existing popups to render and manage their lifetime
        for popup in self.popups:
            if popup.lifetime <= 0:
                self.popups.remove(popup)  # Remove expired popups
            else:
                popup.draw(self.win)  # Render the popup on the window
                popup.lifetime -= 1  # Decrement popup's lifetime
    
    def keydown_handler(self, event : pg.event.Event):
        match event.key:
            case pg.K_SPACE:  # Spacebar to toggle between inventory and interaction
                if self.gui_state is State.INTERACTION:
                    self.gui_state = State.INVENTORY  # Open inventory
                    self.inventory.open()
                elif self.gui_state is State.INVENTORY:
                    self.gui_state = State.INTERACTION  # Return to interaction

            case pg.K_BACKSPACE:  # Backspace to switch to destruction mode
                if self.gui_state is State.INTERACTION:
                    self.gui_state = State.DESTRUCTION
                else:
                    self.gui_state = State.INTERACTION  # Return to interaction

            case pg.K_UP:  # Move up a floor
                self.change_floor(1)

            case pg.K_DOWN:  # Move down a floor
                self.change_floor(-1)

            case pg.K_b:  # Add a bot
                self.hivemind.add_bot()

            case pg.K_n:  # Free the last bot in the current room
                self.hivemind.free_last_bot(self.current_room)

    def placeable_interaction_handler(self, placeable):
        match type(placeable):
            case subplaceable.DoorDown:  # Handle interaction with DoorDown type
                # fondu(filtre,1000) # [Warning]
                self.timer.create_timer(0.75, self.change_floor(-1))  # Create a timer to move down
                self.launch_transition()  # Start transition
                placeable.interaction(self.timer)  # Trigger interaction

            case subplaceable.DoorUp:  # Handle interaction with DoorUp type
                self.timer.create_timer(0.75, self.change_floor(1))  # Create a timer to move up
                self.launch_transition()  # Start transition
                placeable.interaction(self.timer)  # Trigger interaction

            case subplaceable.BotPlaceable:  # Handle interaction with BotPlaceable type
                if placeable.name == 'bot_placeable':
                    self.hivemind.free_last_bot(self.current_room)  # Free the last bot
                    self.gold += 10  # Increment currency

            case _:
                self.popups.append(
                    Popup('bip boup erreur erreur'))  # Add error popup if matching type fails


    def event_handler(self, event, mouse_pos):
            if event.type == pg.KEYDOWN:  # Check for key down events
                self.keydown_handler(event)

            if event.type == pg.MOUSEBUTTONUP:  # Handle mouse button release
                self.clicked_this_frame = True
                # Handle interactions based on the current GUI state
                match self.gui_state:
                    case State.BUILD:
                        if self.build_mode.can_place(self.current_room):
                            self.current_room.placed.append(
                                self.build_mode.place(self.current_room.num))  # Place the object in the current room
                            self.gui_state = State.INTERACTION  # Return to interaction mode

                    case State.INVENTORY:
                        clicked_showed_obj_id = self.inventory.select_item(mouse_pos)  # Check if an inventory item was clicked
                        if clicked_showed_obj_id:
                            clicked_obj = self.inventory.search_by_id(
                                clicked_showed_obj_id)  # Retrieve the object by its ID

                            # Check if the object is already placed
                            if not clicked_obj.placed:
                                # Prepare to enter build mode with the selected placeable
                                self.build_mode.selected_placeable = clicked_obj
                                self.gui_state = State.BUILD

                    case State.DESTRUCTION:
                        for placeable in self.current_room.placed:
                            if placeable.rect.collidepoint(mouse_pos.x, mouse_pos.y):
                                self.destruction_mode.remove_from_room(
                                    placeable, self.current_room)  # Remove the selected placeable from the room

                    case State.INTERACTION:
                        for placeable in self.current_room.placed:
                            if placeable.rect.collidepoint(mouse_pos.x, mouse_pos.y):  # Check if mouse is over a placeable
                                self.placeable_interaction_handler(placeable)
                                        
                    case State.DIALOG:
                        self.gui_state = State.INTERACTION  # Return to interaction mode after dialog when clicking
                    
    def update(self, mouse_pos):
        
        # Update timers
        self.timer.update()

        # Iterate through the placed objects in the current room
        for placeable in self.current_room.placed:
            # If the mouse is hovering over it
            if placeable.rect.collidepoint(mouse_pos.xy):
                color = (150, 150, 255) if self.gui_state != State.DESTRUCTION else (255, 0, 0)  # Change color based on state
                placeable.update_sprite(True, color)  # Update sprite to indicate hover
            # If not hovered
            else:
                placeable.update_sprite(False)  # Reset sprite


        # Manage bot behavior
        self.hivemind.order_inline_bots()  # Arrange bots in a line
        self.hivemind.update_bots_ai(ROOMS, self.timer, self.clicked_this_frame, mouse_pos, self.launch_dialogue)  # Update bot AI

        match self.gui_state:      
            case State.INTERACTION:
                self.hivemind.create_last_bot_clickable()  # Make the last bot clickable


    def draw(self, mouse_pos : Coord):
        self.win.blit(self.current_room.bg_surf, (0, 0))  # Draw the background of the current room
        # Draw all placed objects in the current room
        self.current_room.draw_placed(self.win)

        self.hivemind.draw(self.win, current_room_num=self.current_room.num)  # Draw bots in the current room

        match self.gui_state:
            case State.BUILD:
                mouse_pos_coord = Coord(self.current_room.num, (mouse_pos.x - self.build_mode.get_width() // 2, mouse_pos.y - self.build_mode.get_height() // 2))  # Center the mouse on the hologram
                self.build_mode.show_hologram(self.win, mouse_pos_coord)  # Show the hologram for placing

                self.build_mode.show_room_holograms(self.win, self.current_room)  # Show room holograms

    #        case w if w in (State.PAINTING, State.PLACING_PATTERN):
    #            pattern_inventory.draw(WIN)  # Draw the pattern inventory
    #            test_painting.draw(WIN)  # Draw the painting canvas
            
            case State.DIALOG:
                pg.transform.grayscale(self.win, self.win)  # Apply grayscale effect on the window
                
                self.dialogue_manager.show(self.win)  # Show dialogue on screen
            
            case State.TRANSITION:
                if self.incr_fondu <= pi:
                    self.incr_fondu = sprite.fondu(self.win, self.incr_fondu, 0.0125)  # Manage transition effect
                else:
                    self.gui_state = State.INTERACTION  # Return to interaction state after transition
            
        self.win.blit(Popup(
            f'gui state : {self.gui_state} / fps : {round(self.clock.get_fps())} / mouse : {mouse_pos.xy} / $ : flop').text_surf, (0, 0))
        self.inventory.draw(self.win, mouse_pos, self.gui_state == State.INVENTORY)  # Draw inventory
        
        # Render popups after all other drawings
        self.render_popups()
