from pygame import Surface, SRCALPHA

class Spritesheet:
    def __init__(self, sprite : Surface, img_size : tuple[int]) -> None:
        self.spritesheet = sprite
        self.rect = self.spritesheet.get_rect()
        self.img_size = img_size

    def get_img(self, coord : tuple[int]) -> Surface:
        surf = Surface((self.img_size[0], self.img_size[1]), flags=SRCALPHA)
        coord_x_px = coord[0]*self.img_size[0]
        coord_y_py = coord[1]*self.img_size[1]
        surf.blit(self.spritesheet, (0,0), (coord_x_px, coord_y_py, self.img_size[0], self.img_size[1]))
        return surf


class Animation:
    def __init__(self, spritesheet : Spritesheet, line : int, length : int, speed : int = 6) -> None:
        self.spritesheet = spritesheet
        self.counter : int = 0
        self.line = line
        self.length = length
        self.speed = speed
        self.__speed_incr = 0
    
    def get_frame(self) -> Surface:
        if self.counter == self.length:
            self.counter = 0
        
        if self.__speed_incr >= self.speed:
            self.counter += 1
            self.__speed_incr = 0 
        else:
            self.__speed_incr += 1
        
        new_surf = self.spritesheet.get_img((self.counter, self.line))
        return new_surf