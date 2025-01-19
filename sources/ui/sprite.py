from pygame import image, Surface, transform, SRCALPHA, BLEND_RGBA_MAX, display, Rect, BLEND_RGB_ADD
from math import sin, pi
import utils.anim as anim

if not display.get_init():
    display.set_mode((0,0))

def load_image(path : str):
    sprite = image.load(path)
    sized_sprite = transform.scale_by(sprite, 6)
    return sized_sprite.convert_alpha()

def whiten(surface : Surface):
    dest_surf = surface.copy()
    dest_surf.fill((60,60,60), special_flags=BLEND_RGB_ADD)
    return dest_surf

def nine_slice_scaling(surface, target_size, margins):
    """
    Scale an image using nine-slice scaling.
    
    Parameters:
        image (pygame.Surface): The original image.
        target_size (tuple): The (width, height) of the scaled image.
        margins (tuple): The (left, right, top, bottom) margins for the slices.
    
    Returns:
        pygame.Surface: The scaled image.
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
    outline_width = 3

    width, height = surf.get_size()
    outline_surface = Surface((width + outline_width * 2, height + outline_width * 2), SRCALPHA)

    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if abs(dx) + abs(dy) == outline_width:
                outline_surface.blit(surf, (dx + outline_width, dy + outline_width))

    outline_surface.fill(color+tuple([0]), special_flags=BLEND_RGBA_MAX)
    return outline_surface


def fondu(surf : Surface, incr ,speed) -> Surface:
    """speed is a float between 0 and 1"""
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

P1 = load_image('data/p1.png')

P2 = load_image('data/p2.png')
 
P3 = load_image('data/p3.png')

P4 = load_image('data/p4.png')

P5 = load_image('data/p5.png')

ICON_1 = load_image('data/icon_inv_test.png')

CHIP = load_image('data/chip.png')

SPRITESHEET_INVENTORY = anim.Spritesheet(load_image('data/etagere.png'), (53*6, 31*6))

SPRITESHEET_BOT = anim.Spritesheet(load_image('data/test_robot.png'), (48*6, 48*6))

SPRITESHEET_HAUT = anim.Spritesheet(load_image("data/prt_haut.png"), (42*6, 29*6))

SPRITESHEET_BAS = anim.Spritesheet(load_image("data/prt_bas.png"), (42*6, 29*6))

SPRITESHEET_DOOR_BLINK = anim.Spritesheet(load_image("data/prt_anim_blink.png"), (42*6, 29*6))

PROP_STATUE = load_image('data/props_statue.png')

SPRITESHEET_HAUT_FLIP = anim.Spritesheet(transform.flip(load_image("data/prt_haut.png"),False, True), (42*6, 29*6))

SPRITESHEET_BAS_FLIP = anim.Spritesheet(transform.flip(load_image("data/prt_bas.png"),False, True), (42*6, 29*6))

SPRITESHEET_DOOR_BLINK_FLIP = anim.Spritesheet(transform.flip(load_image("data/prt_anim_blink.png"),False, True), (42*6, 29*6))

WINDOW = load_image('data/bord.png')

SPRITESHEET_CHIP = anim.Spritesheet(load_image('data/chip.png'), (48*6, 48*6))

#---------------------------------------------
#       The format for the robot anim is:
#line 1 - Walk Right
#line 2 - Walk Left
#line 3 - Idle Right
#line 4 - Watch Wall
#---------------------------------------------

SPRITESHEET_ROBOT_1_PACK = (anim.Spritesheet(load_image('data/robots/robot_1.png'),(24*6,46*6)), [8, 8, 8, 8])

SPRITESHEET_ROBOT_2_PACK = (anim.Spritesheet(load_image('data/robots/robot_2.png'),(31*6,43*6)), [8, 8, 8, 8])

SPRITESHEET_ROBOT_3_PACK = (anim.Spritesheet(load_image('data/robots/robot_3.png'),(27*6,39*6)), [14, 14, 11, 17])

SPRITESHEET_ROBOT_4_PACK = (anim.Spritesheet(load_image('data/robots/robot_4.png'),(26*6,38*6)), [8, 8, 8, 8])

SPRITESHEET_ROBOT_5_PACK = (anim.Spritesheet(load_image('data/robots/robot_5.png'),(31*6,48*6)), [8, 8, 8, 8])

SPRITESHEET_ROBOT_MUSIQUE_PACK = (anim.Spritesheet(load_image('data/robots/robot_musique.png'),(48*6,32*6)), [8])

LIST_SPRITESHEET_ROBOT = [SPRITESHEET_ROBOT_1_PACK, SPRITESHEET_ROBOT_2_PACK, SPRITESHEET_ROBOT_3_PACK, SPRITESHEET_ROBOT_4_PACK, SPRITESHEET_ROBOT_5_PACK]

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

REGISTER_BUTTON = load_image("data/register.png")

CONFIRM_BUTTON = load_image("data/confirm.png")

#---------------------------------------------
#       List of the different patterns
#---------------------------------------------

PATTERN_LIST = [load_image("data/pattern_storage/pattern_"+str(num)+".png") for num in range(1,15)]
