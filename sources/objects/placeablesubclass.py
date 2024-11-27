from placeable import Placeable
import sprite
from anim import Animation
from typing import Optional
from timermanager import _Timer_manager
from room import Room

class DoorUp(Placeable):
    def __init__(self, name, coord, surf, tag = None):
        super().__init__(name, coord, surf, tag)
        self.anim_close = Animation(sprite.SPRITESHEET_BAS, 0, 9, 4, False)
        self.anim_open = Animation(sprite.SPRITESHEET_HAUT, 0, 17, 4, False)
        self.anim = self.anim_close
        self.door_down : Optional[DoorDown] = None
    
    def pair_door_down(self, door_down):
        self.door_down = door_down

    
    def update_sprite(self, is_hovered : bool, color : tuple = (150, 150, 255)):
        if is_hovered and self.anim_close.is_finished():
            self.anim = self.anim_open #to replace with only the blinking
            self.anim_close.reset_frame()

        elif not is_hovered and self.anim_open.is_finished():
            self.anim = self.anim_close
            self.anim_open.reset_frame()
        
        super().update_sprite(is_hovered, color)

    def interaction(self, args):
        TIMER : _Timer_manager = args[0]
        rooms : list[Room] = args[1]
        TIMER.create_timer(0.5, )
        

class DoorDown(Placeable):
    def __init__(self, name, coord, surf, tag = None):
        super().__init__(name, coord, surf, tag)
        self.anim_close = Animation(sprite.SPRITESHEET_BAS_1, 0, 9, 4, False)
        self.anim_open = Animation(sprite.SPRITESHEET_HAUT_1, 0, 17, 4, False)
        self.anim = self.anim_close
        self.door_up : Optional[DoorUp] = None
    
    def pair_door_up(self, door_up):
        self.door_up = door_up
    
    def update_sprite(self, is_hovered : bool, color : tuple = (150, 150, 255)):
        if is_hovered and self.anim_close.is_finished():
            self.anim = self.anim_open #to replace with only the blinking
            self.anim_close.reset_frame()

        elif not is_hovered and self.anim_open.is_finished():
            self.anim = self.anim_close
            self.anim_open.reset_frame()
    
        super().update_sprite(is_hovered, color)

class BotPlaceable(Placeable):
    pass