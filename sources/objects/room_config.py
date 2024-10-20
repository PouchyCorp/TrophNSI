from room import Room
from coord import Coord 
from placeable import Placeable
from pygame import Surface

#R1
R1 = Room(1)
R1_stairs = Placeable('R1_stairs', Coord(1,(1600,500)), Surface((100,200)))
R1.placed.append(R1_stairs)
R1.native_placed.append(R1_stairs)


#R2
R2 = Room(2)
R2_stairs = Placeable('R2_stairs', Coord(1,(1200,300)), Surface((200,300)))
R2.placed.append(R2_stairs)
R2.native_placed.append(R2_stairs)



#R3
R3 = Room(3)
