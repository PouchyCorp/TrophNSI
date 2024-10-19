class Coord:
    def __init__(self, room : int, xy : tuple[int]) -> None:
        '''coordinate system for all objects'''
        self.room = room
        self.xy = xy
        self.x, self.y = xy
        self.pixelSize = 6

    def get_pixel_perfect(self, flag : int = 0) -> tuple[int]:
        '''Rounds down the coords to match with the pixel art 6*6 pixel size
        Use optional attribute flag = 1 to round up
        >>> Coord(x = 1900, y = 631).get_pixel_perfect
        (1896,630)'''
        if flag:
            x = self.x - (self.x % self.pixelSize) + self.pixelSize
            y = self.y - (self.y % self.pixelSize) + self.pixelSize
        else:
            x = self.x - (self.x % self.pixelSize)
            y = self.y - (self.y % self.pixelSize)
        return (x, y)
    
    def __repr__(self):
        return str(self.__dict__)

# tests
if False:
    coord = Coord(1, (650, 700))
    print(coord)
    assert coord.get_pixel_perfect() == (648, 696)
    assert coord.get_pixel_perfect(1) == (654, 702)