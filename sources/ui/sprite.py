r"""
   _____            _ _            
  / ____|          (_) |           
 | (___  _ __  _ __ _| |_ ___  ___ 
  \___ \| '_ \| '__| | __/ _ \/ __|
  ____) | |_) | |  | | ||  __/\__ \
 |_____/| .__/|_|  |_|\__\___||___/
        | |                        
        |_|                        

Key Features:
-------------
- Contains all the sprite assets used in the game.
- Nine-slice algorithm scaling for UI elements.
- Whiten effect for surfaces, to be used as activated button sprites (to avoid having unnecessary files).

"""


from pygame import image, Surface, transform, SRCALPHA, BLEND_RGBA_MAX, display, Rect, BLEND_RGB_ADD, BLEND_RGBA_MULT, Vector2, surfarray
from math import sin, pi
import utils.anim as anim
from objects.particlesspawner import ParticleSpawner, LineParticleSpawner
from utils.coord import Coord


if not display.get_init():
    display.set_mode((0,0))

def invert_alpha(surface):
    alpha_array = surfarray.pixels_alpha(surface)
    alpha_array[:] = 255 - alpha_array[:]  # Invert alpha values (0 <-> 255)
    del alpha_array

def load_image(path : str):
    sprite = image.load(path)
    sized_sprite = transform.scale_by(sprite, 6)
    return sized_sprite.convert_alpha()

def whiten(surface : Surface):
    """Whiten a surface to simulate a button press effect."""
    dest_surf = surface.copy()
    dest_surf.fill((60,60,60), special_flags=BLEND_RGB_ADD)
    return dest_surf

def nine_slice_scaling(surface, target_size, margins):
    """
    Scale an image using nine-slice scaling.
    
    Basically, the image is divided into 9 slices:
    - 4 corner slices (top-left, top-right, bottom-left, bottom-right) which keep their original size
    - 4 edge slices (top, bottom, left, right) which are stretched horizontally or vertically
    - 1 center slice which is stretched both horizontally and vertically

    This permits to scale the image to any size without distorting the corners and edges (allows stretchable patterns).
    """

    original_width, original_height = surface.get_size()
    target_width, target_height = target_size
    left, right, top, bottom = margins
    
    # Calculate the coordinates for the slices
    center_width = original_width - left - right
    center_height = original_height - top - bottom
    target_center_width = target_width - left - right
    target_center_height = target_height - top - bottom

    # Create a new surface for the scaled image
    scaled_image = Surface(target_size, SRCALPHA)
    
    # Define the slices
    slices = [
        (Rect(0, 0, left, top), (0, 0)),  # Top-left
        (Rect(left, 0, center_width, top), (left, 0, target_center_width, top)),  # Top-center
        (Rect(original_width - right, 0, right, top), (target_width - right, 0)),  # Top-right
        
        (Rect(0, top, left, center_height), (0, top, left, target_center_height)),  # Middle-left
        (Rect(left, top, center_width, center_height), (left, top, target_center_width, target_center_height)),  # Middle-center
        (Rect(original_width - right, top, right, center_height), (target_width - right, top, right, target_center_height)),  # Middle-right
        
        (Rect(0, original_height - bottom, left, bottom), (0, target_height - bottom)),  # Bottom-left
        (Rect(left, original_height - bottom, center_width, bottom), (left, target_height - bottom, target_center_width, bottom)),  # Bottom-center
        (Rect(original_width - right, original_height - bottom, right, bottom), (target_width - right, target_height - bottom)),  # Bottom-right
    ]
    
    # Blit each slice into the new surface
    for src_rect, dest_coords in slices:
        if len(dest_coords) == 2:
            # For corner slices (which have fixed size)
            dest_rect = Rect(dest_coords[0], dest_coords[1], src_rect.width, src_rect.height)
            scaled_image.blit(surface.subsurface(src_rect), dest_rect.topleft)
        else:
            # For scalable slices (center and edges)
            dest_rect = Rect(dest_coords[0], dest_coords[1], dest_coords[2], dest_coords[3])
            scaled_image.blit(transform.scale(surface.subsurface(src_rect), dest_rect.size), dest_rect.topleft)

    
    return scaled_image

