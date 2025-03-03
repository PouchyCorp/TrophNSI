r"""
                  _         _             _      
                 (_)       | |           (_)     
  _ __ ___   __ _ _ _ __   | | ___   __ _ _  ___ 
 | '_ ` _ \ / _` | | '_ \  | |/ _ \ / _` | |/ __|
 | | | | | | (_| | | | | | | | (_) | (_| | | (__ 
 |_| |_| |_|\__,_|_|_| |_| |_|\___/ \__, |_|\___|
                                     __/ |       
                                    |___/        

This game loop operates with a FSM (Finite State Machine), transitionning between states such as interaction,
building, destruction, inventory management, painting, placing patterns, dialogue, and shop navigation.

Each frame (60fps):
-------------
1. Event Handling: Processes player inputs to update the game state.
                            |
                            v
2. Update: Advances timers, updates AI behaviors, and refreshes objects based on the current state.
                            |
                            v
3. Rendering: Draws objects, UI elements, and overlays according to the active state.

Certain states, like confirmation prompts and transitions, override standard interactions."""

from enum import Enum, auto
class State(Enum):
    INTERACTION = auto()
    BUILD = auto()
    DESTRUCTION = auto()
    INVENTORY = auto()
    DIALOG = auto()
    TRANSITION = auto()
    CONFIRMATION = auto()
    SHOP = auto()
    PAUSED = auto()

import pygame as pg
import objects.placeablesubclass as subplaceable
from objects.bot import Hivemind, BotDistributor
from core.buildmode import BuildMode, DestructionMode
from utils.coord import Coord
from ui.inventory import Inventory, Shop
from ui.infopopup import InfoPopup
from  utils.room_config import R1, ROOMS, Room, PARTICLE_SPAWNERS
from utils.timermanager import TimerManager
import ui.sprite as sprite
from objects.dialogue import DialogueManager
from math import pi
from core.unlockmanager import UnlockManager
from objects.placeable import Placeable
from ui.confirmationpopup import ConfirmationPopup
from utils.sound import SoundManager
from objects.patterns import PatternHolder
from objects.canva import Canva
from ui.button import Button
from objects.particlesspawner import ParticleSpawner

