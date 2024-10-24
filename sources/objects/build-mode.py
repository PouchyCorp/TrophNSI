from placeable import Placeable
from room import Room
from coord import Coord
from pygame import Surface

class Build_mode():
    def __init__(self, selected_placeable) -> None:
        self.selected_placeable : Placeable = selected_placeable
        self.in_build_mode : bool = False

    def show_hologram(self, win : Surface, mouse_pos : Coord):
        pass
    def place(self, current_room : Room):
        pass