from ships import ship, projectile
from math import sin, cos, atan2, pi, degrees, sqrt
import pygame


class Gunner(ship.Ship):
    def __init__(self, control):
        self.max_health = 200
        super().__init__(control)
        self.image = pygame.image.load('assets/Gunner.png')
        self.ships.ally_ships.append(self)
        self.rotation_speed = 1
        self.speed = 4

    def move(self):
        closest_ship, distance = self.find_closest(self.ships.enemy_ships + self.ships.ally_ships)
        if sqrt(distance) < 70:
            self.turn_away_from(closest_ship)
            self.forward()
        else:
            closest_enemy, distance = self.find_closest(self.ships.enemy_ships)
            if closest_enemy is None:
                if self.controller.moving is not None:
                    self.follow_mothership()
                else:
                    self.idle()
                return
            if self.facing(closest_enemy):
                self.shoot()
            else:
                self.turn_towards(closest_enemy)

            if sqrt(distance) > 100:
                self.forward()

    def shoot(self):
        if self.cool_down == 0:
            bullet = projectile.Projectile(self.angle, True, self.controller)
            x, y = self.container.position(self)
            x += (self.hitbox_radius + 5) * cos(self.angle + pi / 10)
            y += (self.hitbox_radius + 5) * sin(self.angle + pi / 10)
            self.container.board.add(bullet, x, y)
            bullet = projectile.Projectile(self.angle, True, self.controller)
            x, y = self.container.position(self)
            x += (self.hitbox_radius + 5) * cos(self.angle - pi / 10)
            y += (self.hitbox_radius + 5) * sin(self.angle - pi / 10)
            self.container.board.add(bullet, x, y)
            self.cool_down = 20
        else:
            self.cool_down -= 1
