import snake
import random
import numpy as np
import pickle
from Arena import Arena
from game import width, height, block_length

population_size = 10000
no_of_generations = 20
# percent of best performing parents
per_of_best_old_pop = 20.0
# percent of worst performing parents
per_of_worst_old_pop = 1.0
mutation_percent = 1.0
mutation_intensity = 0.001
brain_layer = [24, 16, 3]


def run(snakes, arena):
    i = 0
    count = [0 for _ in range(100)]
    snakes_killed = 0
    for python in snakes:
        # print('python', i, python.steps_taken)
        food = arena.newFood(python.list)
        python.Brain.setNextFood(food)
        # print(food, end=" ")
        while python.isAlive():
            result, isFoodEaten= python.Brain.decision_from_nn(python.head_x, python.head_y, python.list, python.direction)
            if python.steps_taken > 200:
                python.crash_wall = True
                python.crash_body = True
                snakes_killed += 1
            if(isFoodEaten):
                python.increaseSize()
                python.steps_taken = 0
                python.Brain.prev_food_cost = 1
                food = arena.newFood(python.list)
                python.Brain.setNextFood(food)
                # print(food, end=" ")
            if python.move(result) == False:
                break
        count[len(python.list) - 1] += 1
        i += 1
    print('total snakes : ', count, 'snakes killed', snakes_killed)
    out.write('total snakes : ' + str(count) + ' snakes killed : ' + str(snakes_killed)+ '\n')
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
    snakes.sort(key = lambda x: (len(x.list), -x.steps_taken), reverse=True)
    file = open('best_snake3.pickle', 'wb')
    pickle.dump(snakes[0], file)
    file.close()
    for i in range(10):
        print('python', i, 'score : ', len(snakes[i].list), 'step : ', snakes[i].steps_taken, 'list', snakes[i].list, snakes[i].Brain.nextFood)
        out.write('python'+ str(i)+ 'score : '+ str(len(snakes[i].list))+'step : '+str(snakes[i].steps_taken)+'list'+str(snakes[i].list)+str(snakes[i].Brain.nextFood)+'\n')
    # choosing the top x% of the population and breeding them to create new population
    # the top x% and bottom y% is also included in new population
    parents = []
    # top_old_parents = int(population_size * per_of_best_old_pop / 100)
    bottom_old_parents = int(population_size * per_of_worst_old_pop / 100)
    top_old_parents = 0
    while len(snakes[top_old_parents].list) > 1:
        top_old_parents += 1
        parent = snake.snake(width, height, brain_layer, block_length, random_weights=False, random_bases=False)
        parent.Brain.weights = snakes[i].Brain.weights
        parent.Brain.bases = snakes[i].Brain.bases
        parents.append(parent)
    for i in range(population_size - 1, population_size - bottom_old_parents - 1, -1):
        parent = snake.snake(width, height, brain_layer, block_length, random_weights=False, random_bases=False)
        parent.Brain.weights = snakes[i].Brain.weights
        parent.Brain.bases = snakes[i].Brain.bases
        parents.append(parent, )
    # generating children of top x%
    children = generate_children(parents, population_size - top_old_parents - bottom_old_parents)
    # mutating children
    children = mutate_children(children)
    # joining parents and children to make new population
    parents.extend(children)
    return parents
def mutate_children(children):
    for child in children:
        for weight in child.Brain.weights:
            for ele in range(int(weight.shape[0]*weight.shape[1]*mutation_percent/100)):
                row = random.randint(0, weight.shape[0]-1)
                col = random.randint(0, weight.shape[1]-1)
                weight[row, col] -= random.uniform(-mutation_intensity, mutation_intensity)
    return children
def generate_children(parents, no_of_children):
    all_children = []
    l = len(parents)
    for count in range(no_of_children):
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        # parent1 = parents[count%l]
        # parent2 = parents[(count+1)%l]
        child = snake.snake(width, height, brain_layer, block_length, random_weights=False, random_bases=True)
        # for i in range(len(parent1.Brain.weights)):
        #     # taking alternate columns of weights from parent1 and parent2
        #     theta = np.zeros(parent1.Brain.weights[i].shape)
        #     for col in range(parent1.Brain.weights[i].shape[1]):
        #         if col % 2 == 0:
        #             theta[:,col] = parent1.Brain.weights[i][:,col]
        #         else:
        #             theta[:,col] = parent2.Brain.weights[i][:,col]
        #     child.Brain.weights.append(theta)
        for i in range(len(parent1.Brain.weights)):
            # taking average of weights from parent1 and parent2
            theta = (parent1.Brain.weights[i] + parent2.Brain.weights[i]) / 2
            child.Brain.weights.append(theta)
        all_children.append(child)
    return all_children
def main():
    snakes = [snake.snake(width, height, brain_layer, block_length) for _ in range(population_size)]
    arena = Arena(width, height, block_length)
    for i in range(no_of_generations):
        print('generation : ', i, ',', end='\t\t')
        out.write('generation : ' + str(i) +'\t')
        run(snakes, arena)
        snakes = create_new_population(snakes)

if __name__ == "__main__":
    out = open('output.txt', 'wt')
    main()
    out.close()


            # if(closer_to_food == False):
            #     python.steps_taken += 1000
            #     snakes_killed += 1
            #     python.crash_wall = True
            #     python.crash_body =True
            # if(result == python.Brain.prev_result):
            #     python.no_of_same_result += 1
            # else:
            #     python.Brain.prev_result = result
            # if(python.no_of_same_result > 50):
            #     python.steps_taken = 0
            #     python.crash_wall = True
            #     python.crash_body =True
        # if len(python.list) > 1 :
        #     if python.crash_body and python.crash_body:
        #         print('crashed repetition', end='\t')
        #     elif python.crash_wall and not python.crash_body:
        #         print('crashed wall', end='\t')
        #     else:
        #         print('crashed body', end='\t')
        #     print('steps taken', python.steps_taken, '\t\tscore : ', len(python.list) - 1)
