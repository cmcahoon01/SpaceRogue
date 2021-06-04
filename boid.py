from math import sin, cos, atan2, pi, degrees
import pygame
import random


class Boid:
    def __init__(self, angle=0, name=str(random.random()), container=None):
        self.angle = angle
        self.container = container
        self.name = name

    def __repr__(self):
        return self.name

    def set_container(self, container):
        self.container = container

    def draw(self, window, x, y):
        color = (100, 100, 100)
        points = [(x, y)]
        size = 20
        angle1 = self.angle + .9 * pi
        angle2 = self.angle + pi
        angle3 = self.angle + 1.1 * pi
        points.append((x + size * cos(angle1), y + size * sin(angle1)))
        points.append((x + size * 0.7 * cos(angle2), y + size * 0.7 * sin(angle2)))
        points.append((x + size * cos(angle3), y + size * sin(angle3)))
        pygame.draw.polygon(window, color, points, 0)

    def act(self, x, y):
        # return
        self.correct_angle()
        target, t_pos, t_distance_sqr = self.closest_neighbor()

        speed = 5
        rotation_speed = 0.05

        if target:
            left_diff = 0
            dy, dx = t_pos[1] - y, t_pos[0] - x
            angle_to_t = atan2(dy, dx)
            angle_to_t = self.correct_angle(angle_to_t)
            if t_distance_sqr > 40 ** 2:
                left_diff = self.angle - angle_to_t
                if left_diff < 0:
                    left_diff = 2 * pi + left_diff
            elif t_distance_sqr < 20 ** 2:
                left_diff = angle_to_t - self.angle
                if left_diff < 0:
                    left_diff = 2 * pi + left_diff
            else:
                left_diff = self.angle - target.angle
                if abs(left_diff) < pi / 30:
                    left_diff = pi
                left_diff = self.correct_angle(left_diff)

            if left_diff < pi:
                self.angle -= rotation_speed * left_diff  # left turn
            else:
                self.angle += rotation_speed * (2 * pi - left_diff)  # right turn
        # else:
        #     self.angle_to_t += (random.random() - 0.5) / 5
        self.correct_angle()

        dx, dy = speed * cos(self.angle), speed * sin(self.angle)
        self.container.move(self, dx, dy)

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

    def closest_neighbor(self):
        neighbors = self.container.contained_near()

        neighbors.pop(self)
        x, y = self.container.position(self)
        closest = None
        closest_distance = 999999999
        closest_position = None
        for boid, _ in neighbors.items():
            position = boid.container.position(boid)
            distance = (x - position[0]) ** 2 + (y - position[1]) ** 2

            if distance < closest_distance:
                closest = boid
                closest_distance = distance
                closest_position = position
        return closest, closest_position, closest_distance
