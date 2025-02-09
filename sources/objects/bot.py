r"""
  _           _         _ _     _        _ _           _             
 | |         | |       | (_)   | |      (_) |         | |            
 | |__   ___ | |_    __| |_ ___| |_ _ __ _| |__  _   _| |_ ___  _ __ 
 | '_ \ / _ \| __|  / _` | / __| __| '__| | '_ \| | | | __/ _ \| '__|
 | |_) | (_) | |_  | (_| | \__ \ |_| |  | | |_) | |_| | || (_) | |   
 |_.__/ \___/ \__|  \__,_|_|___/\__|_|  |_|_.__/ \__,_|\__\___/|_|   

 Key Features:
-------------
- Manages the distribution of bots based on theoretical gold and robot tiers.
- Calculates the proper amount of gold a player should be earning each seconds.
- Distributes bots of various tiers by deducting the appropriate gold.

  _     _                     _           _ 
 | |   (_)                   (_)         | |
 | |__  ___   _____ _ __ ___  _ _ __   __| |
 | '_ \| \ \ / / _ \ '_ ` _ \| | '_ \ / _` |
 | | | | |\ V /  __/ | | | | | | | | | (_| |
 |_| |_|_| \_/ \___|_| |_| |_|_|_| |_|\__,_|

 Key Features:
-------------
- Governs bot behaviors and interactions within the game world.
- Manages a list of inline bots and liberated bots.
- Controls bot spawning and logic updates.

  _           _   
 | |         | |  
 | |__   ___ | |_ 
 | '_ \ / _ \| __|
 | |_) | (_) | |_ 
 |_.__/ \___/ \__|

Key Features:
-------------
- Represents an individual bot with its own unique attributes and behavior.
- Implements a finite state machine (FSM) for bot actions (Idle, Walk, Watch).
- Full movement logic, including movement to specific coordinates and room transitions.
- Handles user interaction via mouse clicks, launching dialogues and reactions.
- Supports animation through sprite sheets for various actions.
"""


from enum import Enum, auto
from utils.coord import Coord
from pygame import Surface, draw, Rect, transform, Vector2
from random import choice, randint
from core.room import Room
from utils.room_config import R1
import ui.sprite as sprite
from utils.timermanager import TimerManager
from utils.anim import Animation, Spritesheet
from utils.sound import SoundManager
from objects.particlesspawner import ParticleSpawner
import objects.placeablesubclass as subplaceable

class BotStates(Enum):
    """Enumeration for the different states a bot can have."""
    IDLE = auto()
    WALK = auto()
    WATCH = auto()

class BotDistributor:
    """Manages the distribution of bots based on theoretical gold and robot tiers."""

    def __init__(self, game_timer: TimerManager, hivemind, game):
        """
        Initialize the BotDistributor.

        Args:
            game_timer (TimerManager): TimerManager instance for game timing.
            hivemind: The Hivemind controlling bots.
            game: The game instance.
        """
        self.theorical_gold: float = 0
        self.robot_tiers = [10, 20, 50, 100, 500, 1000]
        self.game_timer = game_timer
        self.hivemind = hivemind
        self.game = game

        self.game_timer.create_timer(0.25, self.add_to_theorical_gold, True)
        self.game_timer.create_timer(1, self.distribute_to_bot, True, repeat_time_interval=[0.75, 3])

    def add_to_theorical_gold(self):
        """
        Add gold based on the game's beauty attribute.
        Called periodically by a timer.
        """
        if not self.hivemind.is_line_full():
            gold_amount = (self.game.beauty) / 4
            self.theorical_gold += gold_amount

    def distribute_to_bot(self):
        """
        Distribute theoretical gold to create bots of various tiers.
        Handles tier prioritization and ensures proper timing.
        """
        for tier in reversed(self.robot_tiers):
            amount_mod: int = int(self.theorical_gold / tier)

            if 3 >= amount_mod >= 1:
                for j in range(amount_mod):
                    self.game_timer.create_timer(j * 0.5, self.hivemind.add_bot, False, [tier])
                    self.theorical_gold -= tier

            elif amount_mod >= 1 and self.robot_tiers.index(tier) == len(self.robot_tiers) - 1:
                for j in range(amount_mod):
                    self.game_timer.create_timer(j * 0.5, self.hivemind.add_bot, False, [tier])
                    self.theorical_gold -= tier
                return

