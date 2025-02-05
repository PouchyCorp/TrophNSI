from pygame import Vector2, draw

class Particle:
    def __init__(self, coord, radius, direction : Vector2, color):
        self.coord = coord
        self.radius = radius 
        self.direction = direction
        self.color = color
        self.dead = False
        self.lifetime = 60

    def update(self):
        self.radius -= 0.1
        self.lifetime -= 0

        if self.lifetime <= 0 or self.radius <= 0:
            self.dead = True

        self.coord.x += self.direction.x
        self.coord.y += self.direction.y

    def draw_particle(self, win):
        draw.circle(win, self.color, self.coord, self.radius)


class ParticleSpawner:
    def __init__(self, coord : tuple, direction : Vector2, color : tuple, particle_lifetime : int, grav : bool = False, amount : int = None):
        self.coord = coord
        self.direction = direction
        self.color = color
        self.particle_lifetime = particle_lifetime
        self.grav = grav 
        self.particles : list[Particle] = []
        self.amount = amount
        self.finished = False
        self.amount = amount

    def spawn(self):
        if self.amount:
            for _ in range(self.amount):
                self.particles.append(Particle(self.coord, 50, self.direction, self.color))
            self.finished = True
        else:
            self.particles.append(Particle(self.coord, 50, self.direction, self.color))
            

    
    def update_all(self):
        for particle in self.particles:
            particle.update()

            if particle.dead:
                self.particles.remove(particle)

    def draw_all(self, win):
        for particle in self.particles:
            particle.draw_particle(win)