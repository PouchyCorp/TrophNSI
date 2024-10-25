from placeable import Placeable
from room import Room
from coord import Coord
from pygame import Surface, BLEND_RGBA_ADD

class Build_mode():
    def __init__(self, selected_placeable) -> None:
        self.selected_placeable : Placeable = selected_placeable
        self.in_build_mode : bool = False
        

    def show_hologram(self, win : Surface, mouse_pos : Coord):
        pixel_perfect_mouse_pos = mouse_pos.get_pixel_perfect()

        hologram_rect_surf : Surface = Surface((self.selected_placeable.rect.width, self.selected_placeable.rect.height))
        hologram_rect_surf.set_alpha(50)        
        hologram_rect_surf.fill((0,0,200,50))

        hologram : Surface = self.selected_placeable.surf.copy()
        hologram.set_alpha(150)
        hologram.fill((0,0,200,0),special_flags=BLEND_RGBA_ADD)

        win.blits([(hologram_rect_surf, pixel_perfect_mouse_pos), (hologram, pixel_perfect_mouse_pos)])

    def place(self, mouse_pos : Coord) -> Placeable:
        self.selected_placeable.move(mouse_pos)
        self.selected_placeable.placed = True
        self.in_build_mode = False
        return self.selected_placeable