r"""
                                               __ _       
                                              / _(_)      
  _ __ ___   ___  _ __ ___     ___ ___  _ __ | |_ _  __ _ 
 | '__/ _ \ / _ \| '_ ` _ \   / __/ _ \| '_ \|  _| |/ _` |
 | | | (_) | (_) | | | | | | | (_| (_) | | | | | | | (_| |
 |_|  \___/ \___/|_| |_| |_|  \___\___/|_| |_|_| |_|\__, |
                                                     __/ |
                                                    |___/ 

This module contains the default configuration for the rooms in the game.
The initialization of the rooms is done in the init_rooms() function and not directly at the top level of the module to allow for making 
copies of the rooms without reinitializing them (because shared by the main game and spectator mode).
"""

from utils.coord import Coord
from objects.placeable import Placeable
from core.room import Room
import ui.sprite as sprite
from pygame import Surface
import objects.placeablesubclass as subplaceable
from core.unlockmanager import UnlockManager
from utils.anim import Animation
from objects.particlesspawner import ConfettiSpawner


def init_rooms():
    stairs_up = subplaceable.DoorUp(
        'R1_stairs', Coord(1, (1594, 546)), Surface((335, 220)))
    stairs_down = subplaceable.DoorDown('R1_stairs_down', Coord(
        1, (1594, 516 + 33*6)), Surface((335, 220)))

    stairs_down.pair_door_up(stairs_up)
    stairs_up.pair_door_down(stairs_down)
    # R0
    R0 = Room(0, sprite.BG2)
    R0.placed += [stairs_up]

    # R1
    R1 = Room(1, sprite.BG1)
    guichet = subplaceable.DeskPlaceable('guichet', Coord(1, (470, 692)), Surface((0,0)))
    auto_cachier = subplaceable.AutoCachierPlaceable(
        'AutoCachierPlaceable', Coord(1, (1500, 700)), Surface((10*6, 10*6)))
    inventory_plcb = subplaceable.InvPlaceable(
        "Inventory", Coord(1, (1536, 186)), Surface((53*6, 31*6)))
    R1.placed += [guichet, stairs_up,
                  stairs_down, auto_cachier, inventory_plcb]
    R1.blacklist += [stairs_up, stairs_down, auto_cachier, inventory_plcb, guichet]

    # R2
    R2 = Room(2, sprite.BG3)
    shop = subplaceable.ShopPlaceable('shop', Coord(
        2, (1000, 100)), Surface((50*6, 90*6)), "shop")
    R2.placed += [stairs_up, stairs_down, shop]
    R2.blacklist += [stairs_up, stairs_down, shop]

    # R3
    R3 = Room(3, sprite.BG4)
    R3.placed += [stairs_up, stairs_down]

    R4 = Room(4, sprite.BG5)
    R4.placed += [stairs_up, stairs_down]

    R5 = Room(5, anim=Animation(sprite.SPRITESHEET_ROOFTOP, 0, 14, 8))
    R5.placed += [stairs_down]

    return [R0, R1, R2, R3, R4, R5]


ROOMS: list[Room] = init_rooms()

R0 = ROOMS[0]
R1 = ROOMS[1]
R2 = ROOMS[2]
R3 = ROOMS[3]
R4 = ROOMS[4]
R5 = ROOMS[5]

DEFAULT_SAVE = {'gold': 10,
                "beauty": 0,
                "inventory": [Placeable('cheater beauty', Coord(2, (100, 100)), sprite.PROP_STATUE, "decoration", y_constraint=0, price=50, beauty=1000)],


                "shop": [Placeable('bust', Coord(2, (100, 100)), sprite.PROP_STATUE, "decoration", y_constraint=0, price=50, beauty=10),
                         Placeable('plante 1', Coord(2, (100, 100)), sprite.SPRITE_PLANT_1,
                                   "decoration",  y_constraint=0, price=50, beauty=100),
                         Placeable('plante 2', Coord(2, (100, 100)), sprite.SPRITE_PLANT_2, "decoration",  y_constraint=0, price=50, beauty=1000)],

                "unlocks": UnlockManager()}

PARTICLE_SPAWNERS = {0: [], 1: [ConfettiSpawner(Coord(1, (0, 0)), 500)], 2: [], 3: [], 4: [], 5: []}