class Hivemind:
    """Supreme entity governing bots' behavior and interactions."""

    def __init__(self, line_start: int, line_stop: int, TIMER: TimerManager, sound_manager : SoundManager) -> None:
        """
        Initialize the Hivemind.

        Args:
            line_start (int): X-coordinate of the line start.
            line_stop (int): X-coordinate of the line stop.
            TIMER (TimerManager): TimerManager instance for managing timers.
        """
        self.inline_bots: list[Bot | str] = ["empty", "empty", "empty", "empty", "empty", "empty"]
        self.liberated_bots: list[Bot] = []
        self.line_start_x = line_start
        self.line_stop_x = line_stop
        self.react_time_min, self.react_time_max = 30, 60
        self.bot_placeable_pointer: subplaceable.BotPlaceable = None
        self.sound_manager = sound_manager
        assert self.line_stop_x > self.line_start_x, "stop before start"

        step = (self.line_stop_x - self.line_start_x) // len(self.inline_bots)
        self.x_lookup_table = [(step * i) + self.line_start_x for i in range(len(self.inline_bots))]
        TIMER.create_timer(randint(self.react_time_min, self.react_time_max), self.create_react_bot, arguments=[TIMER])

    def create_react_bot(self, TIMER: TimerManager):
        """
        Periodically selects a random bot to react.

        Args:
            TIMER (TimerManager): TimerManager instance for managing timers.
        """
        if self.liberated_bots:
            random_bot = choice(self.liberated_bots)
            random_bot.is_reacting = True
        TIMER.create_timer(randint(self.react_time_min, self.react_time_max), self.create_react_bot, arguments=[TIMER])

    def get_random_bot_spritesheet(self) -> tuple[Spritesheet, list]:
        """
        Fetch a random bot spritesheet.

        Returns:
            tuple: A tuple containing the spritesheet and associated data.
        """
        spritesheet_choice = choice(sprite.LIST_SPRITESHEET_ROBOT)
        assert type(spritesheet_choice) is tuple
        return spritesheet_choice

    def add_bot(self, gold_amount: int = 10):
        """
        Add a bot to the inline bot list if space is available.

        Args:
            gold_amount (int): The amount of gold assigned to the bot.
        """
        if not self.is_line_full():
            spritesheet_args = self.get_random_bot_spritesheet()
            bot_sprite_height = spritesheet_args[0].img_size[0]
            self.inline_bots[0] = Bot(Coord(1, (self.line_start_x, 958 - bot_sprite_height + randint(-50, 50))),
                                      gold_amount, spritesheet_args[0], spritesheet_args[1], spritesheet_args[2])

    
    def free_last_bot(self, current_room):
        if type(self.inline_bots[-1]) is Bot:

            #Updates all the attributes needed to init a working bot.
            self.inline_bots[-1].is_inline = False
            self.inline_bots[-1].target_coord = Coord(2,(0,0))
            self.liberated_bots.append(self.inline_bots[-1])
            last_bot_money_amount = self.inline_bots[-1].gold_amount
            self.inline_bots[-1] = 'empty'
            self.remove_last_bot_clickable(current_room)

            #plays sound
            self.sound_manager.achieve.play()
            return last_bot_money_amount
        return False
        
    
    def update(self, rooms, TIMER):
        """
        Update the AI logic for the bots in the game.
        """
        for bot in [bot for bot in self.inline_bots if type(bot) is Bot]:
            bot.logic(rooms, TIMER)

        new_liberated_bots = self.liberated_bots.copy()
        for bot in self.liberated_bots:
            bot.logic(rooms, TIMER)
            #if bot not leaving and on exit, don't remove it
            if bot.is_leaving and bot.coord.bot_movement_compare(bot.exit_coords):
                new_liberated_bots.remove(bot)

        self.liberated_bots = new_liberated_bots
    
    def handle_bot_click(self, mouse_pos : Coord, launch_dialogue_func):
        for bot in self.liberated_bots:
            bot.handle_click(mouse_pos, launch_dialogue_func)
            

    def order_inline_bots(self):
        #print(self.bots)
        for i in range(len(self.inline_bots)-1):
            if type(self.inline_bots[i]) is Bot and type(self.inline_bots[i+1]) is not Bot:
                self.inline_bots[i].target_coord.x = self.x_lookup_table[i+1]+randint(-30,30)
                self.inline_bots[i], self.inline_bots[i+1] = self.inline_bots[i+1], self.inline_bots[i]

    def draw(self, win : Surface, current_room_num : int, mouse_pos: Coord, transparency_win): 
        #list of background bots
        list_of_bots = [bot for bot in self.inline_bots if type(bot) is Bot] + self.liberated_bots
        sorted_bots = self.sorted_bot_by_y(list_of_bots)

        #updates the placeable to follow the last bot's animation
        if self.bot_placeable_pointer and type(self.inline_bots[-1]) is Bot:
            self.bot_placeable_pointer.surf = self.inline_bots[-1].surf

        #draw bots in background first
        for bot in sorted_bots:
            if bot.coord.room_num == current_room_num:
                bot.particle_logic()
                bot.draw(win, mouse_pos, transparency_win)
    
    def sorted_bot_by_y(self, bots : list):
        """sorts bots depending on y axis, to be blited in the right order (to respect perspective when rendering)
        selection sort algorithm"""
        sorted_bots : list[Bot] = bots
        for k in range(len(sorted_bots)):
            val = sorted_bots[k].coord.y+sorted_bots[k].rect.h

            for i in range(k,len(sorted_bots)):
                comp_bot = sorted_bots[i].coord.y+sorted_bots[i].rect.h
                if comp_bot < val:
                    val = comp_bot
                    sorted_bots[k], sorted_bots[i] = sorted_bots[i], sorted_bots[k]
 
        return sorted_bots
    
    def first_bot_idle(self) -> bool:
        
        if type(self.inline_bots[-1]) is Bot:
            if self.inline_bots[-1].state is BotStates.IDLE:
                return True
        return False

    def is_line_full(self) -> bool:
        """
        Check if the bot line is full.

        Returns:
            bool: True if no empty spaces are available, False otherwise.
        """
        if type(self.inline_bots[0]) is Bot:
            if self.inline_bots[0].state is BotStates.IDLE:
                return True
        return False

    def create_last_bot_clickable(self):
        #"not R1.name_exists('bot_placeable')" checks if bot placeable already exists
        if self.first_bot_idle() and not R1.name_exists_in_placed('bot_placeable'):
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
    """Represents an individual bot with unique attributes and behavior."""

    def __init__(self, coord: Coord, gold_amount: int, anim_spritesheet: Spritesheet, spritesheet_lengths, particle_spawners: dict) -> None:
        """
        Initialize the Bot instance.

        Args:
            coord (Coord): Initial coordinates of the bot.
            gold_amount (int): Gold value associated with the bot.
            anim_spritesheet (Spritesheet): Spritesheet for the bot's animations.
            spritesheet_lengths (list): List of animation lengths for the bot.
            particle_spawners (dict): Dictionary of particle spawners for the bot.
        """
        self.coord = coord
        self.coord.xy = self.coord.get_pixel_perfect()
        self.__target_coord = self.coord.copy()
        self.visited_placeable_id: list[int] = []
        self.is_inline = True
        self.is_leaving = False
        self.state = BotStates.IDLE
        self.__move_cntr = 0
        self.move_dir = "RIGHT"

        self.anim_walk_right = Animation(anim_spritesheet, 0, spritesheet_lengths[0], 2)
        self.anim_walk_left = Animation(anim_spritesheet, 1, spritesheet_lengths[1], 2)
        self.anim_idle_right = Animation(anim_spritesheet, 2, spritesheet_lengths[2], 2)
        self.anim_watch = Animation(anim_spritesheet, 3, spritesheet_lengths[3], 6, False)
        self.exclamation_anim = Animation(sprite.EXCLAMATION_SPRITESHEET, 0, 9, 3)

        self.surf = self.anim_walk_right.get_frame()
        self.rect = self.surf.get_rect()

        self.particle_spawners: dict[str, tuple[ParticleSpawner, tuple]] = particle_spawners

        self.door_x = 1998
        self.exit_coords = Coord(1, (0, 0))

        self.is_reacting = False
        self.gold_amount = gold_amount

    @property
    def target_coord(self):
        self.__target_coord.x -= self.__target_coord.x % 6
        return self.__target_coord

    @target_coord.setter
    def target_coord(self, value: Coord):
        self.__target_coord = value.copy()
        self.__target_coord.x -= self.__target_coord.x % 6

    def logic(self, rooms: list[Room], TIMER: TimerManager):
        """
        Implements the finite state machine (FSM) for bot AI.

        Args:
            rooms (list[Room]): List of all rooms in the game environment.
            TIMER (TimerManager): Timer manager to handle timed events.
        """
        match self.state:
            case BotStates.IDLE:
                self.handle_idle_state(rooms)
            case BotStates.WALK:
                self.handle_walk_state(TIMER)
            case BotStates.WATCH:
                self.handle_watch_state()
            case _:
                raise ValueError

    def handle_idle_state(self, rooms: list[Room]):

        if not self.is_inline:
            self.search_for_destination(rooms)

        self.update_idle_animation()

        if (self.coord.x, self.coord.room_num) != (self.target_coord.x, self.target_coord.room_num):
            self.state = BotStates.WALK

    def handle_walk_state(self, TIMER: TimerManager):

        if self.coord.bot_movement_compare(self.target_coord):
            if self.is_inline:
                self.state = BotStates.IDLE
            else:
                self.state = BotStates.WATCH
                TIMER.create_timer(2.75, self.set_attribute, False, arguments=('state', BotStates.IDLE))
                TIMER.create_timer(2.75, self.anim_watch.reset_frame, False)

        self.move_to_target_coord()
        self.update_walk_animation()

    def handle_watch_state(self):
        self.surf = self.anim_watch.get_frame()

    def search_for_destination(self, rooms: list[Room]):
        potential_dests = self.get_potential_destinations(rooms)
        if potential_dests:
            destination = choice(potential_dests)
            self.target_coord = destination[0]
            self.visited_placeable_id.append(destination[1])
        else:
            self.is_leaving = True
            self.target_coord = self.exit_coords

    def update_idle_animation(self):
        match self.move_dir:
            case "RIGHT":
                self.surf = self.anim_idle_right.get_frame()
            case "LEFT":
                self.surf = transform.flip(self.anim_idle_right.get_frame(), False, True)

    def update_walk_animation(self):
        match self.move_dir:
            case "RIGHT":
                self.surf = self.anim_walk_right.get_frame()
            case "LEFT":
                self.surf = self.anim_walk_left.get_frame()

    def handle_click(self, mouse_pos: Coord, launch_dialogue_func):
        """
        Handles user interaction when the bot is clicked.

        Args:
            mouse_pos (Coord): Current mouse position.
            launch_dialogue_func (callable): Function to launch a dialogue with the bot.
        """
        if self.is_reacting and self.coord.room_num == mouse_pos.room_num and Rect(self.coord.x, self.coord.y, self.rect.width, self.rect.height).collidepoint(mouse_pos.xy):
            self.is_reacting = False
            launch_dialogue_func(self.anim_idle_right)

    def get_potential_destinations(self, rooms: list[Room]) -> list[tuple[Coord, str]]:
        """Returns a list of potential destinations for the robot according to some criteria."""
        potential_destinations = []
        for room in rooms:
            for placeable in room.placed:
                if placeable.tag == "decoration" and placeable.id not in self.visited_placeable_id:
                    placeable_center_coord = placeable.coord.copy()
                    placeable_center_coord.x += placeable.rect.width // 3
                    placeable_center_coord.x += randint(-placeable.rect.width // 3, placeable.rect.width // 3)
                    potential_destinations.append((placeable_center_coord, placeable.id))
        return potential_destinations

    def set_attribute(self, attribute_name, value):
        if hasattr(self, attribute_name):
            setattr(self, attribute_name, value)
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{attribute_name}'")

    def move_to_target_coord(self):
        target_buffer = self.target_coord.copy()

        if self.coord.room_num != self.target_coord.room_num:
            if self.coord.x == self.door_x:
                self.coord.room_num = self.target_coord.room_num
                for spawner_data in self.particle_spawners.values():
                    spawner_data[0].particles = []
            else:
                target_buffer.x = self.door_x

        if self.__move_cntr >= 1:
            if self.coord.x < target_buffer.x:
                self.move_dir = "RIGHT"
                self.coord.x += 6
            elif self.coord.x > target_buffer.x:
                self.move_dir = "LEFT"
                self.coord.x -= 6
            self.__move_cntr = 0
        else:
            self.__move_cntr += 1

    def particle_logic(self):
        for particle_data in self.particle_spawners.values():
            particle_data[0].coord = Coord(self.coord.room_num, (self.coord.x + particle_data[1][0], self.coord.y + particle_data[1][1]))
            particle_data[0].update_all()

        if self.move_dir == "LEFT" and self.state == BotStates.WALK:
            self.particle_spawners['left_dust'][0].spawn()
        elif self.move_dir == "RIGHT" and self.state == BotStates.WALK:
            self.particle_spawners['right_dust'][0].spawn()

        for key, particle_data in self.particle_spawners.items():
            if key not in ['left_dust', 'right_dust']:
                particle_data[0].spawn()

    def draw(self, win: Surface, mouse_pos: Coord, transparency_win: Surface):
        """Needs to be called after hivemind.update_bot_ai."""
        self.draw_outline_if_reacting(win, mouse_pos)
        self.draw_bot(win)
        self.draw_exclamation_if_reacting(win)
        self.draw_particles(transparency_win)

    def draw_outline_if_reacting(self, win: Surface, mouse_pos: Coord):
        if self.is_reacting and self.coord.room_num == mouse_pos.room_num and Rect(self.coord.x, self.coord.y, self.rect.width, self.rect.height).collidepoint(mouse_pos.xy):
            temp_surf = sprite.get_outline(self.surf, (170, 170, 230))
            temp_surf.blit(self.surf, (3, 3))
            win.blit(temp_surf, (self.coord.x - 3, self.coord.y - 3))

    def draw_bot(self, win: Surface):
        win.blit(self.surf, self.coord.xy)

    def draw_exclamation_if_reacting(self, win: Surface):
        if self.is_reacting:
            coord_over_head_of_bot = (self.coord.x + (self.surf.get_width() // 2) - 6, self.coord.y - 10 * 6)
            win.blit(self.exclamation_anim.get_frame(), coord_over_head_of_bot)

    def draw_particles(self, transparency_win: Surface):
        for particle_data in self.particle_spawners.values():
            particle_data[0].draw_all(transparency_win)

    def __repr__(self):
        return str(self.__dict__)

#tests
#if __name__ == '__main__':
#    