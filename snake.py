import random
import pygame
import brain

class snake:
    def __init__(self, width, height, size):
        self.list = []
        self.width = width
        self.height = height
        self.crash_wall = False
        self.crash_body = False
        self.blocksize = size
        x = random.randint(2*size, width - size)
        self.head_x = x - (x%size)
        y = random.randint(size, height - size)
        self.head_y = y - (y%size)
        self.list.append((self.head_x, self.head_y))
        self.list.append((self.head_x - size, self.head_y))
    def draw(self, screen, color):
        length = self.blocksize
        for (x, y) in self.list:
            pygame.draw.rect(screen, color, (x, y, length, length),1)
            pygame.draw.rect(screen, color, (x+4, y+4, length-8, length-8))
        return screen

    def check_up(self):
        if self.head_y - self.blocksize < self.blocksize:
            self.crash_wall = True
        for (x, y) in self.list:
            if y == self.head_y - self.blocksize:
                self.crash_body = True
    def move_up(self):
        self.check_up()
        if not (self.crash_wall or self.crash_body):
            self.head_y = self.head_y - self.blocksize
            self.list.insert(0, (self.head_x, self.head_y))
            self.list.pop()

    def check_down(self):
        if self.head_y + self.blocksize >= self.height - self.blocksize:
            self.crash_wall = True
        for (x, y) in self.list:
            if y == self.head_y + self.blocksize:
                self.crash_body = True
    def move_down(self):
        self.check_down()
        if not (self.crash_wall or self.crash_body):
            self.head_y = self.head_y + self.blocksize
            self.list.insert(0, (self.head_x, self.head_y))
            self.list.pop()

    def check_right(self):
        if self.head_x + self.blocksize >= self.width - self.blocksize:
            self.crash_wall = True
        for (x, y) in self.list:
            if x == self.head_x + self.blocksize:
                self.crash_body = True
    def move_right(self):
        self.check_right()
        if not (self.crash_wall or self.crash_body):
            self.head_x = self.head_x + self.blocksize
            self.list.insert(0, (self.head_x, self.head_y))
            self.list.pop()

    def check_left(self):
        if self.head_x - self.blocksize < self.blocksize:
            self.crash_wall = True
        for (x, y) in self.list:
            if x == self.head_x - self.blocksize:
                self.crash_body = True
    def move_left(self):
        self.check_left()
        if not (self.crash_wall or self.crash_body):
            self.head_x = self.head_x - self.blocksize
            self.list.insert(0, (self.head_x, self.head_y))
            self.list.pop()
