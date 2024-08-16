import pygame as pg
import random

class Ground:
    ground_level = 500

    def __init__(self, win_width):
        self.x, self.y = 0, self.ground_level
        self.rect = pg.Rect(self.x, self.y, win_width, 5)

    def draw(self, window):
        pg.draw.rect(window, (255, 255, 255), self.rect)

class Pipe:
    width = 15
    opening = 100

    def __init__(self, win_width):
        self.x = win_width
        self.bottom_height = random.randint(10, 300)
        self.top_height = Ground.ground_level - self.bottom_height - self.opening
        self.bottom_rect, self.top_rect = pg.Rect(0, 0, 0, 0), pg.Rect(0, 0, 0, 0)
        self.passed = False
        self.off_screen = False

    def draw(self, window):
        self.bottom_rect = pg.Rect(self.x, Ground.ground_level - self.bottom_height, self.width, self.bottom_height)
        pg.draw.rect(window, (255, 255, 255), self.bottom_rect)

        self.top_rect = pg.Rect(self.x, 0, self.width, self.top_height)
        pg.draw.rect(window, (255, 255, 255), self.top_rect)

    def update(self):
        self.x -= 1
        if self.x + self.width <= 50:
            self.passed = True
        if self.x <= -self.width:
            self.off_screen = True

