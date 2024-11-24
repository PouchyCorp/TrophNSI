from objects.coord import Coord 
from objects.placeable import Placeable
from objects.room import Room
import objects.sprite as sprite
from pygame import Surface,image,transform
from objects.anim import Spritesheet,Animation

spritesheet_prt = Spritesheet(sprite.SPRTESHEET_PORTE,(60*20,60*20))
anim_prt = Animation(spritesheet_prt,0,20)

#R0
R0 = Room(0,sprite.BG2)
canva = Placeable('canva', Coord(0,(1200,50)), Surface((700,1000)))

#R1
R1 = Room(1,sprite.BG1)
#R1_stairs = Placeable('R1_stairs', Coord(1,(1000,300)), sprite.P1)
#test_place = Placeable("test",Coord(1,(200,200)), Surface((180,180))) 
test_canva = Placeable('test_canva', Coord(1,(1000,100)), Surface((48*6,64*6)), "decoration")
R1.placed.append(test_canva)
#R1.placed.append(R1_stairs)
#R1.blacklist.append(R1_stairs)


#R2
R2 = Room(2,sprite.BG3)
R2_stairs = Placeable('R2_stairs', Coord(2,(1551,442)), Surface((335,220)),anim_prt)
test_canva = Placeable('test_canva', Coord(2,(100,100)), Surface((48*6,64*6)), "decoration")

R2.placed.append(test_canva)
R2.placed.append(R2_stairs)
R2.blacklist.append(R2_stairs)



#R3
R3 = Room(3,sprite.BG3)


ROOMS : list[Room] = [R0, R1, R2, R3]