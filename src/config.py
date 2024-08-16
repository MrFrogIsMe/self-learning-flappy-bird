import components
import pygame as pg

win_height = 720
win_width = 550
window = pg.display.set_mode((win_width, win_height))

gravity = 0.25

ground = components.Ground(win_width)
pipes = []
