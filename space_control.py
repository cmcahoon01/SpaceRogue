from ui import UI
from ships.enemyA import EnemyA
from ships.mothership import MotherShip
from camera import Camera
import random
from math import sin, cos, atan2, pi, degrees, floor, sqrt
from partitions import Board


class Ships:
    ally_ships = []
    enemy_ships = []
    ally_projectiles = []
    enemy_projectiles = []


ships = Ships()


def decode_ship_string(name):
    if name == "enemyA":
        return EnemyA


class SpaceControl:
    def __init__(self, settings, level):
        self.settings = settings
        self.level = level
        self.ui = UI(self)
        self.ships = ships

        self.money = level["starting_money"]
        self.level_progress = 0
        self.moving = None

        self.board = Board(level["size"][0], level["size"][1])

        cam = level["start_pos"]
        self.camera = Camera(self.board, cam[0], cam[1], level["size"])

        self.add(MotherShip, cam[0] + self.camera.width / 2, cam[1] + self.camera.height / 2)

    def draw(self, window):
        self.camera.draw(window)
        self.ui.draw(window)

    def act(self):
        self.camera.move()
        self.level_events()
        self.board.act()

    def add(self, ship_type, x, y, angle=0):
        new_ship = ship_type(self)
        self.board.add(new_ship, x, y)
        new_ship.angle = angle

    def purchased(self, ship_type, distance=200):
        mother_ship = ships.ally_ships[0]
        x, y = mother_ship.container.position(mother_ship)
        angle = random.random() * 2 * pi
        dx, dy = distance * cos(angle), distance * sin(angle)
        new_ship = ship_type(self)
        self.board.add(new_ship, x + dx, y + dy)

    def level_events(self):
        timeline = self.level["events"]
        ups = 30  # updates per second
        if str(self.level_progress / ups) not in timeline:
            self.level_progress += 1
            return
        current_event = timeline[str(self.level_progress / ups)]
        if current_event[0] == "wait":
            if len(self.ships.enemy_ships) == 0:
                self.level_progress += 1
        elif current_event[0] == "spawn":
            for spawn_code in current_event[1:]:
                ship_type = decode_ship_string(spawn_code[0])
                self.add(ship_type, spawn_code[1], spawn_code[2], spawn_code[3])
            self.level_progress += 1
        elif current_event[0] == "move":
            mother_ship = ships.ally_ships[0]
            ship_pos = mother_ship.container.position(mother_ship)
            target_pos = current_event[1]
            distance = sqrt((ship_pos[0] - target_pos[0]) ** 2 + (ship_pos[1] - target_pos[1]) ** 2)
            if distance < 5:
                self.moving = None
                self.level_progress += 1
            else:
                self.moving = target_pos
                # self.camera.center(ship_pos)
