from objects.coord import Coord 
from objects.placeable import Placeable
from objects.room import Room
from pygame import Surface,image

#R0
R0 = Room(0,image.load("data/bg_test_1.png"))
canva = Placeable('canva', Coord(1,(1200,50)), Surface((700,1000)))

#R1
R1 = Room(1,image.load("data/bg_test_1.png"))
R1_stairs = Placeable('R1_stairs', Coord(1,(1500,600)), Surface((200,300)))
test_place = Placeable("test",Coord(1,(200,200)), Surface((180,180))) 

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
