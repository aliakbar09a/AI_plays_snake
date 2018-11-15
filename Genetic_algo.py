import snake
import random
import numpy as np
from Arena import Arena
from game import width, height, block_length

population_size = 1000
no_of_generations = 20
percent_of_old_population = 50
brain_layer = [10, 32, 32, 3]


def run(snakes, arena):
    i = 0
    for python in snakes:
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
                # print('crashed', end='\t')
                break
        if len(python.list) > 1 :
            print('python', i, end='\t')
            print('steps taken', python.steps_taken, ' score : ', len(python.list))
        i += 1

def sort_based_on_fitness(snakes, make_live=False):
    snakes.sort(key = lambda x: (len(x.list), x.steps_taken), reverse=True)
    if make_live == True:
        for python in snakes:
            python.crash_wall, python.crash_body = False, False
            python.steps_taken = 0
            while len(python.list) > 1:
                python.list.pop()
def create_new_population(snakes):
    # sorting the population wrt length of snake and steps taken
    snakes.sort(key = lambda x: (len(x.list), x.steps_taken), reverse=True)
    # choosing the top x% of the population and breeding them to create new population
    # the top x% is also included in new population
    parents = []
    old_parents = int(population_size * percent_of_old_population / 100)
    for i in range(old_parents):
        parent = snake.snake(width, height, brain_layer, block_length, random_weights=False, random_bases=False)
        parent.Brain.weights = snakes[i].Brain.weights
        parent.Brain.bases = snakes[i].Brain.bases
        parents.append(parent, )
    # generating children of top x%
    children = generate_children(parents, population_size - old_parents)
    parents.append(children)
    return parents
def generate_children(parents, no_of_children):
    all_children = []
    for count in range(no_of_children):
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        child = snake.snake(width, height, brain_layer, block_length, random_weights=False)
        for i in range(len(parent1.Brain.weights)):
            # taking alternate columns of weights from parent1 and parent2
            theta = np.zeros(parent1.Brain.weights[i].shape)
            for col in range(parent1.Brain.weights[i].shape[1]):
                if col % 2 == 0:
                    theta[:,col] = parent1.Brain.weights[i][:,col]
                else:
                    theta[:,col] = parent2.Brain.weights[i][:,col]
            child.Brain.weights.append(theta)
        all_children.append(child)
    return all_children
def main():
    snakes = [snake.snake(width, height, brain_layer, block_length) for _ in range(population_size)]
    arena = Arena(width, height, block_length)
    print(len(snakes))
    run(snakes, arena)
    new_snakes = create_new_population(snakes)
    print(len(new_snakes))
    run(new_snakes, arena)
if __name__ == "__main__":
    main()
