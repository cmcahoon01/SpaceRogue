from ships import ship, projectile
import pygame
from math import sin, cos, atan2, pi, degrees, sqrt


class Projectile(ship.Ship):
    def __init__(self, angle, allied, control):
        super().__init__(control)
        self.hitbox_radius = 3
        self.angle = angle
        self.speed = 30
        self.life_time = 50
        self.allied = allied
        self.damage = 10

    def draw(self, window, x, y):
        color = (0, 0, 255) if self.allied else (255, 0, 0)
        pygame.draw.circle(window, color, (x, y), self.hitbox_radius)

    def move(self):
        self.life_time -= 1
        if self.life_time > 0:
            closest, distance_sqr = self.find_closest(list(self.container.contained_near().keys()))
            if closest is None or sqrt(distance_sqr) > self.hitbox_radius + closest.hitbox_radius:
                self.forward()
            else:
                if self.allied and (closest in self.ships.ally_ships or closest in self.ships.ally_projectiles):
                    self.forward()
                    return
                if not self.allied and (closest in self.ships.enemy_ships or closest in self.ships.enemy_projectiles):
                    self.forward()
                    return
                self.die()
                closest.hit(self)
        else:
            self.die()

