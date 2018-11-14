import pygame
import colors as col
from Arena import *
from snake import *
import time

width = 440
height = 440
block_length = 20

if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption('Snake game played by AI')
	t_snake = snake(width, height, block_length)
	arena = Arena(width, height, block_length)
	screen = arena.setup(screen,col.lavender, col.dark_gray)
	screen = t_snake.draw(screen, col.black)
	food = arena.newFood(t_snake.list)
	screen = arena.drawFood(screen, col.red)
	pygame.display.update()
	time.sleep(1)
	t_snake.Brain.setNextFood(food)
	for i in range(20):
		result, isFoodEaten = t_snake.Brain.decision_from_nn(t_snake.head_x, t_snake.head_y, t_snake.list, t_snake.direction)
		if(isFoodEaten):
		    t_snake.increaseSize()
		    t_snake.Brain.setNextFood(arena.newFood(t_snake.list))
		if t_snake.move(result) == False:
		    print('crashed')
		    break
		screen = arena.setup(screen,col.lavender, col.dark_gray)
		screen = t_snake.draw(screen, col.black)
		screen = arena.drawFood(screen, col.red)
		pygame.display.update()
		time.sleep(1)
	pygame.quit()
	quit()
# pygame.display.update()
# time.sleep(1)
# snake.move_up()
# screen = arena.setup(screen,col.lavender, col.dark_gray)
# screen = snake.draw(screen, col.black)
# pygame.display.update()
# time.sleep(1)
# snake.move_right()
# screen = arena.setup(screen,col.lavender, col.dark_gray)
# screen = snake.draw(screen, col.black)
# pygame.display.update()
# time.sleep(1)
# snake.move_down()
# screen = arena.setup(screen,col.lavender, col.dark_gray)
# screen = snake.draw(screen, col.black)
# pygame.display.update()
# time.sleep(1)
# snake.move_left()
# screen = arena.setup(screen,col.lavender, col.dark_gray)
# screen = snake.draw(screen, col.black)
# pygame.display.update()
# time.sleep(1)
