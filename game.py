import pygame
import colors as col
import pickle
from Arena import *
from snake import *
import time
from input import *

if __name__ == "__main__":
	pygame.init()
	pygame.font.init()
	myfont = pygame.font.SysFont('Bitstream Vera Serif', 20)
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption('Snake game played by AI')
	# loading the saved snakes
	file = open('top_snakes.pickle', 'rb')
	snakes = pickle.load(file)
	file.close()
	arena = Arena(width, height, block_length)
	screen = arena.setup(screen,col.lavender, col.dark_gray)
	pygame.display.update()
	generation = 0
	for saved_snake in snakes:
		t_snake = snake(width, height, brainLayer, block_length, random_weights=False, random_bases=False)
		t_snake.Brain.weights = saved_snake.Brain.weights
		t_snake.Brain.bases = saved_snake.Brain.bases
		t_snake.Brain.setNextFood(arena.newFood(t_snake.list))
		screen = t_snake.draw(screen, col.black)
		screen = arena.drawFood(screen, col.red)
		checkloop = False
		while t_snake.isAlive():
			result, isFoodEaten = t_snake.Brain.decision_from_nn(t_snake.head_x, t_snake.head_y, t_snake.list, t_snake.direction)
			if t_snake.steps_taken > 250:
				if not checkloop:
					checkloop = True
					any_point = (t_snake.head_x, t_snake.head_y)
					times = 0
				if (t_snake.head_x, t_snake.head_y) == any_point:
					times += 1
				if times > 2:
					t_snake.crash_wall = True
					t_snake.crash_body = True
			else:
				checkloop = False
			if isFoodEaten:
				t_snake.steps_taken = 0
				t_snake.increaseSize()
				t_snake.Brain.setNextFood(arena.newFood(t_snake.list))
			if t_snake.move(result) == False:
				time.sleep(3)
				print('crashed')
				break
			screen = arena.setup(screen,col.lavender, col.dark_gray)
			screen = t_snake.draw(screen, col.black)
			screen = arena.drawFood(screen, col.red)
			text = 'Generation : ' + str(generation) + '       ' + 'Score : ' + str(len(t_snake.list)-1)
			screen.blit(arena.text_on_screen(myfont, text), (10, 10))
			pygame.display.update()
			time.sleep(0.01)
		generation += 1
	pygame.quit()
	quit()
