from placeable import Placeable
import sprite
from anim import Animation

class Door_up(Placeable):
    def __init__(self, name, coord, surf, tag = None):
        super().__init__(name, coord, surf, tag)
        self.anim_close = Animation(sprite.SPRITESHEET_BAS, 0, 9, 4, False)
        self.anim_open = Animation(sprite.SPRITESHEET_HAUT, 0, 17, 4, False)
        self.anim = self.anim_close

class Door_down(Placeable):
    def __init__(self, name, coord, surf, tag = None):
        super().__init__(name, coord, surf, tag)
        self.anim_close = Animation(sprite.SPRITESHEET_BAS_1, 0, 9, 4, False)
        self.anim_open = Animation(sprite.SPRITESHEET_HAUT_1, 0, 17, 4, False)
        self.anim = self.anim_close