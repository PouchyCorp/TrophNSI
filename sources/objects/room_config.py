from room import Room
from coord import Coord 
from placeable import Placeable
from pygame import Surface,image

#R1
R1 = Room(1,image.load("data/bg_test_1.png"))
R1_stairs = Placeable('R1_stairs', Coord(1,(1600,500)), Surface((100,200)))
test_place = Placeable("test",Coord(1,(100,500)), Surface((100,200))) 
R1.blacklist.append(test_place)
R1.placed.append(test_place)
R1.placed.append(R1_stairs)
R1.blacklist.append(R1_stairs)


#R2
R2 = Room(2,image.load("data/bg_test_2.png"))
R2_stairs = Placeable('R2_stairs', Coord(1,(1200,300)), Surface((200,300)))
R2.placed.append(R2_stairs)
R2.blacklist.append(R2_stairs)



#R3
R3 = Room(3,image.load("data/bg_test_1.png"))
