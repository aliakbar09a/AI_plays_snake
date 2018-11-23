import random
import pygame
import colors as col


class Arena:
    def __init__(self, width, height, block):
        self.height = height
        self.width = width
        self.block = block
        self.food = (0, 0)

    def setup_background(self, screen, color):
        screen.fill(color)

    def setup(self, screen, color_bg, color):
        self.setup_background(screen, color_bg)
        # building the horizontal walls
        l = self.block
        for x in range(0, self.width, l):
            y = 0
            pygame.draw.rect(screen, color, (x, y, l, l), 1)
            pygame.draw.rect(screen, color, (x+3, y+3, l-6, l-6))
            y = self.height - l
            pygame.draw.rect(screen, color, (x, y, l, l), 1)
            pygame.draw.rect(screen, color, (x+3, y+3, l-6, l-6))
        # building the vertical walls
        for y in range(l, self.height-l, l):
            x = 0
            pygame.draw.rect(screen, color, (x, y, l, l), 1)
            pygame.draw.rect(screen, color, (x+3, y+3, l-6, l-6))
            x = self.width - l
            pygame.draw.rect(screen, color, (x, y, l, l), 1)
            pygame.draw.rect(screen, color, (x+3, y+3, l-6, l-6))
        return screen

    def newFood(self, list):
        '''
        list = snake body parts position list
        '''
        found = False
        size = self.block
        while not found:
            x = random.randint(2*size, self.width - 2*size)
            x = x - (x % size)
            y = random.randint(2*size, self.height - 2*size)
            y = y - (y % size)
            i = 0
            while i < len(list):
                if x == list[i][0] and y == list[i][1]:
                    break
                i = i + 1
            if i == len(list):
                found = True
        self.food = (x, y)
        return self.food

    def drawFood(self, screen, color):
        pygame.draw.rect(screen, color, (self.food[0], self.food[1], self.block, self.block))
        return screen
