import pygame as pg
import tomli

with open('sources/config.toml', 'rb') as f:
    config = tomli.load(f)

def start_game(game_save_dict):
    # Open config file and dump it in a dict
    pg.init()
    pg.mixer.init()

    # Set up the display window with specified resolution using the config file
    if config['screen']['fullscreen']:
        WIN = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    else:
        WIN = pg.display.set_mode(config['screen']['size'])

    pg.display.set_icon(pg.image.load('data/big_icon.png'))

    pg.display.set_caption('Creative Core')

    from ui.inventory import Inventory, Shop
    from core.logic import Game
    from utils.room_config import ROOMS

    # Initialize inventory and shop fromm save
    inventory = Inventory("Inventory", game_save_dict['inventory'])
    shop: Shop = Shop("Shop", game_save_dict['shop'])

    # Places placeables in room from inventory
    for placeable in inventory.inv:
        if placeable.placed:
            ROOMS[placeable.coord.room_num].placed.append(placeable)

    # game initialized with some objects as parameters instead of in the __init__ of Game, because of the eventuality that they would be loaded by a db save
    game = Game(WIN, config, inventory, shop,
                game_save_dict['gold'], game_save_dict['unlocks'])


    # ------------------------#
    #        game loop        #
    # ------------------------#
    return game.main_loop()



# ------------------------#
#      overseer loop      #
# ------------------------#
if not config['gameplay']['no_login']:
    from core.database import PgDataBase
    db = PgDataBase()
    username, user_game_data = db.home_screen()

    print('launching game')
    data_to_save = start_game(user_game_data)

    db.save_user_data(username, data_to_save)
else:
    from utils.room_config import DEFAULT_SAVE
    start_game(DEFAULT_SAVE)
