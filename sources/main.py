import pygame as pg
import sys


pg.init()

# Set up the display window with specified resolution
WIN = pg.display.set_mode((0,0),pg.FULLSCREEN)
CLOCK = pg.time.Clock()
pg.display.set_caption('Creative Core')

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
from utils.timermanager import TimerManager
import ui.sprite as sprite
from objects.dialogue import DialogueManager
from core.logic import Game


TIMER = TimerManager()

popups: list[Popup] = []  # List to manage popups

incr_fondu = 0  # Variable for transition effects

# Initialize Hivemind instance to manage bots
hivemind = Hivemind(60, 600, TIMER)

# Initialize inventory and add placeable items
inventory: Inventory = Inventory()
inventory.inv.append(Placeable('6545dqw231', Coord(1, (121, 50)), sprite.P3))
inventory.inv.append(Placeable('6545dqwz31', Coord(1, (121, 50)), sprite.PROP_STATUE, tag="decoration", y_constraint=620))

# Instantiate build and destruction modes
build_mode: BuildMode = BuildMode()
destruction_mode: DestructionMode = DestructionMode()

#Test implementation of the dialogue class (to be integrated later)
dialogue_manager = DialogueManager('data\dialogue.txt')
dialogue_manager.load_save()

#tests 'temporary'
bot_distributor = BotDistributor(TIMER, hivemind)

moulaga = 0  # Currency variable
money_per_robot = 10  # Rewards per robot

#game initialized with all the objects as parameters instead of in the __init__ of Game, because of the eventuality that they would be loaded by a db save
game = Game(WIN, CLOCK, TIMER, hivemind, inventory, build_mode, destruction_mode, bot_distributor, dialogue_manager, moulaga)

if __name__ == '__main__':
    fps = 60  # Frame rate
    while True:
        CLOCK.tick(fps)  # Maintain frame rate
        mouse_pos: Coord = Coord(game.current_room.num, pg.mouse.get_pos())  # Create a coordinate object for the mouse position
        events = pg.event.get()  # Get all events from the event queue

        for event in events:
          if event.type == pg.QUIT:  # Check for quit event
              pg.quit()  # Quit Pygame
              sys.exit()  # Exit the program
          game.event_handler(event, mouse_pos)
        
        game.update(mouse_pos)

        game.draw(mouse_pos)


        pg.display.flip()  # Update the display
