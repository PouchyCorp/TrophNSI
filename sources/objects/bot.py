from enum import Enum, auto
from coord import Coord
import sprite

class Bot_states(Enum):
    WAIT_INLINE = auto()
    IDLE = auto()
    WALK = auto()

possible_reaction = ['waw', 'bof', 'uwu', 'owo', 'noob']

class Bot:
    def __init__(self) -> None:
        self.coord = Coord(1, (700,700))
        self.state = Bot_states.WAIT_INLINE
        self.__move_cntr = 0
        self.move_dir = "RIGHT"
        self.sprite = sprite.P3
        pass

    def logic(self, other_bots_inline, current_room):
        '''finite state machine (FSM) implementation for bot ai'''
        match self.state:
            case Bot_states.WAIT_INLINE:
                pass
            case Bot_states.IDLE:
                pass
            case Bot_states.WALK:
                pass
            case _:
                raise Exception('bot should not have this state')

    def wait_inline(self, other_bots_inline : list):
        pass

    def move_to(self, dest_x):
        if self.__move_cntr >= 10:
            self.coord = Coord(self.coord.room_num, (self.coord.x+6, self.coord.y))
        else:
            self.__move_cntr += 1
            
    def react():
        pass