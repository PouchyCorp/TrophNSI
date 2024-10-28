from pygame import image, Surface, transform

def load_image(path : str):
    sprite = image.load(path).convert()
    sized_sprite = transform.scale_by(sprite, 6)
    return sized_sprite

BG1 = load_image("data/bg_test_1.png")

BG2 = load_image("data/bg_test_2.png")

P1 = load_image('data/p1.png')

P2 = load_image('data/p2.png')
 
P3 = load_image('data/p3.png')

ICON_1 = load_image('data/icon_inventaire.png')