from enum import Enum, auto
from coord import Coord
from pygame import Surface, draw, Rect
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
    def __init__(self, line_start : int, line_stop : int, TIMER : TimerManager) -> None:
        """supreme entity governing the bots
            All hail the hivemind,
            All hail the hivemind !"""
        self.inline_bots : list[Bot | str] = ["empty","empty","empty","empty", "empty", "empty"]
        self.liberated_bots : list[Bot] = []
        self.line_start_x = line_start
        self.line_stop_x = line_stop
        self.react_time_min, self.react_time_max = 1, 2
        self.bot_placeable_pointer : subplaceable.BotPlaceable = None

        assert self.line_stop_x > self.line_start_x, "stop before start"

        step = (self.line_stop_x - self.line_start_x) // len(self.inline_bots)
        self.x_lookup_table = [(step*i)+self.line_start_x for i in range(len(self.inline_bots))]
        TIMER.create_timer(randint(self.react_time_min,self.react_time_max),self.create_react_bot, arguments=[TIMER])

    def create_react_bot(self, TIMER : TimerManager):
        if self.liberated_bots:
            random_bot = choice(self.liberated_bots)
            random_bot.is_reacting = True
        TIMER.create_timer(randint(self.react_time_min,self.react_time_max),self.create_react_bot, arguments=[TIMER])

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
        
    
    def update_bots_ai(self, rooms, TIMER, clicked, mouse_pos, launch_dialogue_func):
        """
        Update the AI logic for the bots in the game.
        @param self - the object itself
        @param rooms - the rooms in the game
        @param TIMER - the game timer
        @param clicked - the clicked status
        @param mouse_pos - the position of the mouse
        @param launch_dialogue_func - the function to launch a dialogue
        @return None
        """
        for bot in [bot for bot in self.inline_bots if type(bot) is Bot]:
            bot.logic(rooms, TIMER, clicked, mouse_pos, launch_dialogue_func)

        new_liberated_bots = self.liberated_bots.copy()
        for bot in self.liberated_bots:
            bot.logic(rooms, TIMER, clicked, mouse_pos, launch_dialogue_func)
            #if bot not leaving and on exit, don't remove it
            if bot.is_leaving and bot.coord.bot_movement_compare(bot.exit_coords):
                new_liberated_bots.remove(bot)

        self.liberated_bots = new_liberated_bots
            

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
        if self.check_last_bot_idle() and not R1.name_exists_in_placed('bot_placeable'):
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
        self.rect = self.surf.get_rect()
        
        anim = Animation(sprite.SPRITESHEET_BOT, 0, 7)
        self.anim_idle = anim

        self.door_x = 1998
        self.exit_coords = Coord(1, (0,0))

        self.is_reacting = False


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

    def logic(self, rooms : list[Room], TIMER : TimerManager, clicked, mouse_pos, launch_dialogue_func):
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
                        TIMER.create_timer(1, self.set_attribute, False, arguments=('state', BotStates.IDLE))

                self.move_to_target_coord()
                self.surf = self.anim_idle.get_frame()

            case BotStates.WATCH:
                draw.rect(self.surf, "green", (0,0,10,10))

            case _:
                raise ValueError

        #checks if need to react
        self.react_logic(clicked, mouse_pos,launch_dialogue_func)

    def react_logic(self, clicked : bool, mouse_pos : Coord, launch_dialogue_func):
        #checks if mouse on self
        if self.is_reacting and self.coord.room_num == mouse_pos.room_num and Rect(self.coord.x, self.coord.y, self.rect.width, self.rect.height).collidepoint(mouse_pos.xy):
            #checks click
            self.is_mouse_on_self = True

            if clicked:
                self.is_reacting = False
                #launches the dialogue
                launch_dialogue_func(self.surf)

        else:
            self.is_mouse_on_self = False

    def update_placeable(self, rooms : list[Room]):
        self.placeable.rect.topleft = self.coord.xy
        self.placeable.surf = self.surf
                
        if self.placeable.coord.room_num != self.coord.room_num:
            self.remove_placeable(rooms)
            self.placeable.coord.room_num = self.coord.room_num
            self.add_placeable(rooms)

    def add_placeable(self, rooms : list[Room]):
        self.placeable = subplaceable.BotPlaceable('react_placeable', self.coord.copy(), self.surf)
        if self.placeable not in rooms[self.coord.room_num].placed:
            rooms[self.coord.room_num].placed.append(self.placeable)
        
    def remove_placeable(self, rooms : list[Room]):
        if self.placeable in rooms[self.placeable.coord.room_num].placed:
            rooms[self.placeable.coord.room_num].placed.remove(self.placeable)
    

                
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
        '''needs to be called after hivemind.update_bot_ai'''
        if self.is_mouse_on_self:
            temp_surf = sprite.get_outline(self.surf, (150, 150, 255))
            temp_surf.blit(self.surf, (3,3))
            win.blit(temp_surf, (self.coord.x-3, self.coord.y-3))
        else:
            win.blit(self.surf, self.coord.xy)
    
    def __repr__(self):
        return str(self.__dict__)

#tests
#if __name__ == '__main__':
#    