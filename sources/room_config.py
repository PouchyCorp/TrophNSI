from objects.coord import Coord 
from objects.placeable import Placeable
from objects.room import Room
import objects.sprite as sprite
from pygame import Surface,image,transform
from objects.anim import Spritesheet,Animation
import objects.placeablesubclass as subplaceable

#R0
R0 = Room(0,sprite.BG2)
canva = Placeable('canva', Coord(0,(1200,50)), Surface((700,1000)))

#R1
R1 = Room(1,sprite.BG1)
#test_place = Placeable("test",Coord(1,(200,200)), Surface((180,180))) 
test_canva = Placeable('test_canva', Coord(1,(1000,100)), Surface((48*6,64*6)), "decoration")
R1_stairs = subplaceable.Door_up('R1_stairs', Coord(1,(1594,485)), Surface((335,220)))
R1_stairs_down = subplaceable.Door_down('R1_stairs_down', Coord(1,(1594,485 + 35*6)), Surface((335,220)))
R1.placed.append(test_canva)
R1.placed += [R1_stairs_down , R1_stairs ]
R1.blacklist.append(R1_stairs)


#R2
R2 = Room(2,sprite.BG3)
R2_stairs = subplaceable.Door_up('R2_stairs', Coord(2,(1594,485)), Surface((335,220)))
R2_stairs_down = subplaceable.Door_down('R1_stairs_down', Coord(1,(1594,485 +35*6)), Surface((335,220)))
test_canva = Placeable('test_canva', Coord(2,(100,100)), Surface((48*6,64*6)), "decoration")

R2.placed.append(test_canva)
R2.placed += [R2_stairs_down , R2_stairs ]
R2.blacklist.append(R2_stairs)



#R3
R3 = Room(3,sprite.BG4)


ROOMS : list[Room] = [R0, R1, R2, R3]