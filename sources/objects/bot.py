from enum import Enum, auto
from coord import Coord
from pygame import Surface
import sprite

class Bot_states(Enum):
    WAIT_INLINE = auto()
    IDLE = auto()
    WALK = auto()

possible_reaction = ['waw', 'bof', 'uwu', 'owo', 'noob']

class Hivemind:
    def __init__(self, line_start, line_stop) -> None:
        """supreme entity governing the bots
            All hail the hivemind"""
        self.bots : list[Bot | str] = ["empty","empty","empty","empty", "empty", "empty"]
        self.line_start = line_start
        self.line_stop = line_stop
        
        assert self.line_stop > self.line_start, "stop before start"

        step = (self.line_stop - self.line_start) // len(self.bots)
        self.x_lookup_table = [(step*i)+self.line_start for i in range(len(self.bots))]

        self.queued_bot_movement : dict[Bot: int] = {}
    
    def add_bot(self):
        if self.bots[0] is Bot:
            print("can't add another bot")
            return
        else:
            self.bots[0] = Bot(Coord(1, (self.line_start,700)))
    
    def free_last_bot(self):
        self.bots[-1] = "empty"
    
    def update_bot_orders(self):
        for bot in self.queued_bot_movement:
            bot.move_to(self.queued_bot_movement[bot])
        
    def order_bots(self):
        #print(self.bots)
        for i in range(len(self.bots)-1):
            if type(self.bots[i]) == Bot and type(self.bots[i+1]) != Bot:
                print(f"moving bot to {self.x_lookup_table[i+1]}")
                self.queued_bot_movement[self.bots[i]] = self.x_lookup_table[i+1]
                self.bots[i], self.bots[i+1] = self.bots[i+1], self.bots[i]
    
    def draw(self, win : Surface):
        for bot in self.bots:
            if type(bot) == Bot:
                bot.draw(win)

class Bot:
    def __init__(self, coord) -> None:
        self.coord = coord
        self.coord.xy = self.coord.get_pixel_perfect()
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

    def move_to(self, target_x):
        target_x -= target_x%6

        assert target_x%6 == 0, "destination not pixel-perfect"

        if self.__move_cntr >= 0:
            if self.coord.x < target_x:
                self.move_dir = "RIGHT"
                self.coord = Coord(self.coord.room_num, (self.coord.x+6, self.coord.y))

            elif self.coord.x > target_x:
                self.move_dir = "LEFT"
                self.coord = Coord(self.coord.room_num, (self.coord.x-6, self.coord.y))

            else:
                #do nothing if already on target
                return

            self.__move_cntr = 0

        else:
            self.__move_cntr += 1
            
    def react():
        pass

    def draw(self, win : Surface):
        win.blit(self.sprite, self.coord.xy)
    
    def __repr__(self):
        return str(self.__dict__)

#tests
#if __name__ == '__main__':
#    