from placeable import Placeable
import sprite
from anim import Animation

class Door(Placeable):
    def __init__(self, name, coord, surf, tag = None):
        super().__init__(name, coord, surf, tag)
        self.is_open = False
        self.anim_close = Animation(sprite.SPRITESHEET_BAS, 0, 18, 4, False)
        self.anim_open = Animation(sprite.SPRITESHEET_HAUT, 0, 9, 4, False)

    def get_blit_args(self):
        if self.is_open:
            self.anim_close.reset_frame()
            self.surf = self.anim_open.get_frame()
        else:
            self.anim_open.reset_frame()
            self.surf = self.anim_close.get_frame()

        return self.surf, self.rect

        