from pygame import image, Surface, transform, SRCALPHA, BLEND_RGBA_MAX

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
    outline_width = 5

    width, height = surf.get_size()
    outline_surface = Surface((width + outline_width * 2, height + outline_width * 2), SRCALPHA)

    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if abs(dx) + abs(dy) == outline_width:
                outline_surface.blit(surf, (dx + outline_width, dy + outline_width))

    outline_surface.fill(color+tuple([0]), special_flags=BLEND_RGBA_MAX)
    return outline_surface

BG1 = load_image("data/bg_test_approfondis.png")

BG3 = load_image("data/room_2.png")

BG2 = load_image("data/bg_test_paint.png")

P1 = load_image('data/p1.png')

P2 = load_image('data/p2.png')
 
P3 = load_image('data/p3.png')

P4 = load_image('data/p4.png')

P5 = load_image('data/p5.png')

ICON_1 = load_image('data/icon_inv_test.png')

CHIP = load_image('data/chip.png')

SPRITESHEET_TEST = load_image('data/test_robot.png')

SPRTESHEET_PORTE = load_image('data/prte_anim.png')

ROUNDED_WINDOW_TEST = image.load('data/rounded_window.png').convert_alpha()
#ROUNDED_WINDOW_TEST = transform.smoothscale(ROUNDED_WINDOW_TEST,(600 ,ROUNDED_WINDOW_TEST.get_rect().height))
ROUNDED_WINDOW_TEST = nine_slice_scaling(ROUNDED_WINDOW_TEST, (600, 400), 70)

PATTERN_1 = load_image('data/pattern_storage/pattern_test.png')

PATTERN_LIST = [PATTERN_1 for k in range(7)]