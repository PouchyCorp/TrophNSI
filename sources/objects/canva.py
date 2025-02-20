import pygame as pg
from utils.coord import Coord
from objects.placeable import Placeable
from objects.patterns import Pattern
from ui.inputbox import InputBox
from ui.sprite import FRAME_PAINTING, invert_alpha, YES_BUTTON, NO_BUTTON, whiten, ARM, SPRAYER, point_rotate, inverse_kinematics
from ui.button import Button
from ui.confirmationpopup import ConfirmationPopup
from ui.infopopup import InfoPopup
from utils.fonts import TERMINAL_FONT
from math import sqrt, ceil
from objects.particlesspawner import CircleParticleSpawner, ParticleSpawner

COLORS = [(0,0,0), (255,255,255), (255,0,0), (0,0,255), (0,255,0)]

class Canva:
    def __init__(self, coord : Coord, game): 
        """Initialize the Canva object with its properties and UI elements."""
        self.coord = coord

        self.size = (672,1020)
        self.surf = pg.Surface(self.size)
        self.bg_color = (236, 235, 222)
        self.surf.fill(self.bg_color)
        
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = self.coord.xy
        
        self.name_input = InputBox(1446, 210, 100, 50)
        self.confirm_button = Button((1556, 210), self.attempt_save, whiten(NO_BUTTON), NO_BUTTON)
        self.paint_button = Button((1556, 310), self.start_painting, whiten(YES_BUTTON), YES_BUTTON)

        self.color_buttons = self.init_color_buttons()
        
        from core.logic import Game
        self.game : Game = game

        self.name = "peinture"
        self.placed_patterns : list[Pattern] = []
        self.holded_pattern : Pattern = None

        self.total_price = 0
        self.total_beauty = 0

        self.arm_root = (522, 469)
        self.default_target = (605, 454)
        self.arm = {'surf' : ARM.copy(), 'len' : ARM.copy().get_size()[0], 'angle' : 0}
        self.forearm = {'surf' : ARM.copy(), 'len' : ARM.copy().get_size()[0], 'angle' : 0}
        self.arm['angle'], self.forearm['angle'] = inverse_kinematics(self.default_target, self.arm_root, self.arm['len'], self.forearm['len'])

        self.current_color = (255,0,0)

        self.animation_handler = CanvaAnimationHandler(self)

    def change_color(self, color):
        """Change the current color used for painting."""
        self.current_color = color

    def init_color_buttons(self):
        """Initialize the color selection buttons."""
        buttons : list[Button] = []
        size = (120,120)
        x = 12
        y = 384
        for color in COLORS:
            surf = pg.Surface(size)
            surf.fill(color)
            buttons.append(Button((x, y), self.change_color, whiten(surf), surf, [color]))
            y+=size[1]+12
        return buttons

    def get_placeable(self) -> Placeable:
        """Create and return a Placeable object from the current canvas."""
        scaled_surf = pg.transform.scale_by(self.surf.copy(),0.5).convert()
        FRAME_PAINTING.blit(scaled_surf,(12,12))
        placeable = Placeable(self.name, self.coord, FRAME_PAINTING.copy(), beauty=self.total_beauty, tag="decoration")
        self.reset()
        return placeable
    
    def check_price(self, price):
        """Check if the player has enough money to paint and deduct the price if possible."""
        if self.game.money - price >= 0:
            self.game.money -= price
            return True
        else:
            self.game.popups.append(InfoPopup("Vous n'avez pas assez d'argent pour peindre :("))
            self.game.sound_manager.incorrect.play()
            return False

    def get_price(self):
        """Calculate and return the total price of all placed patterns."""
        self.total_price = 0
        for pattern in self.placed_patterns:
            self.total_price += pattern.price
        return self.total_price

    def add_to_beauty(self, patterns : list[Pattern]):
        """Add the beauty value of the given patterns to the total beauty."""
        for pattern in patterns:
            self.total_beauty += pattern.beauty
    
    def reset(self):
        """Reset the canvas to its initial state."""
        self.__init__(self.coord, self.game)
    
    def get_round_mask(self, surface : pg.Surface, xy : tuple, circle_radius):
        """Create and return a circular mask for the given surface."""
        circle_surf = pg.Surface((circle_radius * 2, circle_radius * 2), pg.SRCALPHA)
        pg.draw.circle(circle_surf, (255, 255, 255, 255), (circle_radius, circle_radius), circle_radius)

        circle_surf.blit(surface, (-xy[0], -xy[1]), special_flags=pg.BLEND_RGBA_MIN)
        return circle_surf
    
    def get_next_surf(self):
        """Generate and return the next surface to be painted."""
        next_surf = pg.Surface(self.size)
        next_surf = next_surf.convert_alpha()
        next_surf.fill((0,0,0,0))

        for pattern in self.placed_patterns:
            self.draw_pattern(next_surf, pattern)

        invert_alpha(next_surf)
        next_surf.fill(self.current_color+tuple([0]), special_flags=pg.BLEND_RGBA_MAX)
        return next_surf
    
    def start_painting(self):
        """Start the painting process if the player has enough money."""
        if self.check_price(self.get_price()):
            self.animation_handler.start_anim(self.get_next_surf())
            self.add_to_beauty(self.placed_patterns)
    
    def draw_pattern(self, surf, pattern : Pattern):
        """Imprint the pattern on the given surface."""
        relative_pos = (pattern.rect.x - self.coord.x,
                        pattern.rect.y - self.coord.y)

        surf.blit(pattern.get_effect(), relative_pos)

    def place_pattern(self, pattern : Pattern):
        """Place a moveable pattern on the canvas."""
        self.placed_patterns.append(pattern)
        self.get_price()

    def hold_pattern(self, pattern):
        """Hold a pattern for moving."""
        self.placed_patterns.remove(pattern)
        self.get_price()
        self.holded_pattern = pattern
        self.holded_pattern.rect.center = pg.mouse.get_pos()
        self.game.sound_manager.items.play()
    
    def drop_pattern(self, pos):
        """Drop the held pattern at the given position."""
        if self.rect.collidepoint(pos):
            self.holded_pattern.rect.center = pos
            self.place_pattern(self.holded_pattern)
            self.game.sound_manager.items.play()
        else:
            self.game.popups.append(InfoPopup("Vous reposez le pochoir dans l'armoire."))
        self.holded_pattern = None

    def attempt_save(self):
        """Attempt to save the current canvas."""
        self.name = self.name_input.text
        self.game.confirmation_popups.append(ConfirmationPopup(self.game.win, "are you sure you want to save the canva ?", self.game.save_canva))

    def draw(self, win : pg.Surface):
        """Draw the canvas and its elements on the given window surface."""
        win.blit(self.surf, self.coord.xy)

        for placed_pattern in self.placed_patterns:
            placed_pattern.draw(win)
        
        if self.holded_pattern:
            self.holded_pattern.draw(win)
        
        win.blit(TERMINAL_FONT.render(f"Prix : {self.total_price} / Beauté totale : {self.total_beauty}", True, 'blue'), (1356, 110))

        self.name_input.draw(win)
        self.confirm_button.draw(win, self.confirm_button.rect.collidepoint(pg.mouse.get_pos()))
        self.paint_button.draw(win, self.paint_button.rect.collidepoint(pg.mouse.get_pos()))
        for button in self.color_buttons:
            button.draw(win, button.rect.collidepoint(pg.mouse.get_pos()))
        
        self.blit_arms(win)
    
    def blit_arms(self, win):
        """Draw the robotic arms on the given window surface."""
        rotated_surf, rect = point_rotate(self.arm['surf'], self.arm_root, (5,5), -self.arm['angle'])
        relative_arm_vector = pg.Vector2(self.arm['len'], 0)
        rotated_arm_vector = relative_arm_vector.rotate(self.arm['angle'])
        global_arm_end_pos = rotated_arm_vector + pg.Vector2(self.arm_root)

        rotated_surf2, rect2 = point_rotate(self.forearm['surf'], global_arm_end_pos, (5,5), -self.forearm['angle'])

        relative_forearm_vector = pg.Vector2(self.forearm['len'], 0)
        rotated_forearm_vector = relative_forearm_vector.rotate(self.forearm['angle'])
        global_forearm_end_pos = rotated_forearm_vector + rotated_arm_vector + pg.Vector2(self.arm_root)

        sprayer_rect = SPRAYER.get_rect(center = global_forearm_end_pos)

        win.blit(rotated_surf, rect)
        win.blit(rotated_surf2, rect2)
        win.blit(SPRAYER, sprayer_rect)

    def handle_event(self, event):
        """Handle user input events."""
        mouse_pos = pg.mouse.get_pos()

        self.name_input.handle_event(event)
        self.paint_button.handle_event(event)
        self.confirm_button.handle_event(event)
        
        for button in self.color_buttons:
            button.handle_event(event)


        eventual_collided_pattern = [pattern for pattern in self.placed_patterns if pattern.rect.collidepoint(mouse_pos)]
        if event.type == pg.MOUSEBUTTONDOWN and eventual_collided_pattern:
            self.hold_pattern(eventual_collided_pattern[0])

        
        if self.holded_pattern:
            if event.type == pg.MOUSEBUTTONUP:
                self.drop_pattern(mouse_pos)

            if event.type == pg.MOUSEMOTION:
                self.holded_pattern.rect.center = mouse_pos

        return False
    
