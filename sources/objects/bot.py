from enum import Enum, auto
from coord import Coord
from pygame import Surface
from random import choice, randint
import sprite


class Bot_states(Enum):
    IDLE = auto()
    WALK = auto()

possible_reaction = ['waw', 'bof', 'uwu', 'owo', 'noob']

class Hivemind:
    def __init__(self, line_start, line_stop) -> None:
        """supreme entity governing the bots
            All hail the hivemind,
            All hail the hivemind !"""
        self.inline_bots : list[Bot | str] = ["empty","empty","empty","empty", "empty", "empty"]
        self.liberated_bots : list[Bot] = []
        self.line_start = line_start
        self.line_stop = line_stop
        
        assert self.line_stop > self.line_start, "stop before start"

        step = (self.line_stop - self.line_start) // len(self.inline_bots)
        self.x_lookup_table = [(step*i)+self.line_start for i in range(len(self.inline_bots))]

    def add_bot(self):
        if type(self.inline_bots[0]) == Bot:
            print("can't add another bot")
            return
        else:
            self.inline_bots[0] = Bot(Coord(1, (self.line_start,700+randint(-50,50))))
    
    def free_last_bot(self):
        if type(self.inline_bots[-1]) == Bot:
            self.inline_bots[-1].is_inline == False
            self.inline_bots[-1].target_coord = Coord(1,(0,0))
            self.liberated_bots.append(self.inline_bots[-1])
            self.inline_bots[-1] = 'empty'
        
    
    def update_bot_orders(self):
        for bot in [bot for bot in self.inline_bots if type(bot) == Bot]:
            bot.logic()

        for bot in self.liberated_bots:
            bot.logic()

    def order_bots(self):
        #print(self.bots)
        for i in range(len(self.inline_bots)-1):
            if type(self.inline_bots[i]) == Bot and type(self.inline_bots[i+1]) != Bot:
                #print(f"moving bot to {self.x_lookup_table[i+1]}")
                self.inline_bots[i].target_coord.x = self.x_lookup_table[i+1]+randint(-100,100)
                self.inline_bots[i], self.inline_bots[i+1] = self.inline_bots[i+1], self.inline_bots[i]

    def draw(self, win : Surface): 
        #list of background bots
        list_of_bots = [bot for bot in self.inline_bots if type(bot) == Bot] + self.liberated_bots
        sorted_bots = self.sorted_bot_by_y(list_of_bots)

        #draw bots in background first
        for bot in sorted_bots:
            bot.draw(win)
    
    def sorted_bot_by_y(self, bots : list):
        sorted_bots : list[Bot] = bots
        for k in range(len(sorted_bots)):
            val = sorted_bots[k].coord.y

            for i in range(k,len(sorted_bots)):
                if sorted_bots[i].coord.y < val:
                    val = sorted_bots[i].coord.y
                    sorted_bots[k], sorted_bots[i] = sorted_bots[i], sorted_bots[k]

        return sorted_bots

class Bot:
    def __init__(self, coord : Coord) -> None:
        self.coord = coord
        self.coord.xy = self.coord.get_pixel_perfect()
        self.target_coord = self.coord.copy()

        self.is_inline = True
        self.state = Bot_states.IDLE
        self.__move_cntr = 0
        self.move_dir = "RIGHT"
        self.sprite = choice([sprite.P4,sprite.P5])

    def logic(self):
        '''finite state machine (FSM) implementation for bot ai'''
        match self.state, self.is_inline:
            case Bot_states.IDLE, True:
                if self.coord.x != self.target_coord.x:
                    self.state = Bot_states.WALK

            case Bot_states.WALK ,True:
                if self.coord.x == self.target_coord.x:
                    self.state = Bot_states.IDLE

                self.move_to(self.target_coord.x)
                #print(f'walking to x = {self.target_coord.x}')

            case Bot_states.IDLE, False:
                if self.coord.x != self.target_coord.x:
                    self.state = Bot_states.WALK

            case Bot_states.WALK ,False:
                if self.coord.x == self.target_coord.x:
                    self.state = Bot_states.IDLE

                self.move_to(self.target_coord.x)
                #print(f'walking to x = {self.target_coord.x}')

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
                self.coord.x += 6

            elif self.coord.x > target_x:
                self.move_dir = "LEFT"
                self.coord.x -= 6

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