import pygame as pg
import tomli

with open('sources/config.toml', 'rb') as f:
      config = tomli.load(f)

def get_save_dict(game):
  print('game saved')
  return {'gold' : game.money, 'inventory' : game.inventory.inv, "shop" : game.shop.inv}

def start_game(game_save_dict):
    # Open config file and dump it in a dict
  pg.init()
  pg.mixer.init()

  # Set up the display window with specified resolution using the config file
  if config['screen']['fullscreen']:
    WIN = pg.display.set_mode((0,0),pg.FULLSCREEN)
  else:
    WIN = pg.display.set_mode(config['screen']['size'])

  pg.display.set_icon(pg.image.load('data/big_icon.png'))


  CLOCK = pg.time.Clock()
  pg.display.set_caption('Creative Core')
  
  from utils.coord import Coord
  from ui.inventory import Inventory, Shop
  from core.logic import Game
  from  utils.room_config import ROOMS

  # Initialize inventory and shop fromm save
  inventory= Inventory("Inventory", game_save_dict['inventory'])
  shop: Shop = Shop("Shop", game_save_dict['shop'])

  # Places placeables in room from inventory
  for placeable in inventory.inv:
    if placeable.placed:
      ROOMS[placeable.coord.room_num].placed.append(placeable)

  #game initialized with some objects as parameters instead of in the __init__ of Game, because of the eventuality that they would be loaded by a db save
  game = Game(WIN, CLOCK, inventory, shop, game_save_dict['gold'])
    

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

if not config['gameplay']['no_login']:
  from  core.database import PgDataBase
  db = PgDataBase()
  username, user_game_data = db.tk_ui()

  data_to_save = start_game(user_game_data)

  db.save_user_data(username, data_to_save)
else:
  from  utils.room_config import DEFAULT_SAVE
  start_game(DEFAULT_SAVE)