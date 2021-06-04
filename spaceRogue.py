import pygame
from pygame.constants import *
import threading
import partitions
from boid import Boid
from math import pi
import random
from ships import mothership, enemyA, gunner, projectile, medic
from ui import UI
from space_control import SpaceControl

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class GameSettings:
    def __init__(self, fps, ups, board_size, scale):
        self.fps = fps
        self.ups = ups
        scale = 100
        self.dimensions = (16 * scale, 9 * scale)
        self.game_running = True
        self.display = True
        self.game_time = 0


def display_loop(window, settings, space_control):
    if settings.game_running:
        space_control.draw(window)
        pygame.display.flip()


def event_handler(events, settings, control):
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            settings.game_running = False
        elif event.type == KEYDOWN:
            if event.key == K_q:
                pygame.quit()
                settings.game_running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            control.ui.click(x, y)


def update_loop(settings, control):
    control.act()
    settings.game_time += 1
    time = 1 / settings.ups if settings.display else 0
    thread_update = threading.Timer(time, lambda: update_loop(settings, control))
    thread_update.start()


def run_simulation(settings):
    settings.game_running = True
    settings.game_time = 0
    window_pygame = None
    if settings.display:
        pygame.init()
        window_pygame = pygame.display.set_mode(settings.dimensions, 0, 32)
        pygame.display.set_caption('Boids')
    board = partitions.Board(settings.dimensions[0], settings.dimensions[1])
    space_control = SpaceControl(board, settings)
    add_ships(space_control)
    clock = pygame.time.Clock()
    thread_update = threading.Timer(1 / settings.ups, lambda: update_loop(settings, space_control))
    thread_update.start()
    while settings.game_running:
        if settings.display:
            event_handler(pygame.event.get(), settings, space_control)
            display_loop(window_pygame, settings, space_control)
        if settings.display:
            clock.tick(settings.fps)
    return settings.game_time


def add_ships(control):
    control.add(mothership.MotherShip, 800, 450)


if __name__ == "__main__":
    print(run_simulation(GameSettings(60, 60, (3, 3), 90)))
