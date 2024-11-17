class Coord:
    def __init__(self, room_num : int, xy : tuple[int] = (0,0)) -> None:
        '''coordinate system for all objects'''
        self.room_num = room_num
        self.__x, self.__y = xy
        self.__pixelSize = 6

    @property
    def x(self) -> int:
        return self.__x
    
    @x.setter
    def x(self, value : int):
        self.__x = value

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, value: int):
        self.__y = value
    
    @property
    def xy(self) -> tuple[int]:
        return (self.__x, self.__y)

    @xy.setter
    def xy(self, value : tuple[int]):
        self.__x, self.__y = value


    def get_pixel_perfect(self, flag : int = 0, pxl : int = 0) -> tuple[int]:
        '''Rounds down the coords to match with the pixel art 6*6 pixel size
        Use optional attribute flag = 1 to round up
        >>> Coord(x = 1900, y = 631).get_pixel_perfect
        (1896,630)'''
        if pxl == 12:
            x = self.x - (self.x % 12)
            y = self.y - (self.y % 12)
            return (x, y)
        if flag:
            x = self.x - (self.x % self.__pixelSize) + self.__pixelSize
            y = self.y - (self.y % self.__pixelSize) + self.__pixelSize
        else:
            x = self.x - (self.x % self.__pixelSize)
            y = self.y - (self.y % self.__pixelSize)
        return (x, y)
    
    def __eq__(self, value):
        if self.xy == value.xy and self.room_num == value.room_num:
            return True
        return False

    def copy(self):
        return Coord(self.room_num, self.xy)
    
    def __repr__(self):
        return str(self.__dict__)

# tests
if __name__ == '__main__':
    coord = Coord(1, (650, 700))
    print(coord)
    assert coord.get_pixel_perfect() == (648, 696)
    assert coord.get_pixel_perfect(1) == (654, 702)

    coord.y, coord.x = (20,30)
    coord.xy = (0,8)
    assert coord.x == 0 and coord.y == 8