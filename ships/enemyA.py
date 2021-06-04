from ships import ship, projectile
import pygame
from math import sin, cos, atan2, pi, degrees, sqrt


class EnemyA(ship.Ship):
    def __init__(self, control):
        self.max_health = 300
        super().__init__(control)
        self.image = pygame.image.load('assets/EnemyA.png')
        self.hitbox_radius = 25
        self.ships.enemy_ships.append(self)
        self.speed = 3
        self.rotation_speed = 1
        self.value = 75

    def move(self):
        closest_ally, distance = self.find_closest(self.ships.ally_ships)
        if closest_ally is None:
            return
        if not self.facing(closest_ally):
            self.turn_towards(closest_ally)
        if sqrt(distance) > 300:
            self.forward()
        elif self.facing(closest_ally):
            self.shoot()
            dx, dy = self.speed / 2 * cos(self.angle + pi / 2), self.speed * sin(self.angle + pi / 2) / 2
            self.container.move(self, dx, dy)
            self.angle -= self.rotation_speed / 20
        self.correct_angle()

    def shoot(self):
        if self.cool_down == 0:
            bullet = projectile.Projectile(self.angle, False, self.controller)
            x, y = self.container.position(self)
            x += (self.hitbox_radius + 5) * cos(self.angle)
            y += (self.hitbox_radius + 5) * sin(self.angle)
            self.container.board.add(bullet, x, y)
            self.cool_down = 30
        else:
            self.cool_down -= 1

