import random
import pygame
import colors as col


class Arena:
    def __init__(self, width, height, blocksize):
        self.height = height
        self.width = width
        self.blocksize = blocksize
        self.food = (0, 0)

    def setup_background(self, screen, color):
        screen.fill(color)
    def setup(self, screen, color_bg, color):
        self.setup_background(screen, color_bg)
        # building the horizontal walls
        length = self.blocksize
        for x in range(0, self.width, length):
            y = 0
            # print('vertical (x, y)', x, y)
            pygame.draw.rect(screen, color, (x, y, length, length),1)
            pygame.draw.rect(screen, color, (x+4, y+4, length-8, length-8))
            y = self.height - length
            pygame.draw.rect(screen, color, (x, y, length, length),1)
            pygame.draw.rect(screen, color, (x+4, y+4, length-8, length-8))
        # building the vertical walls
        for y in range(length, self.height-length, length):
            x = 0
            pygame.draw.rect(screen, color, (x, y, length, length),1)
            pygame.draw.rect(screen, color, (x+4, y+4, length-8, length-8))
            x = self.width - length
            pygame.draw.rect(screen, color, (x, y, length, length),1)
            pygame.draw.rect(screen, color, (x+4, y+4, length-8, length-8))
        return screen
    def newFood(self, color, list):
        '''
        list = snake body parts position list
        '''
        found = False
        size = self.blocksize
        while not found:
            x = random.randint(size, width - size)
            x = x - (x%size)
            y = random.randint(size, height - size)
            y = y - (y%size)
            i = 0
            while i < len(list):
                if x == list[i][0] and y == list[i][1]:
                    break
                i = i + 1
            if i == len(list):
                found = True
        self.food = (x, y)
