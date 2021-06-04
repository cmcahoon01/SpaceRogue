import pygame
import random
import math
import time


class Partition:
    def __init__(self, x, y, size, board):
        self.x = x
        self.y = y
        self.above = self.below = self.left = self.right = None
        self.size = size
        self.contained = {}
        self.contained_next = {}
        self.board = board

    def __contains__(self, item):
        return item in self.contained

    def __repr__(self):
        return 'Part (' + str(self.x) + ',' + str(self.y) + ')'

    def draw(self, window, cam_x, cam_y):
        for agent, pos in self.contained.items():
            agent.draw(window, pos[0] + self.x - cam_x, pos[1] + self.y - cam_y)

    def contained_near(self):
        new_set = self.contained.copy()
        new_set = new_set | self.above.contained | self.below.contained | self.left.contained | self.right.contained
        new_set = new_set | self.right.above.contained | self.right.below.contained
        new_set = new_set | self.left.above.contained | self.left.below.contained
        return new_set

    def add(self, addition, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.contained_next[addition] = (x, y)
        else:
            self.add_to_new_container(addition, x, y)

    def remove(self, deleted):
        if deleted in self.contained_next:
            self.contained_next.pop(deleted)

    def move(self, moving, dx, dy):
        old_pos = self.contained[moving]
        x, y = old_pos[0] + dx, old_pos[1] + dy
        if 0 <= x < self.size and 0 <= y < self.size:
            self.contained_next[moving] = (x, y)
        else:
            self.contained_next.pop(moving)
            self.add_to_new_container(moving, x, y)

    def add_to_new_container(self, addition, x, y):
        if x < 0 and y < 0:
            self.above.left.add(addition, x + self.size, y + self.size)
        elif x >= self.size and y < 0:
            self.above.right.add(addition, x - self.size, y + self.size)
        elif x < 0 and y >= self.size:
            self.below.left.add(addition, x + self.size, y - self.size)
        elif x >= self.size and y >= self.size:
            self.below.right.add(addition, x - self.size, y - self.size)
        elif x < 0:
            self.left.add(addition, x + self.size, y)
        elif x >= self.size:
            self.right.add(addition, x - self.size, y)
        elif y < 0:
            self.above.add(addition, x, y + self.size)
        elif y >= self.size:
            self.below.add(addition, x, y - self.size)

    def position(self, agent):
        return self.contained[agent][0] + self.x, self.contained[agent][1] + self.y

    def act_all(self):
        for agent, pos in self.contained.items():
            agent.act(pos[0] + self.x, pos[1] + self.y)

    def update_contained(self):
        self.contained = self.contained_next.copy()
        for agent, pos in self.contained.items():
            agent.set_container(self)


class Board:
    def __init__(self, width, height):
        self.partition_size = 50
        self.width = width
        self.height = height
        self.partitions = [[Partition(x, y, self.partition_size, self)
                            for y in range(0, height, self.partition_size)]
                           for x in range(0, width, self.partition_size)]
        self.set_neighbors()

    def set_neighbors(self):
        for x, arr in enumerate(self.partitions):
            for y, partition in enumerate(arr):
                if x > 0:
                    partition.left = self.partitions[x - 1][y]
                else:
                    partition.left = self.partitions[-1][y]
                if y > 0:
                    partition.above = self.partitions[x][y - 1]
                else:
                    partition.above = self.partitions[x][-1]
                if x < len(self.partitions) - 1:
                    partition.right = self.partitions[x + 1][y]
                else:
                    partition.right = self.partitions[0][y]
                if y < len(arr) - 1:
                    partition.below = self.partitions[x][y + 1]
                else:
                    partition.below = self.partitions[x][0]

    def draw(self, window):
        board_color = (0, 0, 0)
        window.fill(board_color)
        self.draw_stars(window)

    def add(self, addition, x, y):
        if len(self.partitions) <= x / self.partition_size:
            print(len(self.partitions), x / self.partition_size)
        container = self.partitions[math.floor(x / self.partition_size)][math.floor(y / self.partition_size)]
        container.add(addition, x % self.partition_size, y % self.partition_size)
        container.update_contained()

    def act(self):
        for arr in self.partitions:
            for partition in arr:
                partition.update_contained()
        for arr in self.partitions:
            for partition in arr:
                partition.act_all()

    def draw_stars(self, window):
        random.seed(1)
        for n in range(200):  # num stars
            x = random.randint(0, 100 * 16)
            y = random.randint(0, 100 * 9)
            pygame.draw.circle(window, (237, 237, 232), (x, y), 1)
        random.seed(time.time_ns())
