import random
from pygame import draw
from brain import *


class snake:
    def __init__(self, width, height, brainLayer, size, random_weights=True, random_bases=True, random_start=False):
        self.list = []
        self.width = width
        self.height = height
        self.steps_taken = 0
        self.no_of_same_result = 0
        self.crash_wall = False
        self.crash_body = False
        self.block = size
        self.Brain = brain(brainLayer, self.width, self.height,
                           self.block, random_weights, random_bases)
        if random_start:
            self.direction = random.choice(['east', 'north', 'west', 'east'])
            x = random.randint(3*size, width - 2*size)
            self.head_x = x - (x % size)
            y = random.randint(size, height - 2*size)
            self.head_y = y - (y % size)
        else:
            self.direction = 'east'
            self.head_x, self.head_y = 40, 40
        self.list.append((self.head_x, self.head_y))

    # draw the snake on the pygame screen
    def draw(self, screen, color):
        l = self.block
        for (x, y) in self.list:
            draw.rect(screen, color, (x, y, l, l), 1)
            draw.rect(screen, color, (x+3, y+3, l-6, l-6))
        return screen

    # returns true if snake is alive else false
    def isAlive(self):
        if not self.crash_wall and not self.crash_body:
            return True
        else:
            return False

    # sets the crash_wall and crash_body if unable to go north accordingly
    def check_north(self):
        if self.head_y - self.block < self.block:
            self.crash_wall = True
        for i in range(len(self.list) - 1):
            if self.list[i][0] == self.head_x and self.list[i][1] == (self.head_y - self.block):
                self.crash_body = True

    # move the snake in north
    def move_north(self):
        self.check_north()
        if not (self.crash_wall or self.crash_body):
            self.direction = 'north'
            self.head_y = self.head_y - self.block
            self.list.insert(0, (self.head_x, self.head_y))
            self.list.pop()

    # sets the crash_wall and crash_body if unable to go south accordingly
    def check_south(self):
        if self.head_y + self.block >= self.height - self.block:
            self.crash_wall = True
        for i in range(len(self.list) - 1):
            if self.list[i][0] == self.head_x and self.list[i][1] == (self.head_y + self.block):
                self.crash_body = True

    # move the snake in south
    def move_south(self):
        self.check_south()
        if not (self.crash_wall or self.crash_body):
            self.direction = 'south'
            self.head_y = self.head_y + self.block
            self.list.insert(0, (self.head_x, self.head_y))
            self.list.pop()

    # sets the crash_wall and crash_body if unable to go east accordingly
    def check_east(self):
        if self.head_x + self.block >= self.width - self.block:
            self.crash_wall = True
        for i in range(len(self.list) - 1):
            if self.list[i][0] == (self.head_x + self.block) and self.list[i][1] == self.head_y:
                self.crash_body = True

    # move the snake in east
    def move_east(self):
        self.check_east()
        if not (self.crash_wall or self.crash_body):
            self.direction = 'east'
            self.head_x = self.head_x + self.block
            self.list.insert(0, (self.head_x, self.head_y))
            self.list.pop()

    # sets the crash_wall and crash_body if unable to go west accordingly
    def check_west(self):
        if self.head_x - self.block < self.block:
            self.crash_wall = True
        for i in range(len(self.list) - 1):
            if self.list[i][0] == (self.head_x - self.block) and self.list[i][1] == self.head_y:
                self.crash_body = True

    # move the snake in west
    def move_west(self):
        self.check_west()
        if not (self.crash_wall or self.crash_body):
            self.direction = 'west'
            self.head_x = self.head_x - self.block
            self.list.insert(0, (self.head_x, self.head_y))
            self.list.pop()

    # returns the next head position and direction based on the result passed
    def next_position_direction(self, result):
        l = self.block
        x = self.head_x
        y = self.head_y
        direction = self.direction
        if direction == 'north':
            if result == 1:
                return (x, y - l), 'north'
            elif result == 2:
                return (x - l, y), 'west'
            else:
                return (x + l, y), 'east'
        elif direction == 'east':
            if result == 1:
                return (x + l, y), 'east'
            elif result == 2:
                return (x, y - l), 'north'
            else:
                return (x, y + l), 'south'
        elif direction == 'south':
            if result == 1:
                return (x, y + l), 'south'
            elif result == 2:
                return (x + l, y), 'east'
            else:
                return (x - l, y), 'west'
        else:
            if result == 1:
                return (x - l, y), 'west'
            elif result == 2:
                return (x, y + l), 'south'
            else:
                return (x, y - l), 'north'

    # returns true if x and y doesn't lie on the body of snake
    def onBody(self, x, y):
        for i in range(3, len(self.list) - 1):
            if self.list[i][0] == x and self.list[i][1] == y:
                return True
        return False

    # increase the size of the snake in the direction given by nn
    def increaseSize(self, result):
        pos, dir = self.next_position_direction(result)
        if (pos[0] != 0) and (pos[0] != self.width-self.block) and (pos[1] != 0) and (pos[1] != self.height-self.block) and (not self.onBody(pos[0], pos[1])):
            self.head_x, self.head_y = pos[0], pos[1]
            self.list.insert(0, (self.head_x, self.head_y))
            self.direction = dir
            return True
        else:
            return False

    # move the snake based on the result provided
    def move(self, result):
        if self.direction == 'north':
            if result == 1:
                self.move_north()
            elif result == 2:
                self.move_west()
            else:
                self.move_east()
        elif self.direction == 'east':
            if result == 1:
                self.move_east()
            elif result == 2:
                self.move_north()
            else:
                self.move_south()
        elif self.direction == 'south':
            if result == 1:
                self.move_south()
            elif result == 2:
                self.move_east()
            else:
                self.move_west()
        else:
            if result == 1:
                self.move_west()
            elif result == 2:
                self.move_south()
            else:
                self.move_north()
        self.steps_taken += 1
        return self.isAlive()
