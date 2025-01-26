from objects.placeable import Placeable
from utils.anim import Animation

class Room:
    def __init__(self, num, bg_surf = None, anim = None) -> None:
        assert bg_surf or anim, "you should define at least one of the following : bg_surf, anim"

        self.size_px = (320,180)
        self.num = num
        self.placed : list[Placeable] = []
        
        self.anim : Animation = anim
        if self.anim:
            self.bg_surf = self.anim.get_frame()
        else:
            self.bg_surf = bg_surf
        #permanent objects that can not be edited (still place in placed to render the object)
        self.blacklist : list[Placeable] = []

    def in_blacklist(self, plcbl : Placeable) -> bool:
        return (plcbl in self.blacklist)
    
    def name_exists_in_placed(self, name : str) -> bool:
        for obj in self.placed:
            if obj.name == name:
                return True
        return False
    
    def draw_placed(self, win):
        #map(self.check_coords, self.placed)
        win.blits([placeable.get_blit_args() for placeable in self.placed])
        for placeable in self.placed:
            if placeable.temporary:
                self.placed.remove(placeable)
    
    def get_beauty_in_room(self):
        total = 0
        for placeable in self.placed:
            if placeable.tag == "decoration":
                total += placeable.beauty
        return total
    
    def update_sprite(self):
        if self.anim:
            self.bg_surf = self.anim.get_frame()