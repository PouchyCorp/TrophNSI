from pygame import Surface, SRCALPHA, image

class Spritesheet:
    def __init__(self, sprite : Surface, img_size : tuple[int]) -> None:
        self.surf = sprite
        self.rect = self.surf.get_rect()
        self.img_size = img_size

    def get_img(self, coord : tuple[int]) -> Surface:
        surf = Surface((self.img_size[0], self.img_size[1]), flags=SRCALPHA)
        coord_x_px = coord[0]*self.img_size[0] #take the last x-coord to calculate the next position
        coord_y_py = coord[1]*self.img_size[1] #take the last y-coord to calculate the next position
        surf.blit(self.surf, (0,0), (coord_x_px, coord_y_py, self.img_size[0], self.img_size[1]))
        return surf
    
    def __getstate__(self):
        state = self.__dict__
        state["surf"] = (image.tostring(self.surf, "RGBA"), self.surf.get_size())
        return state
    
    def __setstate__(self, state : dict):
        self.__dict__ = state
        self.surf = image.frombuffer(self.surf[0], self.surf[1], "RGBA") 


class Animation:
    def __init__(self, spritesheet : Spritesheet, line : int, length : int, speed : int = 6, repeat = True ) -> None:
        self.spritesheet = spritesheet
        self.img_index : int = 0
        self.line = line
        self.length = length
        self.speed = speed
        self.__speed_incr = 0
        self.repeat = repeat

    def get_frame(self) -> Surface:
        if self.img_index == self.length-1 and self.repeat:
            self.img_index = 0                  #reste to 0 the spritesheet
        
        if self.__speed_incr >= self.speed and self.img_index != self.length-1 :
            self.img_index += 1
            self.__speed_incr = 0           #setup the speed of the animation
        else:
            self.__speed_incr += 1
        
        new_surf = self.spritesheet.get_img((self.img_index, self.line))
        return new_surf
    
    def reset_frame(self):
        self.img_index = 0  

        new_surf = self.spritesheet.get_img((self.img_index, self.line))
        return new_surf
    
    def copy(self):
        return Animation(self.spritesheet,self.line,self.length,self.speed,self.repeat)

    def is_finished(self):
        if self.img_index == self.length-1 : #check if it's the last picture of the spritesheet
            return True
        

if __name__ == "__main__":
    print('launching tests')

    test = Spritesheet(Surface((10,10)),(1,1))
    
    import pickle
    
    pickled_data = pickle.dumps(test)

    unpickled_data = pickle.loads(pickled_data)

    print(unpickled_data.__dict__)
