import random
import pygame as pg
import config
import brain

class Player:
    def __init__(self):
        # Bird
        self.x, self.y = 50, 200
        self.vel = 0
        self.rect = pg.Rect(self.x, self.y, 20, 20)
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)
        self.isFlapping = False
        self.isAlive = True
        self.lifespan = 0

        # AI
        self.decision = None
        self.vision = [0.5, 1, 0.5]
        self.fitness = 0
        self.inputs = 3
        self.brain = brain.Brain(self.inputs)
        self.brain.generate_net()

    def draw(self, window):
        pg.draw.rect(window, self.color, self.rect)

    def update(self):
        if not (self.ground_collision(config.ground.rect) or self.pipe_collision()):
            self.vel += config.gravity
            self.rect.y += self.vel
            if self.vel > 5:
                self.vel = 5
            # Increment lifespan
            self.lifespan += 1
        else:
            self.isAlive = False
            self.isFlapping = False
            self.vel = 0
            if self.ground_collision(config.ground.rect):
                self.rect.y = config.ground.rect.y - self.rect.height

    def flap(self):
        if not self.isFlapping and not self.sky_collision():
            self.isFlapping = True
            self.vel = -5
        if self.vel >= 2:
            self.isFlapping = False

    def ground_collision(self, ground):
        return pg.Rect.colliderect(self.rect, ground)

    def sky_collision(self):
        return bool(self.rect.y <= 30)

    def pipe_collision(self):
        for pipe in config.pipes:
            return pg.Rect.colliderect(self.rect, pipe.bottom_rect) or \
                   pg.Rect.colliderect(self.rect, pipe.top_rect)

    @staticmethod
    def closest_pipe():
        for p in config.pipes:
            if not p.passed:
                return p

    # AI related functions
    def look(self):
        if config.pipes:

            # Line to top pipe
            self.vision[0] = max(0, self.rect.center[1] - self.closest_pipe().top_rect.bottom) / 500
            pg.draw.line(config.window, self.color, self.rect.center, 
                         (self.rect.center[0], config.pipes[0].top_rect.bottom))

            # Line to mid pipe
            self.vision[1] = max(0, self.closest_pipe().x - self.rect.center[0]) / 500
            pg.draw.line(config.window, self.color, self.rect.center, 
                         (config.pipes[0].x, self.rect.center[1]))

            # Line to bottom pipe
            self.vision[2] = max(0, self.closest_pipe().bottom_rect.top - self.rect.center[1]) / 500
            pg.draw.line(config.window, self.color, self.rect.center, 
                         (self.rect.center[0], config.pipes[0].bottom_rect.top))

    def think(self):
        self.decision = self.brain.feed_forward(self.vision)
        if self.decision > 0.73:
            self.flap()

    def calculate_fitness(self):
        self.fitness = self.lifespan

    def clone(self):
        clone = Player()
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generate_net()
        return clone
