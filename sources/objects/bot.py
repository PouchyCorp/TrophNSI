from enum import Enum, auto
from coord import Coord
from pygame import Surface, draw, transform
from random import choice, randint
from room import Room
from room_config import R1
import sprite
from timermanager import TimerManager
from objects.anim import Animation
import objects.placeablesubclass as subplaceable

class BotStates(Enum):
    IDLE = auto()
    WALK = auto()
    WATCH = auto()

possible_reaction = ['waw', 'bof', 'uwu', 'owo', 'noob']

class Hivemind:
    def __init__(self, line_start : int, line_stop : int) -> None:
        """supreme entity governing the bots
            All hail the hivemind,
            All hail the hivemind !"""
        self.inline_bots : list[Bot | str] = ["empty","empty","empty","empty", "empty", "empty"]
        self.liberated_bots : list[Bot] = []
        self.line_start_x = line_start
        self.line_stop_x = line_stop
        
        self.bot_placeable_pointer : subplaceable.BotPlaceable = None
        self.react_bot_pointer : Bot = None
        self.react_bot_placeable : subplaceable.BotPlaceable = None

        assert self.line_stop_x > self.line_start_x, "stop before start"

        step = (self.line_stop_x - self.line_start_x) // len(self.inline_bots)
        self.x_lookup_table = [(step*i)+self.line_start_x for i in range(len(self.inline_bots))]

    def add_bot(self):
        #checks if last place is empty
        if type(self.inline_bots[0]) is not Bot:
            self.inline_bots[0] = Bot(Coord(1, (self.line_start_x,700+randint(-50,50))))
    
    def free_last_bot(self, current_room):
        if type(self.inline_bots[-1]) is Bot:
            self.inline_bots[-1].is_inline = False
            self.inline_bots[-1].target_coord = Coord(2,(0,0))
            self.liberated_bots.append(self.inline_bots[-1])
            self.inline_bots[-1] = 'empty'
            self.remove_last_bot_clickable(current_room)
        
    
    def update_bots_ai(self, rooms, TIMER, current_room : Room):
        for bot in [bot for bot in self.inline_bots if type(bot) is Bot]:
            bot.logic(rooms, TIMER)

        #random chance to trigger
        if not self.react_bot_pointer and self.liberated_bots:
            self.react_bot_pointer = choice(self.liberated_bots)
            self.create_react_placeable(current_room)
        
        new_liberated_bots = self.liberated_bots.copy()
        for bot in self.liberated_bots:
            bot.logic(rooms, TIMER)
            #if bot not leaving and on exit, don't remove it
            if bot.is_leaving and bot.coord.bot_movement_compare(bot.exit_coords):
                new_liberated_bots.remove(bot)
        self.liberated_bots = new_liberated_bots
        
        if self.react_bot_pointer and self.react_bot_placeable:
            self.react_bot_placeable.rect.topleft = self.react_bot_pointer.coord.xy
            self.react_bot_placeable.surf = self.react_bot_pointer.surf
        
        if self.react_bot_pointer:
            self.create_react_placeable(current_room)

    def order_inline_bots(self):
        #print(self.bots)
        for i in range(len(self.inline_bots)-1):
            if type(self.inline_bots[i]) is Bot and type(self.inline_bots[i+1]) is not Bot:
                #print(f"moving bot to {self.x_lookup_table[i+1]}")
                self.inline_bots[i].target_coord.x = self.x_lookup_table[i+1]+randint(-30,30)
                self.inline_bots[i], self.inline_bots[i+1] = self.inline_bots[i+1], self.inline_bots[i]

    def draw(self, win : Surface, current_room_num : int): 
        #list of background bots
        list_of_bots = [bot for bot in self.inline_bots if type(bot) is Bot] + self.liberated_bots
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
        if type(self.inline_bots[-1]) is Bot:
            if self.inline_bots[-1].state is BotStates.IDLE:
                return True
        return False


    def create_last_bot_clickable(self):
        #"not R1.name_exists('bot_placeable')" checks if bot placeable already exists
        if self.check_last_bot_idle() and not self.bot_placeable_pointer:
            last_bot : Bot = self.inline_bots[-1]
            assert type(last_bot) is Bot

            #create a clickable to let robots enter
            bot_placeable = subplaceable.BotPlaceable('bot_placeable', last_bot.coord, last_bot.surf)
            self.bot_placeable_pointer = bot_placeable
            R1.placed.append(bot_placeable)
            R1.blacklist.append(bot_placeable)
    
    def remove_last_bot_clickable(self, current_room : Room):
        if self.bot_placeable_pointer and self.bot_placeable_pointer in current_room.placed:
            current_room.placed.remove(self.bot_placeable_pointer)
            current_room.blacklist.remove(self.bot_placeable_pointer)
            self.bot_placeable_pointer = None

    def remove_react(self, current_room : Room):
        if self.react_bot_placeable and self.react_bot_placeable in current_room.placed:
            current_room.placed.remove(self.react_bot_placeable)
            current_room.blacklist.remove(self.react_bot_placeable)
            self.react_bot_placeable = None
    
    def create_react_placeable(self,current_room : Room):
        if self.react_bot_pointer:
            self.remove_react(current_room)
            self.react_bot_placeable = subplaceable.BotPlaceable('react_placeable', self.react_bot_pointer.coord, self.react_bot_pointer.surf)
            current_room.placed.append(self.react_bot_placeable)
            current_room.blacklist.append(self.react_bot_placeable)
        