def get_outline(surf, color):
    """Returns a surface with an outline around the input surface.
    Home-made algorithm, not the most efficient but it works."""
    outline_width = 3

    width, height = surf.get_size()
    outline_surface = Surface((width + outline_width * 2, height + outline_width * 2), SRCALPHA)

    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if abs(dx) + abs(dy) == outline_width:
                outline_surface.blit(surf, (dx + outline_width, dy + outline_width))

    outline_surface.fill(color+tuple([0]), special_flags=BLEND_RGBA_MAX)
    outline_surface.fill(color, special_flags=BLEND_RGBA_MULT)
    return outline_surface


def fondu(surf : Surface, incr ,speed) -> Surface:
    """Speed is a float between 0 and 1, incr is a float between 0 and pi.
    The function does a fade in/out effect on the surface using the sinus function."""
    if incr <= pi:
        speed = pi*speed
        rect = surf.get_rect()
        black_surf = Surface((rect.w, rect.h), SRCALPHA)
        color = (0,0,0,round(255*sin(incr)))
        black_surf.fill(color)
        surf.blit(black_surf, (0,0))

        incr += speed
    
    return incr


BG1 = load_image("data/bg_test_approfondis.png")

BG3 = load_image("data/R2.png")

BG4 = load_image("data/R3.png")

BG5 = load_image("data/R4.png")

BG6 = load_image("data/R5.png")

BG2 = load_image("data/bg_test_paint.png")

ICON_1 = load_image('data/icon_inv_test.png')

CHIP = load_image('data/chip.png')

SPRITESHEET_INVENTORY = anim.Spritesheet(load_image('data/etagere.png'), (53*6, 31*6))

SPRITESHEET_HAUT = anim.Spritesheet(load_image("data/prt_haut.png"), (42*6, 29*6))

SPRITESHEET_BAS = anim.Spritesheet(load_image("data/prt_bas.png"), (42*6, 29*6))

SPRITESHEET_DOOR_BLINK = anim.Spritesheet(load_image("data/prt_anim_blink.png"), (42*6, 29*6))

PROP_STATUE = load_image('data/props_statue.png')

SPRITESHEET_HAUT_FLIP = anim.Spritesheet(transform.flip(load_image("data/prt_haut.png"),False, True), (42*6, 29*6))

SPRITESHEET_BAS_FLIP = anim.Spritesheet(transform.flip(load_image("data/prt_bas.png"),False, True), (42*6, 29*6))

SPRITESHEET_DOOR_BLINK_FLIP = anim.Spritesheet(transform.flip(load_image("data/prt_anim_blink.png"),False, True), (42*6, 29*6))

WINDOW = load_image('data/bord.png')

SPRITESHEET_CHIP = anim.Spritesheet(load_image('data/chip.png'), (48*6, 48*6))

SPRITESHEET_ROOFTOP = anim.Spritesheet(load_image('data/rooftop.png'), (320*6,180*6))

#---------------------------------------------
#       The format for the robot anim is:
#line 1 - Walk Right
#line 2 - Walk Left
#line 3 - Idle Right
#line 4 - Watch Wall
#---------------------------------------------
#
#dict is the particle + the relative offset from the origin of the bot
#
#---------------------------------------------

dust = ParticleSpawner(Coord(0,(0,0)), Vector2(0,0), (50,50,50,100), 60, dir_randomness=2, density=1, speed=0.1)
none_particle = ParticleSpawner(Coord(0,(0,0)), Vector2(0,0), (0,0,0,0), 0, dir_randomness=0, density=0, speed=0)

SPRITESHEET_ROBOT_1_PACK = (anim.Spritesheet(load_image('data/robots/robot_1.png'),(24*6,46*6)), [8, 8, 8, 8],
                             {"right_dust" :(dust.copy(), (4*6,46*6)),
                              "left_dust" :(dust.copy(), (20*6,46*6)),
                              "light" :(ParticleSpawner(Coord(0,(0,0)), Vector2(0,0), (26,80,90,200), 60, dir_randomness=0, density=1, speed=0, radius=(4,4)), (13*6,30*6))})

