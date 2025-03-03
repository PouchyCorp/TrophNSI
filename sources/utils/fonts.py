from pygame import font

font.init()

font_path = "data/PxPlus_IBM_VGA8.ttf"
font_size = 25
TERMINAL_FONT = font.Font(font_path, font_size)
TERMINAL_FONT_BIG = font.Font(font_path, font_size + 10)