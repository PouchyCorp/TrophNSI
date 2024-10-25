class Coord:
    def __init__(self, room_num : int, xy : tuple[int]) -> None:
        '''coordinate system for all objects'''
        self.room_num = room_num
        self.xy = xy
        self.x, self.y = xy
        self.__pixelSize = 6

    def get_pixel_perfect(self, flag : int = 0) -> tuple[int]:
        '''Rounds down the coords to match with the pixel art 6*6 pixel size
        Use optional attribute flag = 1 to round up
        >>> Coord(x = 1900, y = 631).get_pixel_perfect
        (1896,630)'''
        if flag:
            x = self.x - (self.x % self.__pixelSize) + self.__pixelSize
            y = self.y - (self.y % self.__pixelSize) + self.__pixelSize
        else:
            x = self.x - (self.x % self.__pixelSize)
            y = self.y - (self.y % self.__pixelSize)
        return (x, y)
    
    def __repr__(self):
        return str(self.__dict__)

# tests
if __name__ == '__main__':
    coord = Coord(1, (650, 700))
    print(coord)
    assert coord.get_pixel_perfect() == (648, 696)
    assert coord.get_pixel_perfect(1) == (654, 702)