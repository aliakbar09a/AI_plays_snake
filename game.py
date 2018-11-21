import pygame
import colors as col
import pickle
from Arena import *
from snake import *
import time

width = 740
height = 640
block_length = 10
brainLayer = [24, 16, 3]
if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption('Snake game played by AI')
	t_snake = snake(width, height, brainLayer, block_length, random_weights=False, random_bases=False)
	file = open('best_snake.pickle', 'rb')
	snake = pickle.load(file)
	file.close()
	t_snake.Brain.weights = snake.Brain.weights
	t_snake.Brain.bases = snake.Brain.bases
	arena = Arena(width, height, block_length)
	screen = arena.setup(screen,col.lavender, col.dark_gray)
	screen = t_snake.draw(screen, col.black)
	food = arena.newFood(t_snake.list)
	screen = arena.drawFood(screen, col.red)
	pygame.display.update()
	time.sleep(1)
	t_snake.Brain.setNextFood(food)
	while t_snake.isAlive():
		result, isFoodEaten = t_snake.Brain.decision_from_nn(t_snake.head_x, t_snake.head_y, t_snake.list, t_snake.direction)
		if(isFoodEaten):
		    t_snake.increaseSize()
		    t_snake.Brain.setNextFood(arena.newFood(t_snake.list))
		if t_snake.move(result) == False:
			time.sleep(1)
			print('crashed')
			break
		screen = arena.setup(screen,col.lavender, col.dark_gray)
		screen = t_snake.draw(screen, col.black)
		screen = arena.drawFood(screen, col.red)
		pygame.display.update()
		print(len(t_snake.list))
		time.sleep(0.001)
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
