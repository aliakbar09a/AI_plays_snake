import pygame
import colors as col
from Arena import *
from snake import *
import time

width = 440
height = 440
block_length = 20

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake game played by AI')

arena = Arena(width, height, block_length)
snake = snake(width, height, block_length)
screen = arena.setup(screen,col.lavender, col.dark_gray)
screen = snake.draw(screen, col.black)
pygame.display.update()
time.sleep(1)
snake.move_up()
screen = arena.setup(screen,col.lavender, col.dark_gray)
screen = snake.draw(screen, col.black)
pygame.display.update()
time.sleep(1)
snake.move_right()
screen = arena.setup(screen,col.lavender, col.dark_gray)
screen = snake.draw(screen, col.black)
pygame.display.update()
time.sleep(1)
snake.move_down()
screen = arena.setup(screen,col.lavender, col.dark_gray)
screen = snake.draw(screen, col.black)
pygame.display.update()
time.sleep(1)
snake.move_left()
screen = arena.setup(screen,col.lavender, col.dark_gray)
screen = snake.draw(screen, col.black)
pygame.display.update()
time.sleep(1)
pygame.quit()
quit()
