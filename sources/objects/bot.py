from enum import Enum, auto
from coord import Coord
from pygame import Surface, draw
from placeable import Placeable
from random import choice, randint
from room import Room
from room_config import R1
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
            self.inline_bots[-1].target_coord = Coord(2,(0,0))
            self.liberated_bots.append(self.inline_bots[-1])
            self.inline_bots[-1] = 'empty'
        
    
    def update_bots_ai(self, rooms):
        for bot in [bot for bot in self.inline_bots if type(bot) == Bot]:
            bot.logic(rooms)

        for bot in self.liberated_bots:
            bot.logic(rooms)

    def order_inline_bots(self):
        #print(self.bots)
        for i in range(len(self.inline_bots)-1):
            if type(self.inline_bots[i]) == Bot and type(self.inline_bots[i+1]) != Bot:
                #print(f"moving bot to {self.x_lookup_table[i+1]}")
                self.inline_bots[i].target_coord.x = self.x_lookup_table[i+1]+randint(-30,30)
                self.inline_bots[i], self.inline_bots[i+1] = self.inline_bots[i+1], self.inline_bots[i]

    def draw(self, win : Surface, current_room_num : int): 
        #list of background bots
        list_of_bots = [bot for bot in self.inline_bots if type(bot) == Bot] + self.liberated_bots
        sorted_bots = self.sorted_bot_by_y(list_of_bots)

        #draw bots in background first
        for bot in sorted_bots:
            if bot.coord.room_num == current_room_num:
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
    
    def check_last_bot_idle(self) -> bool:
        if type(self.inline_bots[-1]) == Bot:
            if self.inline_bots[-1].state is Bot_states.IDLE:
                return True
        return False


    def create_last_bot_clickable(self):
        #"not R1.name_exists('bot_placeable')" checks if bot placeable already exists
        if self.check_last_bot_idle() and not R1.name_exists_in_placed('bot_placeable'):
            last_bot : Bot = self.inline_bots[-1]
            assert type(last_bot) == Bot

            #creat a clickable to let robots enter
            bot_placeable = Placeable('bot_placeable', last_bot.coord, last_bot.surf)
            R1.placed.append(bot_placeable)
            R1.blacklist.append(bot_placeable)
        

class Bot:
    def __init__(self, coord : Coord) -> None:
        self.coord = coord
        self.coord.xy = self.coord.get_pixel_perfect()
        self.__target_coord = self.coord.copy()

        self.is_inline = True
        self.state = Bot_states.IDLE
        self.__move_cntr = 0
        self.move_dir = "RIGHT"
        self.surf = choice([sprite.P4,sprite.P5])

        self.door_x = 1716

    @property
    def target_coord(self):
        #makes sure that target coord is reachable
        self.__target_coord.x -= self.__target_coord.x%6
        return self.__target_coord
    
    @target_coord.setter
    def target_coord(self, value : Coord):
        self.__target_coord = value.copy()
        #makes sure that target coord is reachable
        self.__target_coord.x -= self.__target_coord.x%6

    def logic(self, rooms : frozenset[Room]):
        '''finite state machine (FSM) implementation for bot ai'''
        match self.state:
            case Bot_states.IDLE:
                draw.rect(self.surf, "red", (0,0,10,10))

                #search for objects to walk to
                potential_destinations : list[Coord] = []
                for room in rooms:
                    for placeable in room.placed:
                        if placeable.tag == "decoration":
                            potential_destinations.append(placeable.coord.copy())

                print(potential_destinations)
                self.target_coord = choice(potential_destinations)

                if self.coord.x != self.target_coord.x:
                    self.state = Bot_states.WALK

            case Bot_states.WALK:
                draw.rect(self.surf, "blue", (0,0,10,10))

                if self.coord.x == self.target_coord.x:
                    self.state = Bot_states.IDLE

                self.move_to_target_coord()
                #print(f'walking to x = {self.target_coord.x}')

            case _:
                raise Exception('bot should not have this state')

    def move_to_target_coord(self):

        #to keep final target coord during pathfinding modifications
        target_buffer = self.target_coord.copy()

        #change floor
        if self.coord.room_num < self.target_coord.room_num:
            if self.coord.x == self.door_x:
                self.coord.room_num = self.target_coord.room_num
            else:
                #if not on door, change target_buffer to door
                target_buffer.x = self.door_x


        #movement
        if self.__move_cntr >= 0:
            if self.coord.x < target_buffer.x:
                self.move_dir = "RIGHT"
                self.coord.x += 6

            elif self.coord.x > target_buffer.x:
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
        win.blit(self.surf, self.coord.xy)
    
    def __repr__(self):
        return str(self.__dict__)

#tests
#if __name__ == '__main__':
#    