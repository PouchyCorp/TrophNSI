from enum import Enum, auto
class State(Enum):
    INTERACTION = auto()
    BUILD = auto()
    DESTRUCTION = auto()
    INVENTORY = auto()
    PAINTING = auto()
    PLACING_PATTERN = auto()
    DIALOG = auto()
    TRANSITION = auto()
    CONFIRMATION = auto()
    SHOP = auto()

import pygame as pg
import sys
import objects.placeablesubclass as subplaceable
from objects.bot import Hivemind, BotDistributor
from core.buildmode import BuildMode, DestructionMode
from utils.coord import Coord
from ui.inventory import Inventory, Shop
from ui.popup import InfoPopup
from room_config import R0, R1, ROOMS, Room
from utils.timermanager import TimerManager
import ui.sprite as sprite
from objects.dialogue_v2 import DialogueManagement
from math import pi
from objects.placeable import Placeable
from ui.confirmationpopup import ConfirmationPopup
from utils.sound import SoundManager
from core.unlockmanager import UnlockManager

class Game:
    def __init__(self, win, clock, inventory, shop, gold):
        self.timer : TimerManager = TimerManager()
        self.win : pg.Surface = win
        self.clock : pg.time.Clock = clock
        self.popups : list[InfoPopup] = []
        self.confirmation_popups : list[ConfirmationPopup] = []
        self.gui_state = State.INTERACTION
        self.hivemind : Hivemind = Hivemind(60, 600, self.timer)
        self.inventory : Inventory = inventory
        self.shop : Shop = shop
        self.build_mode : BuildMode= BuildMode()
        self.destruction_mode : DestructionMode= DestructionMode()
        self.bot_distributor : BotDistributor = BotDistributor(self.timer, self.hivemind, self)
        self.dialogue_manager : DialogueManagement = DialogueManagement('data/dialogue.json')
        self.current_room : Room = R1 #starter room always in floor 1
        self.incr_fondu = 0
        self.clicked_this_frame = False
        self.money : int = gold
        self.beauty : float = self.process_total_beauty()
        self.unlock_manager = UnlockManager()

    def change_floor(self, direction):
        """to move up : 1
           to move down : -1"""
        if self.current_room.num + direction >= 0:
            self.current_room = ROOMS[self.current_room.num + direction]  # Move to the previous room

            # Enter painting mode when moving down to room R0
            if self.current_room == R0:
                self.gui_state = State.PAINTING
        else:
            self.popups.append(InfoPopup("you can't go off limits"))  # Show popup if trying to go below limits

    def launch_dialogue(self, bot_anim):
        """# Function to initiate dialogue easily passed to other functions"""
        self.gui_state = State.DIALOG
        self.temp_bg =  pg.transform.grayscale(self.win)
        self.dialogue_manager.random_dialogue()  # Trigger a random dialogue
        self.dialogue_manager.bot_anim = bot_anim.copy()  # Copy the bot's surface for display
    
    def process_total_beauty(self):
        total = 0
        for room in ROOMS:
            total += room.get_beauty_in_room()
        return total


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
                    self.inventory.init()
                elif self.gui_state is State.INVENTORY:
                    self.gui_state = State.INTERACTION  # Return to interaction

            case pg.K_BACKSPACE:  # Backspace to switch to destruction mode
                if self.gui_state is State.INTERACTION:
                    self.gui_state = State.DESTRUCTION
                else:
                    self.gui_state = State.INTERACTION  # Return to interaction

            case pg.K_s:
                if self.gui_state is State.INTERACTION:
                    self.gui_state = State.SHOP  # Open inventory
                    self.shop.init()
                elif self.gui_state is State.SHOP:
                    self.gui_state = State.INTERACTION  # Return to interaction
            
            case pg.K_ESCAPE:
                if self.gui_state not in [State.TRANSITION, State.CONFIRMATION]:
                    self.gui_state = State.INTERACTION

            case pg.K_UP:  # Move up a floor
                self.change_floor(1)

            case pg.K_DOWN:  # Move down a floor
                self.change_floor(-1)

            case pg.K_b:  # Add a bot
                self.hivemind.add_bot()

            case pg.K_n:  # Free the last bot in the current room
                self.hivemind.free_last_bot(self.current_room)

    def placeable_interaction_handler(self, placeable : Placeable):
        match type(placeable):
            case subplaceable.DoorDown:  # Handle interaction with DoorDown type
                if self.unlock_manager.is_floor_unlocked(self.current_room.num-1):
                    self.timer.create_timer(0.75, self.change_floor, arguments=[-1])  # Create a timer to move down
                    self.launch_transition()  # Start transition
                    placeable.interaction(self.timer)  # Trigger interaction
                else:
                    self.unlock_manager.try_to_unlock_floor(self.current_room.num-1, self)
                

            case subplaceable.DoorUp:  # Handle interaction with DoorUp type
                if self.unlock_manager.is_floor_unlocked(self.current_room.num+1):
                    self.timer.create_timer(0.75, self.change_floor, arguments=[1]) # Create a timer to move up
                    up=SoundManager('data/sounds/elevator.wav')
                    up.played()
                    self.launch_transition()  # Start transition
                    placeable.interaction(self.timer)  # Trigger interaction
                self.unlock_manager.try_to_unlock_floor(self.current_room.num+1, self)

            case subplaceable.BotPlaceable:  # Handle interaction with BotPlaceable type
                if placeable.name == 'bot_placeable':
                    self.money += self.hivemind.inline_bots[-1].gold_amount  # Increment currency
                    self.hivemind.free_last_bot(self.current_room)  # Free the last bot
                    
            case subplaceable.ShopPlaceable:
                if self.gui_state is not State.SHOP:
                    self.gui_state = State.SHOP
                    self.shop.init()

            case subplaceable.InvPlaceable:
                if self.gui_state is not State.INVENTORY:
                    self.gui_state = State.INVENTORY
                    self.inventory.init()

            case _:
                self.popups.append(
                    InfoPopup('bip boup erreur erreur'))  # Add error popup if matching type fails


    def event_handler(self, event: pg.event.Event, mouse_pos: Coord):
        """
        Handle events such as key presses and mouse button releases.

        Args:
            event (pg.event.Event): The event to handle.
            mouse_pos (Coord): The current position of the mouse.

        Returns:
            None
        """
        self.clicked_this_frame = False  # If not supplanted below, set false for this frame 
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
                        self.beauty = self.process_total_beauty()
                        self.gui_state = State.INVENTORY  # Return to interaction mode
                        self.inventory.init() # Resets inventory gui

                case State.INVENTORY:
                    self.inventory.handle_navigation(event)
                    clicked_placeable : Placeable | None = self.inventory.handle_click(mouse_pos)
                    if clicked_placeable:
                        # Prepare to enter build mode with the selected placeable
                        self.build_mode.selected_placeable = clicked_placeable
                        self.gui_state = State.BUILD
                
                case State.SHOP:
                    self.shop.handle_click(mouse_pos, self)
                    

                case State.DESTRUCTION:
                    for placeable in self.current_room.placed:
                        if placeable.rect.collidepoint(mouse_pos.x, mouse_pos.y):
                            self.destruction_mode.remove_from_room(
                                placeable, self.current_room)  # Remove the selected placeable from the room
                            self.beauty = self.process_total_beauty()

                case State.INTERACTION:
                    for placeable in self.current_room.placed:
                        if placeable.rect.collidepoint(mouse_pos.x, mouse_pos.y):  # Check if mouse is over a placeable
                            self.placeable_interaction_handler(placeable)
                                    
                case State.DIALOG:
                    if self.dialogue_manager.click_interaction():
                        self.gui_state = State.INTERACTION
                
                case State.CONFIRMATION:
                    flag = self.confirmation_popups[-1].handle_click(mouse_pos)
                    if flag is not None:
                        self.confirmation_popups.pop()

                    if not len(self.confirmation_popups):
                        self.gui_state = State.INTERACTION
                               

    def update(self, mouse_pos):
        
        # Update timers
        self.timer.update()

        # Iterate through the placed objects in the current room
        for placeable in self.current_room.placed:
            # If the mouse is hovering over it
            if placeable.rect.collidepoint(mouse_pos.xy) and self.gui_state in [State.DESTRUCTION, State.INTERACTION]:
                color = (150, 150, 255) if self.gui_state != State.DESTRUCTION else (255, 0, 0)  # Change color based on state
                placeable.update_sprite(True, color)  # Update sprite to indicate hover
            # If not hovered
            else:
                placeable.update_sprite(False)  # Reset sprite


        # Manage bot behavior
        self.hivemind.order_inline_bots()  # Arrange bots in a line
        self.hivemind.update(ROOMS, self.timer, self.clicked_this_frame, mouse_pos, self.launch_dialogue, self.gui_state in [State.INTERACTION])  # Update bot AI

        match self.gui_state:      
            case State.INTERACTION:
                self.hivemind.create_last_bot_clickable()  # Make the last bot clickable

        
        if self.confirmation_popups:
            self.gui_state = State.CONFIRMATION


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
    #            test_painting.draw(WIN)  # Draw the painting 
            
            case State.DIALOG:
                self.win.blit(self.temp_bg, (0,0))  # Apply grayscale effect on the background
                self.dialogue_manager.update() #update the dialogue manager and it's subclasses
                self.dialogue_manager.draw(self.win)    

            case State.TRANSITION:
                if self.incr_fondu <= pi:
                    self.incr_fondu = sprite.fondu(self.win, self.incr_fondu, 0.0125)  # Manage transition effect
                else:
                    self.gui_state = State.INTERACTION  # Return to interaction state after transition
            
            case State.CONFIRMATION:
                if self.confirmation_popups:
                    self.confirmation_popups[-1].draw(mouse_pos)
            
            case State.INVENTORY:
                self.inventory.draw(self.win, mouse_pos)

            case State.SHOP:
                self.shop.draw(self.win, mouse_pos)

        self.win.blit(InfoPopup(
            f'gui state : {self.gui_state} / fps : {round(self.clock.get_fps())} / mouse : {mouse_pos.xy} / $ : {self.money} / th_gold : {self.bot_distributor.theorical_gold}').text_surf, (0, 0))
        
          # Draw inventory
        
        # Render popups after all other drawings
        self.render_popups()
