from pygame import Vector2, draw
from utils.coord import Coord
from typing_extensions import Optional
from random import randint, uniform, choice
from colorsys import rgb_to_hls, hls_to_rgb

class Particle:
    def __init__(self, coord : Coord, radius : float, direction : Vector2, color : Optional[tuple], gravity = 0, lifetime = 60):
        self.coord = coord
        self.radius = radius 
        self.direction = direction
        self.color = color
        self.dead = False
        self.lifetime = lifetime
        self.gravity = gravity

    def update(self):
        self.radius -= 0.1
        self.lifetime -= 1
        self.direction.x -= self.gravity

        if self.lifetime <= 0 or self.radius <= 0:
            self.dead = True

        self.coord.x += self.direction.x
        self.coord.y += self.direction.y

    def draw_particle(self, win):
        #print(self.color)
        draw.circle(win, self.color, self.coord.xy, self.radius)


class ParticleSpawner:
    def __init__(self, coord : Coord, direction : Vector2, color : tuple, particle_lifetime : int,
                  gravity : bool = False, total_amount : int = None, speed : float = 5, dir_randomness = 0.5, density = 5):
        self.coord = coord
        if direction.magnitude(): #if null vector don't normalize
            self.direction = direction.normalize()
        else:
            self.direction = direction
        self.particle_lifetime = particle_lifetime
        self.gravity = gravity 
        self.particles : list[Particle] = []
        self.amount = total_amount
        self.finished = False
        self.active = True
        self.density = density
        self.speed = speed
        self.dir_randomness = dir_randomness*2

        #color lookup table
        self.color_lookup_table = []
        for i in range(10):
            hls_col = rgb_to_hls(*color[:3])
            rng_hls_col = (hls_col[0],hls_col[1]+(-40+i*8),hls_col[2])

            rng_rgb_col = hls_to_rgb(*rng_hls_col)+color[3:]
            rounded_rng_rgb_col = tuple([min(255,max(0,int(i))) for i in rng_rgb_col])
            self.color_lookup_table.append(rounded_rng_rgb_col)
        


    def spawn(self):
        if self.active:
            if self.amount:
                for _ in range(self.amount):
                    self.particles.append(self.get_particle())
                self.finished = True
            else:
                for _ in range(self.density):
                    self.particles.append(self.get_particle())
            

    def get_particle(self):
        rng_rad = randint(2,10)
        rng_dir = Vector2(self.direction.x + uniform(-self.dir_randomness, self.dir_randomness), 
                          self.direction.y + uniform(-self.dir_randomness, self.dir_randomness))
        
        if rng_dir.magnitude():
            rng_dir = rng_dir.normalize()*self.speed
        
        rng_col = choice(self.color_lookup_table)

        return Particle(self.coord.copy(), rng_rad, rng_dir, rng_col , self.gravity, self.particle_lifetime)
    
    def update_all(self):
        for particle in self.particles:
            particle.update()

            if particle.dead:
                self.particles.remove(particle)

    def draw_all(self, win):
        for particle in self.particles:
            particle.draw_particle(win)


class ConfettiSpawner(ParticleSpawner):
    def __init__(self, coord, particle_amount):
        self.coord = coord
        self.particles = []
        self.particle_amount = particle_amount
        self.finished = False
        self.finished_countdown = 600

    def spawn(self):
        if self.particle_amount > 0:
            for _ in range(5):
                coord = Coord(self.coord.room_num,(randint(0,1920),0))
                rng_rad = randint(5,15)
                rng_dir = Vector2(uniform(-0.2, 0.2), 
                                1 + uniform(-0.2, 0.2))
                rng_dir = rng_dir.normalize()*7
                rng_col = (randint(0,255),randint(0,255),randint(0,255))
                self.particle_amount-= 1
                self.particles.append(Particle(coord, rng_rad, rng_dir, rng_col , 0, 1000))
        else:
            self.finished_countdown -= 1
        
        if self.finished_countdown <= 0:
            self.finished = True

        
    