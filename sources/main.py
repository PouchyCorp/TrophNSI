import pygame as pg
import sys


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
from objects.dialogue import DialogueManager
from math import pi
from core.logic import Game


TIMER = TimerManager()

current_room = R1  # Initialize the current room to R1
  # Start with the interaction GUI state
popups: list[Popup] = []  # List to manage popups

incr_fondu = 0  # Variable for transition effects

# Initialize Hivemind instance to manage bots
hivemind = Hivemind(60, 600, TIMER)
anim = Animation(sprite.SPRITESHEET_ROBOT_2, 0, 14)

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
dialogue_manager = DialogueManager('data\dialogue.txt')
dialogue_manager.load_save()

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

if __name__ == '__main__':
    fps = 60  # Frame rate
    game = Game(WIN, CLOCK, TIMER, hivemind, inventory, build_mode, destruction_mode, bot_distributor, dialogue_manager, moulaga)
    while True:
        CLOCK.tick(fps)  # Maintain frame rate
        mouse_pos: Coord = Coord(current_room.num, pg.mouse.get_pos())  # Create a coordinate object for the mouse position
        events = pg.event.get()  # Get all events from the event queue
        keys = pg.key.get_pressed()  # Get the current state of all keyboard keys

        for event in events:
          if event.type == pg.QUIT:  # Check for quit event
              pg.quit()  # Quit Pygame
              sys.exit()  # Exit the program
          game.event_handler(event, mouse_pos)
        
        game.update(mouse_pos)

        game.draw(mouse_pos)


        pg.display.flip()  # Update the display
