from pygame import image, Surface, transform

def load_image(path : str):
    sprite = image.load(path)
    sized_sprite = transform.scale_by(sprite, 6)
    return sized_sprite.convert_alpha()

BG1 = load_image("data/bg_test_approfondis.png")

P1 = load_image('data/p1.png')

P2 = load_image('data/p2.png')
 
P3 = load_image('data/p3.png')

ICON_1 = load_image('data/icon_inventaire.png')

CHIP = load_image('data/chip.png')