class CanvaAnimationHandler:
    def __init__(self, canva):
        """Initialize the AnimationHandler with a reference to the Canva object."""
        self.canva : Canva = canva

    def start_anim(self, next_surf):
        """Start the painting animation with the given surface."""
        circle_radius = 120
        step = 25
        optimal_corner = ceil((circle_radius - (circle_radius * sqrt(2) / 2)))
        optimal_height = ceil(circle_radius * sqrt(2))
        width = (self.canva.size[0] - (circle_radius + optimal_corner))

        paint_gun_pos = [-optimal_corner-100, -optimal_corner+self.canva.size[1]//2]

        center = Coord(0, (self.canva.coord.x + paint_gun_pos[0] + circle_radius, self.canva.coord.y + paint_gun_pos[1] + circle_radius))
        static_particles, aura_particles = self.create_particles(center, circle_radius)

        self.canva.game.particle_spawners[0] += [static_particles, aura_particles]
        path_stack = self.create_path_stack(width, optimal_height)
        current_dir = path_stack.pop()
        

        active = False
        static_particles.active = False
        aura_particles.active = False
        
        true_next_surf = self.canva.surf.copy()
        true_next_surf.blit(next_surf, (0, 0))

        clock = pg.time.Clock()
        while path_stack or current_dir[1] > 0:
            clock.tick(60)

            if current_dir[1] <= 0:
                current_dir = path_stack.pop()

            if current_dir == 'toggle':
                active = not active
                static_particles.active = not static_particles.active
                aura_particles.active = not aura_particles.active
                current_dir = path_stack.pop()

            if active:
                self.canva.surf.blit(self.canva.get_round_mask(next_surf, tuple(paint_gun_pos), circle_radius), paint_gun_pos)

            current_dir[1] -= step

            next_step = step + current_dir[1] if current_dir[1] < 0 else step

            self.update_paint_gun_pos(current_dir[0], paint_gun_pos, next_step)

            mouse_pos = Coord(0, pg.mouse.get_pos())
            center.xy = (self.canva.coord.x + paint_gun_pos[0] + circle_radius, self.canva.coord.y + paint_gun_pos[1] + circle_radius)

            self.canva.game.update(mouse_pos)
            self.canva.game.draw(mouse_pos)
            self.canva.blit_arms(self.canva.game.win)

            self.canva.arm['angle'], self.canva.forearm['angle'] = inverse_kinematics(center.xy, self.canva.arm_root, self.canva.arm['len'], self.canva.forearm['len'])

            pg.display.flip()
            print(center.xy)

        self.canva.surf = true_next_surf
        static_particles.active = False
        aura_particles.active = False
        self.canva.game.timer.create_timer(5, self.canva.game.particle_spawners[0].remove, arguments=[static_particles])
        self.canva.game.timer.create_timer(5, self.canva.game.particle_spawners[0].remove, arguments=[aura_particles])

    def create_particles(self, center, circle_radius):
        """Create and return static and aura particle spawners."""
        static_particles = CircleParticleSpawner(center, circle_radius, pg.Vector2(0, 0), self.canva.current_color, 600, density=20, dir_randomness=0, radius=(10, 20))
        aura_particles = ParticleSpawner(center, pg.Vector2(0, 0), self.canva.current_color, 60, dir_randomness=2)
        return static_particles, aura_particles

    def create_path_stack(self, width, optimal_height):
        """Create and return the path stack for the painting animation."""
        return [["U", self.canva.size[1]//2], ["L", 100-25], 'toggle', ["L", width+25], ["D", optimal_height], ["R", width], ["D", optimal_height],
                ["L", width], ["D", optimal_height], ["R", width], ["D", optimal_height],
                ["L", width], ["D", optimal_height], ["R", width], 'toggle', ["R", 100], ["U", self.canva.size[1]//2]]

    def update_paint_gun_pos(self, direction, paint_gun_pos, step):
        """Update the paint gun position based on the current direction and step."""
        match direction:
            case "R":
                paint_gun_pos[0] += step
            case "L":
                paint_gun_pos[0] -= step
            case "D":
                paint_gun_pos[1] += step
            case "U":
                paint_gun_pos[1] -= step