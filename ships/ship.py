import pygame
from math import sin, cos, atan2, pi, degrees, sqrt


class Ship:
    max_health = 1

    def __init__(self, control):
        self.controller = control
        self.angle = 0
        self.image = None
        self.container = None
        self.ships = self.controller.ships
        self.health = self.max_health
        self.has_moved = False

        self.hitbox_radius = 25
        self.cool_down = 0
        self.speed = 5
        self.rotation_speed = 1 / 10
        self.value = 0

    def draw(self, window, x, y):
        rotated_image = pygame.transform.rotate(self.image, degrees(-self.angle) - 90)
        rect = rotated_image.get_rect(center=self.image.get_rect(center=(x, y)).center)
        window.blit(rotated_image, rect)
        if self.health < self.max_health:
            rect = pygame.Rect(x - 30, y + self.hitbox_radius * 1.5, 60, 7)
            pygame.draw.rect(window, (89, 89, 89), rect)
            rect = pygame.Rect(x - 28, y + self.hitbox_radius * 1.5 + 1, 58 * (self.health / self.max_health), 5)
            pygame.draw.rect(window, (35, 196, 81), rect)

    def set_container(self, container):
        self.container = container

    def act(self, x, y):
        if self.health > 0:
            self.has_moved = False
            self.move()
        else:
            self.die()

    def move(self):
        pass

    def find_closest(self, targets):
        if self in targets:
            targets.remove(self)
        closest = None
        closest_distance = 999999999
        for ship in targets:
            distance = self.distance_squared(ship)
            if distance < closest_distance:
                closest = ship
                closest_distance = distance
        return closest, closest_distance

    def distance_squared(self, target):
        x, y = self.container.position(self)
        position = target.container.position(target)
        return (x - position[0]) ** 2 + (y - position[1]) ** 2

    def distance_to(self, target):
        return sqrt(self.distance_squared(target))

    def facing(self, target):
        threshold = pi / 100

        x, y = self.container.position(self)
        target_pos = target.container.position(target)
        dy, dx = target_pos[1] - y, target_pos[0] - x
        angle_to_t = self.correct_angle(atan2(dy, dx))
        difference = abs(angle_to_t - self.angle)
        return difference < threshold or difference > 2 * pi - threshold

    def turn_towards(self, target, away=1):
        target_pos = target.container.position(target)
        x, y = self.container.position(self)
        dy, dx = target_pos[1] - y, target_pos[0] - x
        angle_to_t = atan2(dy, dx)
        angle_to_t = self.correct_angle(angle_to_t)
        left_diff = self.angle - angle_to_t
        if left_diff < 0:
            left_diff = 2 * pi + left_diff
        if left_diff < pi:  # left turn
            self.angle -= self.rotation_speed / 20 * away  # away is negative if avoiding the target
        else:  # right turn
            self.angle += self.rotation_speed / 20 * away
        self.correct_angle()

    def turn_away_from(self, target):
        self.turn_towards(target, -1)

    def correct_angle(self, to_correct=None):
        if to_correct is not None:
            while to_correct < 0:
                to_correct += 2 * pi
            while to_correct >= 2 * pi:
                to_correct -= 2 * pi
            return to_correct
        else:
            while self.angle < 0:
                self.angle += 2 * pi
            while self.angle >= 2 * pi:
                self.angle -= 2 * pi

    def hit(self, hit_by):
        self.health -= hit_by.damage
        if self.health <= 0:
            self.die()

    def die(self):
        self.controller.money += self.value
        self.value = 0
        self.container.remove(self)
        if self in self.ships.enemy_ships:
            self.ships.enemy_ships.remove(self)
        if self in self.ships.ally_ships:
            self.ships.ally_ships.remove(self)
        if self in self.ships.enemy_projectiles:
            self.ships.enemy_projectiles.remove(self)
        if self in self.ships.ally_projectiles:
            self.ships.ally_projectiles.remove(self)

    def forward(self):
        if self.has_moved:
            return
        dx, dy = self.speed * cos(self.angle), self.speed * sin(self.angle)
        self.container.move(self, dx, dy)
        self.has_moved = True

    def idle(self):
        self.forward()
        self.angle -= self.rotation_speed / 40  # spin left
        self.correct_angle()
