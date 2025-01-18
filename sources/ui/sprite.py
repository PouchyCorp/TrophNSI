from pygame import image, Surface, transform, SRCALPHA, BLEND_RGBA_MAX, display
from math import sin, pi
import utils.anim as anim

if not display.get_init():
    display.set_mode((0,0))

def load_image(path : str):
    sprite = image.load(path)
    sized_sprite = transform.scale_by(sprite, 6)
    return sized_sprite.convert_alpha()

def nine_slice_scaling(surf : Surface, size : tuple[int], border : int) -> Surface:
    original_rect = surf.get_rect()
    target_surf = Surface(size, flags=SRCALPHA)
    target_rect = target_surf.get_rect()

    #need to resize the image width
    if original_rect.width != target_rect.width:

        left_slice_area = (0, 0, border, original_rect.height)
        left_slice = Surface((border, original_rect.height), flags=SRCALPHA)
        left_slice.blit(surf, (0, 0), left_slice_area)

        right_slice_area = (original_rect.width-border, 0, border, original_rect.height)
        right_slice = Surface((border, original_rect.height), flags=SRCALPHA)
        right_slice.blit(surf, (0, 0), right_slice_area)

        middle_slice_area = (border, 0, original_rect.width-(border*2), original_rect.height)
        middle_slice = Surface((original_rect.width-(border*2), original_rect.height), flags=SRCALPHA)
        middle_slice.blit(surf, (0, 0), middle_slice_area)

        #resize only middle slice horizontally
        middle_slice_new_width = target_rect.width-(border*2)
        middle_slice = transform.smoothscale(middle_slice, (middle_slice_new_width, original_rect.height))

        #blit all slices together
        target_surf.blits([(left_slice, (0,0)), (middle_slice, (border, 0)), (right_slice, (border+middle_slice_new_width,0))])
    
    #need to resize the image height
    if original_rect.height != target_rect.height:
        top_slice_area = (0, 0, target_rect.width, border)
        top_slice = Surface((target_rect.width, border), flags=SRCALPHA)
        top_slice.blit(target_surf, (0, 0), top_slice_area)

        bottom_slice_area = (0, original_rect.height-border, target_rect.width, border)
        bottom_slice = Surface((target_rect.width, border), flags=SRCALPHA)
        bottom_slice.blit(target_surf, (0, 0), bottom_slice_area)

        middle_slice_area = (0, border, target_rect.width, original_rect.height-(border*2))
        middle_slice = Surface((target_rect.width, original_rect.height-(border*2)), flags=SRCALPHA)
        middle_slice.blit(target_surf, (0, 0), middle_slice_area)

        #resize only middle slice vertically
        middle_slice_new_height = target_rect.height-(border*2)
        middle_slice = transform.smoothscale(middle_slice, (target_rect.width, middle_slice_new_height))

        #blit all slices together
        target_surf.blits([(top_slice, (0,0)), (middle_slice, (0, border)), (bottom_slice, (0,border+middle_slice_new_height))])
    return target_surf

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

SPRITESHEET_BOT = anim.Spritesheet(load_image('data/test_robot.png'), (48*6, 48*6))

SPRITESHEET_HAUT = anim.Spritesheet(load_image("data/prt_haut.png"), (42*6, 29*6))

SPRITESHEET_BAS = anim.Spritesheet(load_image("data/prt_bas.png"), (42*6, 29*6))

SPRITESHEET_DOOR_BLINK = anim.Spritesheet(load_image("data/prt_anim_blink.png"), (42*6, 29*6))

PROP_STATUE = load_image('data/props_statue.png')

SPRITESHEET_HAUT_FLIP = anim.Spritesheet(transform.flip(load_image("data/prt_haut.png"),False, True), (42*6, 29*6))

SPRITESHEET_BAS_FLIP = anim.Spritesheet(transform.flip(load_image("data/prt_bas.png"),False, True), (42*6, 29*6))

SPRITESHEET_DOOR_BLINK_FLIP = anim.Spritesheet(transform.flip(load_image("data/prt_anim_blink.png"),False, True), (42*6, 29*6))

BUTTON = load_image('data/button.png')

WINDOW = load_image('data/bord.png')

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