class Game:
    def __init__(self, win : pg.Surface, config : dict, inventory, shop, gold, unlock_manager, transparency_win):
        self.config = config
        self.win : pg.Surface = win
        self.timer : TimerManager = TimerManager()

        # Loading backgound while the sounds and sprites load.
        self.win.blit(pg.image.load('data/loading_bg.png'),(0,0))
        pg.display.flip()
        self.transparency_win = transparency_win

        self.sound_manager = SoundManager(self.timer)
        self.clock : pg.time.Clock = pg.time.Clock()
        self.popups : list[InfoPopup] = []
        self.confirmation_popups : list[ConfirmationPopup] = [] # Stack of confirmation popups
        self.gui_state = State.INTERACTION
        self.hivemind : Hivemind = Hivemind(60, 600, self.timer, self.sound_manager)
        self.inventory : Inventory = Inventory(self.change_floor, self.reset_guistate, title= "Inventaire", content = inventory)
        self.shop : Shop = Shop(None, None, title= "Shop", content = shop)
        self.inventory.sound_manager = self.sound_manager
        self.shop.sound_manager = self.sound_manager
        self.build_mode : BuildMode= BuildMode()
        self.destruction_mode : DestructionMode= DestructionMode()
        self.bot_distributor : BotDistributor = BotDistributor(self.timer, self.hivemind, self)
        self.dialogue_manager : DialogueManager = DialogueManager()
        self.current_room : Room = R1 # Starter room always in floor 1.
        self.incr_fondu = 0
        self.money : int = gold
        self.beauty : float = self.process_total_beauty()
        self.unlock_manager : UnlockManager = unlock_manager
        self.canva : Canva = Canva(Coord(0,(621,30)), self)
        self.pattern_holder : PatternHolder = PatternHolder(Coord(0, (0, 0)), canva=self.canva)
        self.paused = False

        self.particle_spawners : dict[int,list] = PARTICLE_SPAWNERS

        # Initialize unlocks effects.
        if self.unlock_manager.is_feature_unlocked("Auto Cachier"):
            self.timer.create_timer(3, self.accept_bot, True)

        if not self.config['gameplay']['offline_mode']: # If the player is not in the no_login mode, don't init the spectating placeable
            self.spectating_placeable = subplaceable.SpectatorPlaceable('spectating_placeable', Coord(5,(100,100)), pg.Surface((100,100)), self.config)
            ROOMS[5].placed.append(self.spectating_placeable)
            ROOMS[5].blacklist.append(self.spectating_placeable)

        self.cachier_desk = [plbl for plbl in ROOMS[1].placed if type(plbl) == subplaceable.DeskPlaceable][0] # Very ugly indeed

    def change_floor(self, direction):
        """to move up : 1
           to move down : -1"""

        if 0 <= self.current_room.num + direction <= 5 and (self.unlock_manager.is_floor_unlocked(self.current_room.num + direction) or self.config['gameplay']['cheats']):

            self.current_room = ROOMS[self.current_room.num + direction]  # Move to the previous room
            # Checks if floor already visited and launches dialogue if not
            if not self.unlock_manager.is_floor_discovered(self.current_room.num):
                self.unlock_manager.discovered_floors.append(str(self.current_room.num))
                self.timer.create_timer(0.75, self.launch_special_dialogue, arguments=[str(self.current_room.num)])
               
        else:
            self.popups.append(InfoPopup("you can't go off limits"))  # Show popup if trying to go below limits

    def launch_random_dialogue(self, bot_anim):
        """ Function to initiate dialogue easily passed to other functions"""
        self.gui_state = State.DIALOG
        self.paused = True
        self.temp_bg = pg.transform.grayscale(self.win)
        self.dialogue_manager.random_dialogue()  # Trigger a random dialogue
        self.dialogue_manager.bot_anim = bot_anim.copy()  # Copy the bot's surface for display
    
    def launch_special_dialogue(self, dialogue_name):
        self.gui_state = State.DIALOG
        self.paused = True
        self.temp_bg = pg.transform.grayscale(self.win)
        if dialogue_name=='0':
            self.dialogue_manager.special_dialogue(dialogue_name)
            InfoPopup("ATTENDEZ !! ")
            self.dialogue_manager.special_dialogue("0.5")
            self.dialogue_manager.bot_anim = None
        else:
            self.dialogue_manager.special_dialogue(dialogue_name)  # Trigger a random dialogue.
            self.dialogue_manager.bot_anim = None

    def pause(self):
        self.gui_state = State.PAUSED
        self.paused = True
        self.temp_bg = pg.transform.grayscale(self.win)
        self.quit_button = Button((0,0), self.quit, sprite.whiten(sprite.QUIT_BUTTON), sprite.QUIT_BUTTON)
        self.quit_button.rect.center = self.win.get_rect().center
        
    def quit(self):
        print('Quitting game ...')
        pg.event.post(pg.event.Event(pg.QUIT))
    
    def reset_guistate(self):
        self.paused = False
        self.gui_state = State.INTERACTION

    def process_total_beauty(self):
        """ Sums the overall beauty score to be used by the Bot_Manager"""
        total = 0
        for room in ROOMS:
            total += room.get_beauty_in_room()
        return total
    
    def accept_bot(self):
        """ When liberating a bot, add the proper money amount given by hivemind.free_last_bot (which updates the bots logic)"""
        accepted_bot_money_amount = self.hivemind.free_last_bot(R1)
        if accepted_bot_money_amount: # Attempt to free the last bot and checks output
            self.money += accepted_bot_money_amount  # Increment currency
        self.cachier_desk.active = True
        
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

