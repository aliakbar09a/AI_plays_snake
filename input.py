# game environment parameters
width = 540
height = 440
block_length = 20
brainLayer = [24, 16, 3]  # neural network layers that act as brain of snake

# genetic algorithm parameter
population_size = 50
no_of_generations = 30
per_of_best_old_pop = 20.0  # percent of best performing parents to be included
per_of_worst_old_pop = 2.0  # percent of worst performing parents to be included
mutation_percent = 7.0
mutation_intensity = 0.1
