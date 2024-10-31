from objects.coord import Coord 
from objects.placeable import Placeable
from objects.room import Room
import objects.sprite as sprite
from pygame import Surface,image,transform

#R0
R0 = Room(0,sprite.BG1)
canva = Placeable('canva', Coord(1,(1200,50)), Surface((700,1000)))

#R1
R1 = Room(1,sprite.BG1)
#R1_stairs = Placeable('R1_stairs', Coord(1,(1000,300)), sprite.P1)
#test_place = Placeable("test",Coord(1,(200,200)), Surface((180,180))) 

#R1.placed.append(R1_stairs)
#R1.blacklist.append(R1_stairs)


#R2
R2 = Room(2,sprite.BG1)
R2_stairs = Placeable('R2_stairs', Coord(1,(1200,300)), Surface((200,300)))
test_canva = Placeable('test_canva', Coord(1,(100,100)), Surface((48*6,64*6)))

R2.placed.append(test_canva)
R2.placed.append(R2_stairs)
R2.blacklist.append(R2_stairs)



#R3
R3 = Room(3,sprite.BG1)


#P
P = Room(666, sprite.BG2)