class Bot:
    def __init__(self, coord : Coord) -> None:
        self.coord = coord
        self.coord.xy = self.coord.get_pixel_perfect()
        self.__target_coord = self.coord.copy()
        self.visited_placeable_id : list[int] = []

        self.is_inline = True
        self.is_leaving = False
        self.state = BotStates.IDLE
        self.__move_cntr = 0
        self.move_dir = "RIGHT"
        self.surf = choice([sprite.P4,sprite.P5]).copy()
        self.center_offset = self.surf.get_rect().width//2
        
        anim = Animation(sprite.SPRITESHEET_BOT, 0, 7)
        self.anim_idle = anim

        self.door_x = 1998
        self.exit_coords = Coord(1, (0,0))


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

    def logic(self, rooms : list[Room], TIMER : TimerManager):
        '''finite state machine (FSM) implementation for bot ai'''

        match self.state:
            case BotStates.IDLE:
                draw.rect(self.surf, "red", (0,0,10,10))
                

                #search for objects to walk to if not inline
                if not self.is_inline:
                    #if not inline, search for valid destination
                    #criteria : placeable have the tag "decoration"
                    #           placeable wasn't already visited
                    potential_dests = self.get_potential_destinations(rooms)
                    if potential_dests:
                        destination = choice(potential_dests)
                        self.target_coord = destination[0]
                        self.target_coord.x += randint(-28,28)
                        self.visited_placeable_id.append(destination[1])
                    
                    else:
                        #no valid destination -> leave
                        self.is_leaving = True
                        self.target_coord = self.exit_coords
                        
                if (self.coord.x, self.coord.room_num) != (self.target_coord.x, self.target_coord.room_num):
                    self.state = BotStates.WALK

            case BotStates.WALK:
                draw.rect(self.surf, "blue", (0,0,10,10))

                if self.coord.bot_movement_compare(self.target_coord):
                    if self.is_inline:
                        self.state = BotStates.IDLE
                    else:
                        self.state = BotStates.WATCH
                        TIMER.create_timer(5, self.set_attribute, False, arguments=('state', BotStates.IDLE))

                self.move_to_target_coord()
                self.surf = self.anim_idle.get_frame()
            case BotStates.WATCH:
                draw.rect(self.surf, "green", (0,0,10,10))
                

            case _:
                raise ValueError

    def get_potential_destinations(self, rooms : list[Room]) -> list[tuple[Coord, str]]:
        """returns a list of potential destinations for the robot according to some criteria"""
        potential_destinations = []
        for room in rooms:
            for placeable in room.placed:
                if placeable.tag == "decoration" and placeable.id not in self.visited_placeable_id:
                    potential_destinations.append((placeable.coord.copy(), placeable.id))
        return potential_destinations
    
    def set_attribute(self, attribute_name, value):
        if hasattr(self, attribute_name):  # check if the attribute exists
            setattr(self, attribute_name, value)  # dynamically set the attribute
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{attribute_name}'")

    def move_to_target_coord(self):

        #to keep final target coord during pathfinding modifications
        target_buffer = self.target_coord.copy()

        #change floor
        if self.coord.room_num != self.target_coord.room_num:
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

    def draw(self, win : Surface):
        win.blit(self.surf, self.coord.xy)
    
    def __repr__(self):
        return str(self.__dict__)

#tests
#if __name__ == '__main__':
#    