#    ____              __    
#   / __/  _____ ___  / /____
#  / _/| |/ / -_) _ \/ __(_-<
# /___/|___/\__/_//_/\__/___/
                           
    def event_handler(self, event: pg.event.Event, mouse_pos: Coord):
        """
        Manages all events, eventually dispatching to sub functions like placeable_interaction_handler
        or keydown_handler
        """
        if event.type == pg.KEYDOWN:
            self.keydown_handler(event)

        if hasattr(self, "spectating_placeable") and self.spectating_placeable.open and self.current_room.num == 5:
            self.spectating_placeable.user_list.handle_event(event)

        if event.type == pg.MOUSEBUTTONDOWN:
            self.handle_mouse_button_down(event, mouse_pos)
        
        if self.current_room.num == 0:
            self.pattern_holder.handle_event(event)
            self.canva.handle_event(event)

# -----------------------------
# Keydown event handler
# -----------------------------

    def keydown_handler(self, event : pg.event.Event):
        if self.config['gameplay']['cheats']:
            self.handle_cheat_keys(event.key)
        self.handle_regular_keys(event.key)

    def handle_regular_keys(self, key):
        match key:
            case pg.K_SPACE:
                self.toggle_inventory()
            case pg.K_BACKSPACE:
                self.toggle_destruction_mode()
            case pg.K_ESCAPE:
                self.handle_escape_key()

    def handle_cheat_keys(self, key):
        match key:
            case pg.K_UP:
                self.change_floor(1)
            case pg.K_DOWN:
                self.change_floor(-1)
            case pg.K_b:
                self.hivemind.add_bot()
            case pg.K_n:
                self.hivemind.free_last_bot(self.current_room)
            case pg.K_s:
                self.toggle_shop()

    def toggle_inventory(self):
        if self.gui_state is State.INTERACTION:
            self.gui_state = State.INVENTORY
            self.inventory.init()
        elif self.gui_state is State.INVENTORY:
            self.reset_guistate()

    def toggle_destruction_mode(self):
        if self.gui_state is State.INTERACTION:
            self.gui_state = State.DESTRUCTION
        else:
            self.reset_guistate()

    def handle_escape_key(self):
        if self.gui_state not in [State.TRANSITION, State.CONFIRMATION, State.INTERACTION]:
            self.reset_guistate()
        elif self.gui_state is State.INTERACTION:
            self.pause()

    def save_canva(self):
        self.inventory.inv.append(self.canva.get_placeable())

    def toggle_shop(self):
        if self.gui_state is State.INTERACTION:
            self.gui_state = State.SHOP
            self.sound_manager.shop.play()
            self.shop.init()
        elif self.gui_state is State.SHOP:
            self.reset_guistate()

