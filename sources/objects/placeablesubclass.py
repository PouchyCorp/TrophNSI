from placeable import Placeable
import ui.sprite as sprite
from utils.anim import Animation
from typing import Optional
from utils.timermanager import TimerManager

class DoorUp(Placeable):
    def __init__(self, name, coord, surf, tag = None):
        super().__init__(name, coord, surf, tag)
        self.anim_close = Animation(sprite.SPRITESHEET_BAS, 0, 9, 4, False)     #download closing animation
        self.anim_open = Animation(sprite.SPRITESHEET_HAUT, 0, 17, 4, False)    #download oppening animation
        self.anim_blink = Animation(sprite.SPRITESHEET_DOOR_BLINK, 0, 10)       #download blinking animation
        self.anim = self.anim_close
        _rect = self.anim.get_frame().get_rect()
        self.rect.width, self.rect.height = _rect.width, _rect.height
        self.anim.reset_frame()
        self.door_down : Optional[DoorDown] = None
    
    def pair_door_down(self, door_down):
        self.door_down = door_down

    def update_sprite(self, is_hovered : bool, color : tuple = (150, 150, 255)):
        if self.anim != self.anim_open and self.anim_close.is_finished():     #check if the animation is finish
            if is_hovered:
                self.anim = self.anim_blink
            else:           #delete the blinking animation after closing when the mouse isn't on the door
                self.surf = sprite.SPRITESHEET_DOOR_BLINK.get_img((0,0))
                self.anim = None
    
        super().update_sprite(is_hovered, color)
    
    def interaction(self, timer : TimerManager):
        self.anim_open.reset_frame()        #reset all animations when the mouse is on the door to expect the change of floor
        self.anim_close.reset_frame()
        self.anim = self.anim_open
        self.door_down.anim_open.reset_frame()
        self.door_down.anim_close.reset_frame()
        self.door_down.anim = self.door_down.anim_open
        

        timer.create_timer(1.5, self.set_attribute, arguments=('anim', self.anim_close))        #set the duration of the animation
        timer.create_timer(1.5, self.door_down.set_attribute, arguments=('anim', self.door_down.anim_close))

class DoorDown(Placeable):
    def __init__(self, name, coord, surf, tag = None):
        super().__init__(name, coord, surf, tag)
        self.anim_close = Animation(sprite.SPRITESHEET_BAS_FLIP, 0, 9, 4, False)        #download closing animation
        self.anim_open = Animation(sprite.SPRITESHEET_HAUT_FLIP, 0, 7, 4, False)        #download oppening animation
        self.anim_blink = Animation(sprite.SPRITESHEET_DOOR_BLINK_FLIP, 0, 10)          #download blink animation
        self.anim = self.anim_close
        _rect = self.anim.get_frame().get_rect()
        self.rect.width, self.rect.height = _rect.width, _rect.height
        self.door_up : Optional[DoorUp] = None

    
    def pair_door_up(self, door_up):
        self.door_up = door_up
    
    def update_sprite(self, is_hovered : bool, color : tuple = (150, 150, 255)):
        if self.anim != self.anim_open and self.anim_close.is_finished():       #check if the animation is finish
            if is_hovered:
                self.anim = self.anim_blink
            else:           #delete the blinking animation after closing when the mouse isn't on the door
                self.surf = sprite.SPRITESHEET_DOOR_BLINK_FLIP.get_img((0,0))
                self.anim = None
    
        super().update_sprite(is_hovered, color)
    
    def interaction(self, timer : TimerManager):
        self.anim_open.reset_frame()        #reset all animations when the mouse is on the door to expect the change of floor
        self.anim_close.reset_frame()
        self.anim = self.anim_open
        self.door_up.anim_open.reset_frame()
        self.door_up.anim_close.reset_frame()
        self.door_up.anim = self.door_up.anim_open
        

        timer.create_timer(1.5, self.set_attribute, arguments=('anim', self.anim_close))        #set the duration of the animation
        timer.create_timer(1.5, self.door_up.set_attribute, arguments=('anim', self.door_up.anim_close))
        

class BotPlaceable(Placeable):
    pass

class ShopPlaceable(Placeable):
    pass

class InvPlaceable(Placeable):
    pass

class AutoCachierPlaceable(Placeable):
    pass
    



