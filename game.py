import pygame
import colors as col
import pickle
from Arena import *
from snake import *
import time
import argparse
from input import *

if __name__ == "__main__":
    # command line argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input', required=True, help='relative path of the saved pickle file')
    ap.add_argument('-s', '--start', type=int, help='relative start of the saved snakes')
    args = vars(ap.parse_args())
    # loading the saved snakes
    file = open(args['input'], 'rb')
    snakes = pickle.load(file)
    generation = 0
    if args['start'] is not None:
        start = args['start']
        snakes = snakes[start:]
        generation += start
    file.close()
    # pygame initialization
    pygame.init()
    pygame.font.init()
    myfont = pygame.font.SysFont('Bitstream Vera Serif', 20)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Generation : 0\t\tScore : 0')
    # seed generated so that each snake sees same set of foods for performance comparison
    seed = random.random()
    arena = Arena(width, height, block_length)

    for saved_snake in snakes:
        t_snake = snake(width, height, brainLayer, block_length,
                        random_weights=False, random_bases=False)
        t_snake.Brain.weights = saved_snake.Brain.weights
        t_snake.Brain.bases = saved_snake.Brain.bases
        random.seed(seed)
        t_snake.Brain.setNextFood(arena.newFood(t_snake.list))
        screen = arena.setup(screen, col.bg, col.gray)
        screen = arena.drawFood(screen, col.pink)
        screen = t_snake.draw(screen, col.blue)
        pygame.display.update()
        checkloop = False
        while t_snake.isAlive():
            # checking for key presses and close button presses and pause-continue funcionality
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    pressed = True
                    while pressed:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                                pressed = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    t_snake.crash_wall = True
                    t_snake.crash_body = True
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            # getting result from the neural network
            result = t_snake.Brain.decision_from_nn(
                t_snake.head_x, t_snake.head_y, t_snake.list, t_snake.direction)
            # moving the snake
            alive = t_snake.move(result)
            # checking for loops made by snake
            if t_snake.steps_taken > (len(t_snake.list)/5*100):
                if not checkloop:
                    checkloop = True
                    any_point = (t_snake.head_x, t_snake.head_y)
                    times = 0
                if (t_snake.head_x, t_snake.head_y) == any_point:
                    times += 1
                if times > 4:
                    t_snake.crash_wall = True
                    t_snake.crash_body = True
                    alive = False
            else:
                checkloop = False
            if not alive:
                text = 'Generation : ' + str(generation+1) + '\t\t' + \
                    'Score : ' + str(len(t_snake.list)-1)+'\t[Dead]'
                if t_snake.crash_wall and t_snake.crash_body:
                    print('killed,', 'generation : ', generation+1, 'score : ', len(t_snake.list)-1)
                elif t_snake.crash_wall and not t_snake.crash_body:
                    print('crashed on wall,', 'generation : ',
                          generation+1, 'score : ', len(t_snake.list)-1)
                else:
                    print('crashed on body,', 'generation : ',
                          generation+1, 'score : ', len(t_snake.list)-1)
                pygame.display.set_caption(text)
                time.sleep(2)
                break
            if (t_snake.head_x, t_snake.head_y) == arena.food:
                t_snake.steps_taken = 0
                next_position = t_snake.Brain.decision_from_nn(
                    t_snake.head_x, t_snake.head_y, t_snake.list, t_snake.direction)
                if not t_snake.increaseSize(next_position):
                    t_snake.crash_wall = True
                t_snake.Brain.setNextFood(arena.newFood(t_snake.list))
            screen = arena.setup(screen, col.bg, col.gray)
            screen = arena.drawFood(screen, col.pink)
            screen = t_snake.draw(screen, col.blue)
            pygame.display.update()
            text = 'Generation : ' + str(generation+1) + '\t\t' + \
                'Score : ' + str(len(t_snake.list)-1)+'\t[Press q to kill]'
            pygame.display.set_caption(text)
            pygame.display.update()
            time.sleep(0.03)
        generation += 1
    pygame.quit()
    quit()