# -----------------------------
# Placeable interaction handler
# -----------------------------
    def placeable_interaction_handler(self, placeable : Placeable):
        """ Dispatches to the proper interaction function based on the placeable type"""
        match type(placeable):
            case subplaceable.DoorDown:
                self.handle_door_down_interaction(placeable)
            case subplaceable.DoorUp:
                self.handle_door_up_interaction(placeable)
            case subplaceable.BotPlaceable:
                self.accept_bot()
            case subplaceable.ShopPlaceable:
                self.handle_shop_interaction()
            case subplaceable.InvPlaceable:
                self.handle_inventory_interaction()
            case subplaceable.AutoCachierPlaceable:
                self.handle_auto_cachier_interaction()
            case subplaceable.SpectatorPlaceable:
                self.handle_spectator_interaction(placeable)
            case _:
                self.popups.append(InfoPopup(placeable.name))

    def handle_door_down_interaction(self, placeable):
        if self.current_room.num == 0:
            self.popups.append(InfoPopup("you can't go further down"))
        elif self.unlock_manager.is_floor_unlocked(self.current_room.num-1):
            self.timer.create_timer(0.75, self.change_floor, arguments=[-1])
            self.sound_manager.down.play()
            self.launch_transition()
            placeable.interaction(self.timer)
        else:
            self.unlock_manager.try_to_unlock_floor(self.current_room.num-1, self)

    def handle_door_up_interaction(self, placeable):
        if self.unlock_manager.is_floor_unlocked(self.current_room.num+1): # Check if the next floor is unlocked
            self.timer.create_timer(0.75, self.change_floor, arguments=[1]) # Change floor
            self.sound_manager.up.play() # Play sound
            self.launch_transition() # Launch transition
            placeable.interaction(self.timer)
        else: 
            self.unlock_manager.try_to_unlock_floor(self.current_room.num+1, self) # Try to unlock the next floor

    def handle_shop_interaction(self):
        if not self.unlock_manager.is_feature_discovered("shop"): # Check if the shop is discovered
            self.unlock_manager.discovered_features.append("shop")
            self.launch_special_dialogue("shop") # Launch tutorial dialogue
            return
        
        if self.gui_state is not State.SHOP:
            self.gui_state = State.SHOP
            self.shop.init()

    def handle_inventory_interaction(self):
        if not self.unlock_manager.is_feature_discovered("inventory"):
            self.unlock_manager.discovered_features.append("inventory")
            self.launch_special_dialogue("inventory")
            return

        if self.gui_state is not State.INVENTORY:
            self.gui_state = State.INVENTORY
            self.inventory.init()

    def handle_auto_cachier_interaction(self):
        if not self.unlock_manager.is_feature_unlocked("auto_cachier"):
            self.unlock_manager.try_to_unlock_feature("Auto Cachier", self)
        else:
            self.popups.append(InfoPopup("Vous avez déjà débloqué l'Auto Cachier"))

    def handle_spectator_interaction(self, placeable):
        if not self.unlock_manager.is_feature_discovered("spectator"):
            self.unlock_manager.discovered_features.append("spectator")
            self.launch_special_dialogue("spectator")
            return
        
        placeable.interaction()
        if placeable.open:
            self.popups.append(InfoPopup("Cliquez sur les fenetres pour visiter le musée d'un autre joueur !"))

# -----------------------------
# Mouse button up event handler
# -----------------------------

    def handle_mouse_button_down(self, event: pg.event.Event, mouse_pos: Coord):
        """
        Handles mouse button release events based on the current GUI state.
        """
        match self.gui_state:
            case State.BUILD:
                self.handle_build_mode()

            case State.INVENTORY:
                self.handle_inventory_mode(event, mouse_pos)

            case State.SHOP:
                self.shop.handle_click(mouse_pos, self)

            case State.DESTRUCTION:
                self.handle_destruction_mode(mouse_pos)

            case State.INTERACTION:
                self.handle_interaction_mode(mouse_pos)

            case State.DIALOG:
                self.handle_dialog_mode()

            case State.CONFIRMATION:
                self.handle_confirmation_mode(mouse_pos)

            case State.PAUSED:
                self.quit_button.handle_event(event)

    def handle_build_mode(self):
        if self.build_mode.can_place(self.current_room):
            self.current_room.placed.append(self.build_mode.place(self.current_room.num)) # Place the object in the room
            self.sound_manager.items.play() 
            self.beauty = self.process_total_beauty() # Update beauty score
            self.gui_state = State.INVENTORY # Return to the inventory
            self.inventory.init()

    def handle_inventory_mode(self, event: pg.event.Event, mouse_pos: Coord):
        self.inventory.handle_floor_navigation_buttons(event)
        self.inventory.handle_navigation(event)
        clicked_placeable = self.inventory.handle_click(mouse_pos)
        if clicked_placeable and self.current_room.num != 0:
            self.build_mode.selected_placeable = clicked_placeable
            self.gui_state = State.BUILD

    def handle_destruction_mode(self, mouse_pos: Coord):
        for placeable in self.current_room.placed:
            if placeable.rect.collidepoint(mouse_pos.x, mouse_pos.y):
                self.destruction_mode.remove_from_room(placeable, self.current_room) # Remove the object from the room
                self.beauty = self.process_total_beauty()

    def handle_interaction_mode(self, mouse_pos: Coord):
        for placeable in self.current_room.placed:
            if placeable.rect.collidepoint(mouse_pos.x, mouse_pos.y): # Check if the mouse is over a placeable
                self.placeable_interaction_handler(placeable)

        self.hivemind.handle_bot_click(mouse_pos, self.launch_random_dialogue) # Handle bot reaction click

    def handle_dialog_mode(self):
        if self.dialogue_manager.click_interaction(): # Check if the dialogue is over
            self.reset_guistate() # Return to the interaction state
            self.paused = False

    def handle_confirmation_mode(self, mouse_pos: Coord):
        flag = self.confirmation_popups[-1].handle_click(mouse_pos) # Check if the confirmation popup was clicked
        if flag is not None:
            self.confirmation_popups.pop()

        if not self.confirmation_popups: # If there are no more confirmation popups
            self.reset_guistate() # Return to the interaction state


