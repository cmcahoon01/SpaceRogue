from ships import ship, projectile
from math import sin, cos, atan2, pi, degrees, sqrt
import pygame


class Medic(ship.Ship):
    def __init__(self, control):
        self.max_health = 200
        super().__init__(control)
        self.image = pygame.image.load('assets/Medic.png')
        self.ships.ally_ships.append(self)

        self.rotation_speed = 2
        self.speed = 1
        self.heal_range = 100
        self.heal_amount = 50

    def move(self):
        closest_ship, distance = self.find_closest(self.ships.enemy_ships + self.ships.ally_ships)
        if sqrt(distance) < 70:
            self.turn_away_from(closest_ship)
            self.forward()
        allies = self.controller.ships.ally_ships
        most_hurt = allies[0]
        for ally in allies:
            if ally.health / ally.max_health < most_hurt.health / most_hurt.max_health:
                most_hurt = ally
        if most_hurt.health == most_hurt.max_health:
            self.idle()
        else:
            if most_hurt is not self:
                if not self.facing(most_hurt):
                    self.turn_towards(most_hurt)
                distance = self.distance_to(most_hurt)
                if sqrt(distance) > 10:
                    self.forward()
            self.heal()

    def heal(self):
        heal_amount = self.heal_amount
        if self.cool_down == 0:
            in_range = []
            for ally in self.controller.ships.ally_ships:
                if self.distance_to(ally) < self.heal_range:
                    in_range.append(ally)
            for ally in in_range:
                if ally.health > 0:
                    ally.health = min(ally.health + heal_amount, ally.max_health)
            x, y = self.container.position(self)
            ray = HealRay(x, y, self.heal_range, self.controller)
            self.container.board.add(ray, x, y + 1)
            self.cool_down = 60
        else:
            self.cool_down -= 1


class HealRay(ship.Ship):
    def __init__(self, x, y, heal_range, control):
        super().__init__(control)
        self.x = x
        self.y = y
        self.range = heal_range

        self.age = 0
        self.max_age = 20

    def act(self, x, y):
        self.age += 1
        if self.age >= self.max_age:
            self.die()

    def draw(self, window, x, y):
        color = (0, 255, 0)
        radius = self.range * self.age / self.max_age
        pygame.draw.circle(window, color, (x, y), radius, 5)
