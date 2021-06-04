from ships import ship, projectile
from math import sin, cos, atan2, pi, degrees, sqrt
import pygame


class MotherShip(ship.Ship):
    def __init__(self, control):
        self.max_health = 150
        super().__init__(control)
        self.image = pygame.image.load('assets/Mothership.png')
        self.ships.ally_ships.append(self)
        self.rotation_speed = 10 / 10
        self.speed = 0

    def move(self):
        closest_enemy, distance = self.find_closest(self.ships.enemy_ships)
        self.health += 0.1
        if closest_enemy is None:
            self.idle()
            return
        if self.facing(closest_enemy):
            self.shoot()
        else:
            self.turn_towards(closest_enemy)

    def shoot(self):
        if self.cool_down == 0:
            bullet = projectile.Projectile(self.angle, True, self.controller)
            x, y = self.container.position(self)
            x += (self.hitbox_radius + 5) * cos(self.angle)
            y += (self.hitbox_radius + 5) * sin(self.angle)
            self.container.board.add(bullet, x, y)
            self.cool_down = 20
        else:
            self.cool_down -= 1

    # def die(self):
    #     super().die()
    #     self.controller.settings.game_running = False