#                    __      __     
#   __  ______  ____/ /___ _/ /____ 
#  / / / / __ \/ __  / __ `/ __/ _ \
# / /_/ / /_/ / /_/ / /_/ / /_/  __/
# \__,_/ .___/\__,_/\__,_/\__/\___/ 
#     /_/                         


    def update(self, mouse_pos):
        self.update_timers()
        self.update_particles()
        self.update_current_room(mouse_pos)
        self.update_bots()
        self.update_gui_state()

    def update_timers(self):
        self.timer.update()

    def update_particles(self):
        spawners: list[ParticleSpawner] = self.particle_spawners.get(self.current_room.num, None)
        if spawners is not None:
            for spawner in spawners:
                spawner.spawn()
                spawner.update_all()
                if spawner.finished:
                    spawners.remove(spawner)

    def update_current_room(self, mouse_pos):
        self.current_room.update_sprite()
        for placeable in self.current_room.placed:
            if placeable.rect.collidepoint(mouse_pos.xy) and self.gui_state in [State.DESTRUCTION, State.INTERACTION]:
                color = (170, 170, 230) if self.gui_state != State.DESTRUCTION else (255, 0, 0)
                placeable.update_sprite(True, color)
            else:
                placeable.update_sprite(False)

    def update_bots(self):
        self.hivemind.order_inline_bots()
        self.hivemind.update(ROOMS, self.timer)

    def update_gui_state(self):
        match self.gui_state:
            case State.INTERACTION:
                self.hivemind.create_last_bot_clickable()
        if self.confirmation_popups:
            self.gui_state = State.CONFIRMATION


