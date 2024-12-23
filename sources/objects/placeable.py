from pygame import Surface, Rect, transform, BLEND_RGBA_MAX, BLEND_RGBA_MIN, SRCALPHA
import sys
import os
from random import randint
#do not remove
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.coord import Coord
from utils.anim import Animation
from ui.sprite import get_outline

class Placeable:
    def __init__(self, name: str, coord: Coord, surf: Surface, tag: str | None = None, anim: Animation | None = None, y_constraint: int | None = None, temporary: bool = False) -> None:
        self.name = name
        self.id = randint(0, 10000000)  # Generates a random ID for the Placeable instance
        self.coord = coord
        self.coord.xy = self.coord.get_pixel_perfect()  # Obtains pixel-perfect coordinates
        self.coord.x, self.coord.y = self.coord.xy

        # Select either the animation frame or the provided surface for rendering
        if anim:
            self.surf = anim.get_frame()
        else:
            self.surf = surf
        self.anim = anim
        self.temp_surf = self.surf.copy()  # Create a temporary copy of the surface

        self.tag = tag

        self.rect: Rect = self.surf.get_rect()  # Get the rectangular area of the surface
        self.rect.x, self.rect.y = self.coord.xy  # Set rectangle's position
        self.temp_rect = self.rect.copy()

        # Snap to x-axis if a y_constraint is provided
        self.y_constraint = y_constraint
        self.placed = False  # Indicates if the Placeable object has been placed

        self.temporary = temporary  # Indicates whether the Placeable object is temporary

    def get_blit_args(self):
        """Returns the surface and rectangle for blitting."""
        return self.temp_surf, self.temp_rect

    def draw_outline(self, win: Surface, color: tuple):
        """Draws an outline around the surface on the given window."""
        win.blit(get_outline(self.surf, color), (self.rect.x-3, self.rect.y-3))
    
    def move(self, coord: Coord):
        """Updates the position of the Placeable object based on new coordinates."""
        self.coord = coord
        self.coord.xy = coord.get_pixel_perfect()  # Ensure the coordinates are pixel-perfect
        self.rect.topleft = self.coord.xy  # Update the rectangle's position

    def pixelise(self):
        """Applies a pixel art shader effect by scaling the surface down and then back up."""
        self.surf = transform.scale_by(self.surf, 1/6)
        self.surf = transform.scale_by(self.surf, 6)

    def __repr__(self) -> str:
        """Returns a string representation of the Placeable object."""
        return str(self.__dict__)
    
    def interaction(self, args):
        """Placeholder method for interaction logic; meant to be overridden in subclasses."""
        pass

    def update_sprite(self, is_hovered: bool, color: tuple = (150, 150, 255)):
        """Updates the sprite based on hover state and modifies visual aspects if necessary."""
        if self.anim:
            self.surf = self.anim.get_frame()  # Update the surface if an animation is used

        if is_hovered:
            # Create an outline if the sprite is hovered over
            self.temp_surf = get_outline(self.surf, color)
            self.temp_surf.blit(self.surf, (3, 3))  # Blit the original surface onto the outline
            self.temp_rect = self.rect.copy()
            self.temp_rect.x -= 3  # Adjust position for outline
            self.temp_rect.y -= 3
        else:
            self.temp_surf = self.surf.copy()  # Use the normal surface when not hovered
            self.temp_rect = self.rect.copy()  # Retain original rectangle dimensions
    
    def set_attribute(self, attribute_name, value):
        """Dynamically sets an attribute if it exists; raises an attribute error otherwise."""
        if hasattr(self, attribute_name):  # Check if the attribute exists
            setattr(self, attribute_name, value)  # Dynamically set the attribute
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{attribute_name}'")

# tests
if __name__ == '__main__':
    placeholder_surf = Surface((60, 60))  # Create a new surface for testing
    placeholder_surf.fill('red')  # Fill the surface with red color
    painting = Placeable('skibidi', Coord(1, (650, 125)), placeholder_surf)  # Create a Placeable instance
    print(painting)  # Output the string representation of the Placeable instance
