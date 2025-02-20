r"""
   _____       _          _                         
  / ____|     | |        | |                        
 | (___  _   _| |__   ___| | __ _ ___ ___  ___  ___ 
  \___ \| | | | '_ \ / __| |/ _` / __/ __|/ _ \/ __|
  ____) | |_| | |_) | (__| | (_| \__ \__ \  __/\__ \
 |_____/ \__,_|_.__/ \___|_|\__,_|___/___/\___||___/
                                                    
Module dedicated to the subclass of the Placeable class.

Key Features:
-------------
    - DoorUp and DoorDown classes for the door objects.
    - BotPlaceable for the clickable inline bot.
    - ShopPlaceable for the shop placeable at floor 2.
    - InvPlaceable for the inventory placeable at floor 1.
    - AutoCachierPlaceable for the automatic cash register unlock at floor 4.
    - SpectatorPlaceable for the spectator placeable at floor 5.
"""

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
    def __init__(self, name, coord, surf, tag = None):
        super().__init__(name, coord, surf, tag)
        self.blink_anim = Animation(sprite.SPRITESHEET_INVENTORY, 0, 7)
        self.surf = self.blink_anim.get_frame()
    
    def update_sprite(self, is_hovered, color = (150, 150, 255)):
        if is_hovered:
            self.surf = self.blink_anim.get_frame()
        else:
            self.surf = sprite.SPRITESHEET_INVENTORY.get_img((0,0))

        return super().update_sprite(is_hovered, color)

class AutoCachierPlaceable(Placeable):
    pass

class SpectatorPlaceable(Placeable):
    def __init__(self, name, coord, surf, pg_database, tag = None):
        super().__init__(name, coord, surf, tag)
        self.pg_database = pg_database
        from ui.userlist import UserList
        self.user_list = UserList(self.coord.xy, self.pg_database.fetch_all_user_data())
        self.open = False
        
    def interaction(self):
        self.open = not self.open
        if self.open:
            self.user_list.init(self.pg_database.fetch_all_user_data())

class DeskPlaceable(Placeable):
    def __init__(self, name, coord, surf, tag = None):
        super().__init__(name, coord, surf, tag)
        self.anim_bg = Animation(sprite.COUNTER_DESK, 0, 14, repeat=False)
        self.surf = self.anim_bg.reset_frame()
        print(self.surf)
        self.active = False

    def update_sprite(self, is_hovered, color = ...):
        if self.anim_bg.is_finished():
            self.active = False
            self.surf = self.anim_bg.reset_frame()

        if self.active:
            self.surf = self.anim_bg.get_frame()
        
        self.temp_surf = self.surf.copy()
        self.temp_rect = self.rect.copy()