#     ____                     
#    / __ \_________ __      __
#   / / / / ___/ __ `/ | /| / /
#  / /_/ / /  / /_/ /| |/ |/ / 
# /_____/_/   \__,_/ |__/|__/  

    def draw(self, mouse_pos: Coord):
        self.draw_background()
        self.draw_current_room()
        self.draw_bots(mouse_pos)
        self.draw_patterns_and_canva()
        self.draw_particles()
        self.draw_foreground()
        self.draw_gui(mouse_pos)
        if self.config['gameplay']['debug']:
            self.draw_debug_info(mouse_pos)
        self.render_popups()
        if not self.paused:
            self.win.blit(self.transparency_win, (0, 0))

    def draw_background(self):
        self.win.blit(self.current_room.bg_surf, (0, 0))
        self.transparency_win.fill((0, 0, 0, 0))

    def draw_current_room(self):
        self.current_room.draw_placed(self.win)
    
    def draw_foreground(self):
        self.current_room.draw_placed_foreground(self.win)

    def draw_bots(self, mouse_pos):
        self.hivemind.draw(self.win, self.current_room.num, mouse_pos, self.transparency_win)

    def draw_patterns_and_canva(self):
        if self.current_room.num == 0:
            self.canva.draw(self.win)
            self.pattern_holder.draw(self.win)

    def draw_particles(self):
        spawners: list[ParticleSpawner] = self.particle_spawners.get(self.current_room.num, None)
        if spawners is not None:
            for spawner in spawners:
                spawner.draw_all(self.transparency_win)

    def draw_gui(self, mouse_pos):
        match self.gui_state:
            case State.INTERACTION:
                if hasattr(self, "spectating_placeable") and self.spectating_placeable.open and self.current_room.num == 5:
                    self.spectating_placeable.user_list.draw(self.win)

            case State.BUILD:
                self.win.blit(sprite.BUILD_MODE_BORDER, (0, 0))
                mouse_pos_coord = Coord(self.current_room.num, (mouse_pos.x - self.build_mode.get_width() // 2, mouse_pos.y - self.build_mode.get_height() // 2))
                self.build_mode.show_hologram(self.win, mouse_pos_coord)
                self.build_mode.show_room_holograms(self.win, self.current_room)
            
            case State.DESTRUCTION:
                self.win.blit(sprite.DESTRUCTION_MODE_BORDER, (0, 0))

            case State.DIALOG:
                self.win.blit(self.temp_bg, (0, 0))
                self.paused = True
                self.dialogue_manager.update()
                self.dialogue_manager.draw(self.win)

            case State.PAUSED:
                self.win.blit(self.temp_bg, (0, 0))
                self.paused = True
                self.quit_button.draw(self.win, self.quit_button.rect.collidepoint(mouse_pos.xy))

            case State.TRANSITION:
                if self.incr_fondu <= pi:
                    self.incr_fondu = sprite.fondu(self.win, self.incr_fondu, 0.0125) #
                else:
                    self.reset_guistate() 

            case State.CONFIRMATION:
                if self.confirmation_popups:
                    self.confirmation_popups[-1].draw(mouse_pos)

            case State.INVENTORY:
                self.inventory.draw(self.win, mouse_pos)
                self.inventory.draw_floor_navigation_buttons(self.win, mouse_pos)

            case State.SHOP:
                self.shop.draw(self.win, mouse_pos)

    def draw_debug_info(self, mouse_pos):
        self.win.blit(InfoPopup(
            f'gui state : {self.gui_state} / fps : {round(self.clock.get_fps())} / mouse : {mouse_pos.xy} / $ : {self.money} / th_gold : {self.bot_distributor.theorical_gold} / beauty : {self.beauty}').text_surf, (0, 0))


#     __  ______    _____   __   __    ____  ____  ____ 
#    /  |/  /   |  /  _/ | / /  / /   / __ \/ __ \/ __ \
#   / /|_/ / /| |  / //  |/ /  / /   / / / / / / / /_/ /
#  / /  / / ___ |_/ // /|  /  / /___/ /_/ / /_/ / ____/ 
# /_/  /_/_/  |_/___/_/ |_/  /_____/\____/\____/_/      


    def get_save_dict(self):
        return {'gold': self.money, 'inventory': self.inventory.inv, "shop": self.shop.inv, "unlocks": self.unlock_manager, "beauty" : self.beauty}

    def main_loop(self) -> dict:
        fps = self.config['gameplay']['fps']  # Frame rate
        while True:
            self.clock.tick(fps)  # Maintain frame rate
            mouse_pos: Coord = Coord(self.current_room.num, pg.mouse.get_pos())  # Coordinates of the mouse (to not call pg.mouse.get_pos() multiple times)
            events = pg.event.get()  # Get all events from the event queue

            for event in events:
                if event.type == pg.QUIT:  # Check for quit event
                    pg.quit()  # Quit Pygame
                    return self.get_save_dict() # Return data to be saved in the DB
                
                self.event_handler(event, mouse_pos)
            
            if not self.paused: # If the game is not paused
                self.update(mouse_pos)

            self.draw(mouse_pos) # Draw the game


            pg.display.flip()  # Update the display