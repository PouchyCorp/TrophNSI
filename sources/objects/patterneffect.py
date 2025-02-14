from pygame import Surface, BLEND_RGBA_MIN

def placeholder(surface : Surface, color : tuple):
    surf = surface.copy()
    surf.fill(color, special_flags=BLEND_RGBA_MIN)
    return surf
