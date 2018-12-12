import snake
import random
import numpy as np
import pickle
from Arena import Arena
import argparse
from input import *
import time


# used to show the progress bar
def progress_bar(curr, total, length):
    frac = curr/total
    filled_bar = round(frac*length)
    print('\r', '#'*filled_bar + '-'*(length - filled_bar), '[{:>7.2%}]'.format(frac), end='')


# to run all the snakes of a population
def run(snakes, arena):
    i = 1
    count = [0 for _ in range(300)]
    snakes_killed = 0
    # making new seed for each generation so that fittest of one generation may not be fittest in another
    # and we get a global optimum
    env_seed = random.random()
    for s in snakes:
        start_time = time.time()
        checkloop = False
        progress_bar(i, population_size, 30)
        random.seed(env_seed)  # so that each snake of the population faces the same environment
        s.Brain.setNextFood(arena.newFood(s.list))
        while s.isAlive():
            result = s.Brain.decision_from_nn(s.head_x, s.head_y, s.list, s.direction)
            # to check if continuous loop formed by snake and then killing that snake
            if s.steps_taken > 250:
                if not checkloop:
                    checkloop = True
                    any_point_of_loop = (s.head_x, s.head_y)
                    times = 0
                elif (s.head_x, s.head_y) == any_point_of_loop:
                    times += 1
                if times > 2:
                    s.crash_wall = True
                    s.crash_body = True
                    snakes_killed += 1
            else:
                checkloop = False
            # forcefully killing if loop not caught
            if time.time() - start_time > 0.5:
                s.crash_wall = True
                s.crash_body = True
                snakes_killed += 1
            # if food eaten by snake
            if (s.head_x, s.head_y) == arena.food:
                s.steps_taken = 0
                result = s.Brain.decision_from_nn(s.head_x, s.head_y, s.list, s.direction)
                if not s.increaseSize(result):
                    s.crash_wall = True
                start_time = time.time()
                s.Brain.setNextFood(arena.newFood(s.list))
            if s.move(result) == False:
                break
        random.seed()
        count[len(s.list) - 1] += 1
        i += 1
    print('\nsnakes distribution with index as score : ',
          count[0:15], 'snakes killed', snakes_killed)


# to print the top five snakes info
def print_top_5(five_snakes):
    i = 0
    for snake in five_snakes:
        i += 1
        print('snake : ', i, ', score : ', len(snake.list) -
              1, ', steps : ', snake.steps_taken, end='\t')
        if snake.crash_body and snake.crash_wall:
            print('crashed repetition')
        elif snake.crash_wall and not snake.crash_body:
            print('crashed wall')
        else:
            print('crashed body')


# to save the snake
def save_top_snakes(snakes,  filename):
    f = open(filename, 'wb')
    pickle.dump(snakes, f)
    f.close()


# used to create the popultion for next generation
def create_new_population(snakes):
    # choosing the top x% of the population and breeding them to create new population
    # the top x% and bottom y% is also included in new population
    parents = []
    top_old_parents = int(population_size * per_of_best_old_pop / 100)
    bottom_old_parents = int(population_size * per_of_worst_old_pop / 100)
    for i in range(top_old_parents):
        parent = snake.snake(width, height, brainLayer, block_length,
                             random_weights=False, random_bases=False)
        parent.Brain.weights = snakes[i].Brain.weights
        parent.Brain.bases = snakes[i].Brain.bases
        parents.append(parent)
    for i in range(population_size - 1, population_size - bottom_old_parents - 1, -1):
        parent = snake.snake(width, height, brainLayer, block_length,
                             random_weights=False, random_bases=False)
        parent.Brain.weights = snakes[i].Brain.weights
        parent.Brain.bases = snakes[i].Brain.bases
        parents.append(parent)
    # generating children of top x% and bottom y%
    children = generate_children(parents, population_size - (top_old_parents + bottom_old_parents))
    # mutating children
    children = mutate_children(children)
    # joining parents and children to make new population
    parents.extend(children)
    return parents


# mutating the children
def mutate_children(children):
    for child in children:
        for weight in child.Brain.weights:
            for ele in range(int(weight.shape[0]*weight.shape[1]*mutation_percent/100)):
                row = random.randint(0, weight.shape[0]-1)
                col = random.randint(0, weight.shape[1]-1)
                weight[row, col] += random.uniform(-mutation_intensity, mutation_intensity)
    return children


# generating children based on the parents passed
def generate_children(parents, no_of_children):
    all_children = []
    l = len(parents)
    for count in range(no_of_children):
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        child = snake.snake(width, height, brainLayer, block_length)
        for i in range(len(parent1.Brain.weights)):
            for j in range(parent1.Brain.weights[i].shape[0]):
                for k in range(parent1.Brain.weights[i].shape[1]):
                    child.Brain.weights[i][j, k] = random.choice(
                        [parent1.Brain.weights[i][j, k], parent2.Brain.weights[i][j, k]])
            for j in range(parent1.Brain.bases[i].shape[1]):
                child.Brain.bases[i][0, j] = random.choice(
                    [parent1.Brain.bases[i][0, j], parent2.Brain.bases[i][0, j]])
        all_children.append(child)
    return all_children


def main():
    # command line argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument('-o', '--output', required=True, help='relative path to save the snakes')
    args = vars(ap.parse_args())
    snakes = [snake.snake(width, height, brainLayer, block_length) for _ in range(population_size)]
    arena = Arena(width, height, block_length)
    top_snakes = []
    for i in range(no_of_generations):
        print('generation : ', i+1, ',', end='\n')
        run(snakes, arena)
        # sorting the population wrt length of snake and steps taken
        snakes.sort(key=lambda x: (len(x.list), -x.steps_taken), reverse=True)
        print_top_5(snakes[0:5])
        # generalising the whole population
        print('saving the snake')
        top_snakes.append(snakes[0])
        # saving top snakes list as pickle
        save_top_snakes(top_snakes, args['output'])
        snakes = create_new_population(snakes)


if __name__ == "__main__":
    main()
