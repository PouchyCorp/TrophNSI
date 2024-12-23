from utils.coord import Coord 
from objects.placeable import Placeable
from core.room import Room
import ui.sprite as sprite
from pygame import Surface
import objects.placeablesubclass as subplaceable

stairs_up = subplaceable.DoorUp('R1_stairs', Coord(1,(1594,546)), Surface((335,220)))
stairs_down = subplaceable.DoorDown('R1_stairs_down', Coord(1,(1594,516 + 33*6)), Surface((335,220)))

stairs_down.pair_door_up(stairs_up)
stairs_up.pair_door_down(stairs_down)
#R0
R0 = Room(0,sprite.BG2)
canva = Placeable('canva', Coord(0,(1200,50)), Surface((700,1000)))

#R1
R1 = Room(1,sprite.BG1)
test_canva = Placeable('test_canva', Coord(1,(1000,100)), Surface((48*6,64*6)), "decoration")
R1.placed.append(test_canva)
R1.placed += [stairs_up , stairs_down]


#R2
R2 = Room(2,sprite.BG3)
test_canva = Placeable('test_canva', Coord(2,(100,100)), Surface((48*6,64*6)), "decoration")
R2.placed.append(test_canva)
R2.placed += [stairs_up , stairs_down]



#R3
R3 = Room(3,sprite.BG4)
R3.placed += [stairs_up , stairs_down]


R4 = Room(4, sprite.BG5)
R4.placed += [stairs_up , stairs_down]


ROOMS : list[Room] = [R0, R1, R2, R3, R4]