import pygame as pg
from utils.coord import Coord
from objects.placeable import Placeable
from objects.patterns import Pattern
from ui.inputbox import InputBox
from ui.sprite import FRAME_PAINTING, invert_alpha, YES_BUTTON, NO_BUTTON, whiten
from ui.button import Button
from ui.confirmationpopup import ConfirmationPopup
from ui.infopopup import InfoPopup
from utils.fonts import TERMINAL_FONT
from math import sqrt, ceil
from objects.particlesspawner import CircleParticleSpawner, ParticleSpawner

COLORS = [(0,0,0), (255,255,255), (255,0,0), (0,0,255), (0,255,0)]

class Canva:
    def __init__(self, coord : Coord, game): 
        self.coord = coord

        self.size = (672,1020)
        self.surf = pg.Surface(self.size)
        self.bg_color = (236, 235, 222)
        self.surf.fill(self.bg_color)
        
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = self.coord.xy
        
        self.name_input = InputBox(1446, 210, 100, 50)
        self.confirm_button = Button((1556, 210), self.attempt_save, whiten(NO_BUTTON), NO_BUTTON) # Int is a callable placeholder.
        self.paint_button = Button((1556, 310), self.start_painting, whiten(YES_BUTTON), YES_BUTTON)

        self.color_buttons = self.init_color_buttons()
        
        from core.logic import Game
        self.game : Game = game

        self.name = "peinture"
        self.placed_patterns : list[Pattern] = []
        self.holded_pattern : Pattern = None

        self.total_price = 0
        self.total_beauty = 0

        self.current_color = (255,0,0)

    def change_color(self, color):
        self.current_color = color

    def init_color_buttons(self):
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
        scaled_surf = pg.transform.scale_by(self.surf.copy(),0.5).convert()
        FRAME_PAINTING.blit(scaled_surf,(12,12))
        placeable = Placeable(self.name, self.coord, FRAME_PAINTING.copy(), beauty=self.total_beauty, tag="decoration")
        self.reset()
        return placeable
    
    def check_price(self, price):
        if self.game.money - price >= 0:
            self.game.money -= price
            return True
        else:
            self.game.popups.append(InfoPopup("Vous n'avez pas assez d'argent pour peindre :("))
            self.game.sound_manager.incorrect.play()
            return False

    def get_price(self):
        self.total_price = 0
        for pattern in self.placed_patterns:
            self.total_price += pattern.price
        return self.total_price

    def add_to_beauty(self, patterns : list[Pattern]):
        for pattern in patterns:
            self.total_beauty += pattern.beauty
    
    def reset(self):
        self.__init__(self.coord, self.game)
    
    def get_round_mask(self, surface : pg.Surface, xy : tuple, circle_radius):
        circle_surf = pg.Surface((circle_radius * 2, circle_radius * 2), pg.SRCALPHA)
        pg.draw.circle(circle_surf, (255, 255, 255, 255), (circle_radius, circle_radius), circle_radius)

        circle_surf.blit(surface, (-xy[0], -xy[1]), special_flags=pg.BLEND_RGBA_MIN)
        return circle_surf
    
    def get_next_surf(self):
        next_surf = pg.Surface(self.size)
        next_surf = next_surf.convert_alpha()
        next_surf.fill((0,0,0,0))

        for pattern in self.placed_patterns:
            self.draw_pattern(next_surf, pattern)

        invert_alpha(next_surf)
        next_surf.fill(self.current_color+tuple([0]), special_flags=pg.BLEND_RGBA_MAX)
        return next_surf
    
    def start_anim(self, next_surf):

        circle_radius = 120
        step = 25
        optimal_corner = ceil((circle_radius-(circle_radius*sqrt(2)/2)))
        optimal_height = ceil(circle_radius*sqrt(2))
        width = (self.size[0]-(circle_radius+optimal_corner))

        paint_gun_pos = [-optimal_corner, -optimal_corner]

        center = Coord(0,(self.coord.x+paint_gun_pos[0]+circle_radius, self.coord.y+paint_gun_pos[1]+circle_radius))
        static_particles = CircleParticleSpawner(center, circle_radius, pg.Vector2(0,0), self.current_color, 600, density=50, dir_randomness=0, radius=(10,20))
        aura_particles = ParticleSpawner(center, pg.Vector2(0,0), self.current_color, 60, dir_randomness=2)


        self.game.particle_spawners[0] += [static_particles, aura_particles]
        #order is inversed as it is a stack
        path_stack = [["R",width], ["D",optimal_height],["L",width],["D",optimal_height],
                      ["R",width],["D",optimal_height],["L",width], ["D",optimal_height],
                      ["R",width],["D",optimal_height],["L",width], ["D",optimal_height], ["R",width]]            
        current_dir = path_stack.pop()

        clock = pg.time.Clock()
        while path_stack:
            clock.tick(60)

            center.xy = (self.coord.x+paint_gun_pos[0]+circle_radius, self.coord.y+paint_gun_pos[1]+circle_radius)
            self.surf.blit(self.get_round_mask(next_surf, tuple(paint_gun_pos), circle_radius), paint_gun_pos)

            if current_dir[1] <= 0:
                current_dir = path_stack.pop()

            current_dir[1] -= step

            if current_dir[1] < 0:
                next_step = step + current_dir[1]
            else:
                next_step = step

            match current_dir[0]:
                case "R":
                    paint_gun_pos[0] += next_step
                case "L":
                    paint_gun_pos[0] -= next_step
                case "D":
                    paint_gun_pos[1] += next_step
            
            mouse_pos = Coord(0,pg.mouse.get_pos())
            self.game.update(mouse_pos)
            self.game.draw(mouse_pos)

            pg.display.flip()

        static_particles.active = False
        aura_particles.active = False

        self.game.timer.create_timer(5, self.game.particle_spawners[0].remove, arguments=[static_particles])
        self.game.timer.create_timer(5, self.game.particle_spawners[0].remove, arguments=[aura_particles])

    def start_painting(self):
        if self.check_price(self.get_price()):
            self.start_anim(self.get_next_surf())
            self.add_to_beauty(self.placed_patterns)
    
    def draw_pattern(self, surf, pattern : Pattern):
        """Imprints the pattern on the canva."""
        relative_pos = (pattern.rect.x - self.coord.x,
                        pattern.rect.y - self.coord.y)

        surf.blit(pattern.get_effect(), relative_pos)

    def place_pattern(self, pattern : Pattern):
        """Place a moveable pattern."""
        self.placed_patterns.append(pattern)
        self.get_price()

    def hold_pattern(self, pattern):
        self.placed_patterns.remove(pattern)
        self.get_price()
        self.holded_pattern = pattern
        self.holded_pattern.rect.center = pg.mouse.get_pos()
        self.game.sound_manager.items.play()
    
    def drop_pattern(self, pos):
        if self.rect.collidepoint(pos):
            self.holded_pattern.rect.center = pos
            self.place_pattern(self.holded_pattern)
            self.game.sound_manager.items.play()
        else:
            self.game.popups.append(InfoPopup("Vous reposez le pochoir dans l'armoire."))
        self.holded_pattern = None

    def attempt_save(self):
        self.name = self.name_input.text
        self.game.confirmation_popups.append(ConfirmationPopup(self.game.win, "are you sure you want to save the canva ?", self.game.save_canva))

    def draw(self, win):
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

    def handle_event(self, event):
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
            