SPRITESHEET_ROBOT_2_PACK = (anim.Spritesheet(load_image('data/robots/robot_2.png'),(31*6,43*6)), [8, 8, 8, 8],
                            {"right_dust" :(dust.copy(), (6*6,43*6)),
                              "left_dust" :(dust.copy(), (23*6,43*6))})

SPRITESHEET_ROBOT_3_PACK = (anim.Spritesheet(load_image('data/robots/robot_3.png'),(27*6,39*6)), [14, 14, 11, 17],
                            {"right_dust" :(dust.copy(), (4*6,39*6)),
                              "left_dust" :(dust.copy(), (21*6,39*6))})

SPRITESHEET_ROBOT_4_PACK = (anim.Spritesheet(load_image('data/robots/robot_4.png'),(26*6,38*6)), [8, 8, 8, 8],
                            {"right_dust" :(dust.copy(), (5*6,38*6)),
                              "left_dust" :(dust.copy(), (17*6,38*6))})

SPRITESHEET_ROBOT_5_PACK = (anim.Spritesheet(load_image('data/robots/robot_5.png'),(31*6,48*6)), [8, 8, 8, 8],
                            {"right_dust" :(dust.copy(), (11*6,48*6)),
                              "left_dust" :(dust.copy(), (26*6,48*6))})

SPRITESHEET_ROBOT_6_PACK = (anim.Spritesheet(load_image('data/robots/robot_6.png'),(32*6,48*6)), [8, 8, 17, 23],
                            {"right_dust" :(none_particle.copy(), (11*6,48*6)),
                              "left_dust" :(none_particle.copy(), (26*6,48*6)),
                              "levitation" : (LineParticleSpawner(Coord(0,(0,0)), Vector2(1,0), Vector2(0,-1), (150,150,150,200), 25, dir_randomness=0, density=5, speed=1, radius=(4,4), line_length=96), (8*6, 48*6))})

SPRITESHEET_ROBOT_MUSIQUE_PACK = (anim.Spritesheet(load_image('data/robots/robot_musique.png'),(48*6,32*6)), [8])

LIST_SPRITESHEET_ROBOT = [SPRITESHEET_ROBOT_1_PACK, SPRITESHEET_ROBOT_2_PACK, SPRITESHEET_ROBOT_3_PACK, SPRITESHEET_ROBOT_4_PACK, SPRITESHEET_ROBOT_5_PACK, SPRITESHEET_ROBOT_6_PACK]

SPRITE_PLANT_1 = load_image("data/plant_2_39x38.png")

SPRITE_PLANT_2 = load_image("data/plant_3_28x48.png")

ARROW_LEFT = load_image("data/fleche_gauche.png")

ARROW_RIGHT  = load_image("data/fleche_droite.png")

DIALBOX = load_image("data/pop_up_dialogue.png")

EXCLAMATION_SPRITESHEET = anim.Spritesheet(load_image("data/exclamation_2x9.png"),(2*6,9*6))

YES_BUTTON = load_image("data/oui.png")

NO_BUTTON = load_image("data/non.png")

LOGIN_BUTTON = load_image("data/login.png")

QUIT_BUTTON = load_image("data/quit.png")

CLOSE_BUTTON = load_image("data/close.png")

REGISTER_BUTTON = load_image("data/register.png")

CONFIRM_BUTTON = load_image("data/confirm.png")

CHIP_BUTTON = load_image("data/chip_button.png")

BUILD_MODE_BORDER = load_image("data/bordure_construction.png")

DESTRUCTION_MODE_BORDER = load_image("data/destruction_bordure.png")

FRAME_PAINTING = load_image("data/cadre.png")
#---------------------------------------------
#       List of the different patterns
#---------------------------------------------

PATTERN_LIST = [load_image("data/pattern_storage/pattern_"+str(num)+".png") for num in range(1,16)]
