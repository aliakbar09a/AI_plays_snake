import snake
import numpy as np
from Arena import Arena
from game import width, height, block_length
populations = 1000
no_of_generations = 20

def run():
    snakes = np.array([snake.snake(width, height, block_length) for _ in range(populations)])
    arena = Arena(width, height, block_length)
    i = 0
    for python in snakes:
        print('python', i, end='\t')
        python.Brain.setNextFood(arena.newFood(python.list))
        while python.isAlive():
            result, isFoodEaten = python.Brain.decision_from_nn(python.head_x, python.head_y, python.list, python.direction)
            if(result == python.Brain.prev_result):
                python.no_of_same_result += 1
            else:
                python.Brain.prev_result = result
            if(python.no_of_same_result > 20):
                python.crash_wall = True
            if(isFoodEaten):
                python.increaseSize()
                python.Brain.setNextFood(arena.newFood(python.list))
            if python.move(result) == False:
                print('crashed', end='\t')
                break
        print('score : ', len(python.list))
        i += 1
run()
