import pygame as pg
import sys
import tomllib
import pickle


def get_save_dict(game):
  print('game saved')
  return pickle.dumps({'gold' : game.gold, 'beauty' : game.beauty})

def load_game(default) -> dict:
    try:
      with open('save.pkl', 'rb') as file:
        data = pickle.load(file)

        if data:
           return data
        else:
           return {'gold' : 0, 'beauty' : 1} # Default 
      
    except FileNotFoundError:
       print('no save file to load, loading default values')
       return {'gold' : 0, 'beauty' : 1} # Default 

def start_game(game_save_dict):
    # Open config file and dump it in a dict
  with open('sources/config.toml', 'rb') as f:
      config = tomllib.load(f)

  pg.init()
  pg.mixer.init()

  # Set up the display window with specified resolution using the config file
  if config['screen']['fullscreen']:
    WIN = pg.display.set_mode((0,0),pg.FULLSCREEN)
  else:
    WIN = pg.display.set_mode(config['screen']['size'])

  CLOCK = pg.time.Clock()
  pg.display.set_caption('Creative Core')

  from objects.placeable import Placeable
  from utils.coord import Coord
  from ui.inventory import Inventory, Shop
  from core.logic import Game
  import ui.sprite as sprite

  # Initialize inventory and add placeable items
  inventory= Inventory([Placeable('6545dqw231', Coord(1, (121, 50)), sprite.P3),
                        Placeable('6545dqwz31', Coord(1, (121, 50)), sprite.PROP_STATUE, tag="decoration", y_constraint=620),
                        Placeable('6545dqwz31', Coord(1, (39, 38)), sprite.SPRITE_PLANT_1, tag="decoration", y_constraint=700),
                        Placeable('6545dqwz31', Coord(1, (28, 48)), sprite.SPRITE_PLANT_2, tag="decoration", y_constraint=620),
                        Placeable('6545dqwz31', Coord(1, (28, 48)), sprite.SPRITE_PLANT_2, tag="decoration", y_constraint=620),
                        Placeable('6545dqwz31', Coord(1, (28, 48)), sprite.SPRITE_PLANT_2, tag="decoration", y_constraint=620),
                        Placeable('6545dqwz31', Coord(1, (28, 48)), sprite.SPRITE_PLANT_2, tag="decoration", y_constraint=620),
                        Placeable('6545dqwz31', Coord(1, (28, 48)), sprite.SPRITE_PLANT_2, tag="decoration", y_constraint=620),
                        Placeable('6545dqwz31', Coord(1, (28, 48)), sprite.SPRITE_PLANT_2, tag="decoration", y_constraint=620),
                        Placeable('6545dqwz31', Coord(1, (28, 48)), sprite.SPRITE_PLANT_2, tag="decoration", y_constraint=620),
                        Placeable('6545dqwz31', Coord(1, (28, 48)), sprite.SPRITE_PLANT_2, tag="decoration", y_constraint=620)])

  shop: Shop = Shop()
  shop.inv.append(Placeable('6545dqdfwz31', Coord(1, (121, 50)), sprite.PROP_STATUE, tag="decoration", y_constraint=620, price=10))

  #game initialized with some objects as parameters instead of in the __init__ of Game, because of the eventuality that they would be loaded by a db save
  game = Game(WIN, CLOCK, inventory, shop, game_save_dict['gold'], game_save_dict['beauty'])
    

  if __name__ == '__main__':
      fps = config['gameplay']['fps']  # Frame rate
      while True:
          CLOCK.tick(fps)  # Maintain frame rate
          mouse_pos: Coord = Coord(game.current_room.num, pg.mouse.get_pos())  # Create a coordinate object for the mouse position
          events = pg.event.get()  # Get all events from the event queue

          for event in events:
            if event.type == pg.QUIT:  # Check for quit event
                pg.quit()  # Quit Pygame
                return get_save_dict(game)

            game.event_handler(event, mouse_pos)
          
          game.update(mouse_pos)

          game.draw(mouse_pos)


          pg.display.flip()  # Update the display

#------------------------#
#       main loop        #
#------------------------#

from database import TkDataBase
db = TkDataBase()
db.tk_ui()

start_game({'gold' : 10, 'beauty' : 0})