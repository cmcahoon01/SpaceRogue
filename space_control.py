from ui import UI
from ships.enemyA import EnemyA
import random
from math import sin, cos, atan2, pi, degrees, floor


class Ships:
    ally_ships = []
    enemy_ships = []
    ally_projectiles = []
    enemy_projectiles = []


ships = Ships()


class SpaceControl:
    def __init__(self, board, settings):
        self.board = board
        self.settings = settings
        self.ui = UI(self)
        self.ships = ships

        self.money = 75

        self.enemy_interval = 1100
        self.time_since_enemy = self.enemy_interval

    def draw(self, window):
        self.board.draw(window)
        self.ui.draw(window)

    def act(self):
        self.board.act()
        self.spawn_enemies()

    def add(self, ship_type, x, y):
        new_ship = ship_type(self)
        self.board.add(new_ship, x, y)

    def purchased(self, ship_type, distance=200):
        mother_ship = ships.ally_ships[0]
        x, y = mother_ship.container.position(mother_ship)
        angle = random.random() * 2 * pi
        dx, dy = distance * cos(angle), distance * sin(angle)
        new_ship = ship_type(self)
        self.board.add(new_ship, x + dx, y + dy)

    def spawn_enemies(self):
        if self.time_since_enemy == self.enemy_interval:
            self.purchased(EnemyA, 449)
            self.enemy_interval = floor(self.enemy_interval * 0.8) + 15
            self.time_since_enemy = 0
        self.time_since_enemy += 1
