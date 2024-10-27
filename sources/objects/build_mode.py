from placeable import Placeable
from room import Room
from coord import Coord
from pygame import Surface, BLEND_RGBA_ADD

class Build_mode():
    def __init__(self) -> None:
        self.selected_placeable : Placeable = None
        #self.in_build_mode : bool = False
        

    def show_hologram(self, win : Surface, mouse_pos : Coord):
        pixel_perfect_mouse_pos = mouse_pos.get_pixel_perfect()

        hologram_rect_surf : Surface = Surface((self.selected_placeable.rect.width, self.selected_placeable.rect.height))
        hologram_rect_surf.set_alpha(50)        
        hologram_rect_surf.fill((0,0,200,50))

        hologram : Surface = self.selected_placeable.surf.copy()
        hologram.set_alpha(150)
        hologram.fill((0,0,200,0),special_flags=BLEND_RGBA_ADD)

        win.blits([(hologram_rect_surf, pixel_perfect_mouse_pos), (hologram, pixel_perfect_mouse_pos)])
    
    def can_place(self, mouse_pos : Coord, room : Room) -> bool:
        """check if the placeable can be placed without colliding with other objects"""
        ghost_rect = self.selected_placeable.rect.copy()
        ghost_rect.topleft = mouse_pos.xy
        room_rects = [placeable.rect for placeable in room.placed]
        if ghost_rect.collidelistall(room_rects):
            return False
        else:
            return True

    def place(self, mouse_pos : Coord) -> Placeable:
        self.selected_placeable.move(mouse_pos)
        self.selected_placeable.placed = True
        return self.selected_placeable
    
class Destruction_mode():
    def __init__(self) -> None:
        self.in_destruction_mode : bool = False

    def remove_from_room(self, placeable : Placeable, room : Room):
        """removes the placeable in the room"""
        if placeable not in room.blacklist:
            placeable.placed = False
            room.placed.remove(placeable)
    
    def toggle(self):
        self.in_destruction_mode = not self.in_destruction_mode
