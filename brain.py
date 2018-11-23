import random
import numpy as np


class brain:
    def __init__(self, layers, width, height, block, random_weights=True, random_bases=True):
        self.nextFood = None
        self.outputs = []
        self.weights = []
        self.prev_result = 1
        self.bases = []
        self.prev_food_cost = 1.0
        self.block = block
        self.width = width
        self.height = height
        if random_weights == True:
            for i in range(len(layers) - 1):
                theta = np.random.uniform(low=-0.5, high=.5, size=(layers[i], layers[i+1]))
                self.weights.append(theta)
        if random_bases == True:
            for i in range(len(layers) - 1):
                base = np.random.uniform(low=-0.1, high=0.1, size=(1, layers[i+1]))
                self.bases.append(base)

    # returns true if x, y is the part of the snake else false
    def isBody(self, x, y, snake):
        for i in range(3, len(snake) - 1):
            if snake[i][0] == x and snake[i][1] == y:
                return True
        return False

    # next position and direction based on the result passed
    def next_position_direction(self, x, y, direction, result):
        l = self.block
        if direction == 'north':
            if result == 1:
                return (x, y - l), 'north'
            elif result == 2:
                return (x - l, y), 'west'
            else:
                return (x + l, y), 'east'
        elif direction == 'east':
            if result == 1:
                return (x + l, y), 'east'
            elif result == 2:
                return (x, y - l), 'north'
            else:
                return (x, y + l), 'south'
        elif direction == 'south':
            if result == 1:
                return (x, y + l), 'south'
            elif result == 2:
                return (x + l, y), 'east'
            else:
                return (x - l, y), 'west'
        else:
            if result == 1:
                return (x - l, y), 'west'
            elif result == 2:
                return (x, y + l), 'south'
            else:
                return (x, y - l), 'north'

    # returns an list with three element indicating the food, body part and boundary based on the direction passed
    def look_in_direction(self, x, y, dirx, diry, fx, fy, snake):
        distance = 1
        input = [0, 0, 0]
        food_found = False
        body_found = False
        while((x != 0) and (x != self.width-self.block) and (y != 0) and (y != self.height-self.block)):
            x, y = x + dirx, y + diry
            distance += 1
            if(not food_found and fx == x and fy == y):
                input[0] = 1
                food_found = True
            if(not body_found and self.isBody(x, y, snake)):
                input[1] = 1 / distance
                body_found = True
        input[2] = 1 / distance
        return input

    # makes the input for the neural network by passing all 8 directions to look_in_direction
    def make_input(self, x, y, fx, fy, snake, direction):
        input = []
        # look in direction where snake is moving
        (new_x, new_y), _ = self.next_position_direction(x, y, direction, 1)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.look_in_direction(x, y, dir_x, dir_y, fx, fy, snake))
        # look in 90 degree left of direction where snake is moving
        (new_x, new_y), _ = self.next_position_direction(x, y, direction, 2)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.look_in_direction(x, y, dir_x, dir_y, fx, fy, snake))
        # look in 90 degree right of direction where snake is moving
        (new_x, new_y), _ = self.next_position_direction(x, y, direction, 3)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.look_in_direction(x, y, dir_x, dir_y, fx, fy, snake))
        # look in 45 degree left of direction where snake is moving
        (tempx, tempy), new_dir = self.next_position_direction(x, y, direction, 1)
        (new_x, new_y), _ = self.next_position_direction(tempx, tempy, new_dir, 2)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.look_in_direction(x, y, dir_x, dir_y, fx, fy, snake))
        # look in 45 degree right of direction where snake is moving
        (tempx, tempy), new_dir = self.next_position_direction(x, y, direction, 1)
        (new_x, new_y), _ = self.next_position_direction(tempx, tempy, new_dir, 3)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.look_in_direction(x, y, dir_x, dir_y, fx, fy, snake))
        # look in opposite to the direction where snake is moving
        (tempx, tempy), new_dir = self.next_position_direction(x, y, direction, 2)
        (new_x, new_y), new_dir = self.next_position_direction(tempx, tempy, new_dir, 2)
        (new_x, new_y), _ = self.next_position_direction(new_x, new_y, new_dir, 2)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.look_in_direction(x, y, dir_x, dir_y, fx, fy, snake))
        # look in 135 degree right of direction where snake is moving
        (tempx, tempy), new_dir = self.next_position_direction(x, y, direction, 3)
        (new_x, new_y), _ = self.next_position_direction(tempx, tempy, new_dir, 3)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.look_in_direction(x, y, dir_x, dir_y, fx, fy, snake))
        # look in 135 degree left direction where snake is moving
        (tempx, tempy), new_dir = self.next_position_direction(x, y, direction, 2)
        (new_x, new_y), _ = self.next_position_direction(tempx, tempy, new_dir, 2)
        dir_x, dir_y = new_x - x, new_y - y
        input.extend(self.look_in_direction(x, y, dir_x, dir_y, fx, fy, snake))
        return input

    # feed forward using neural network
    def decision_from_nn(self, x, y, snake, direction):
        closer_to_food = True
        fx, fy = self.nextFood
        input = self.make_input(x, y, fx, fy, snake, direction)
        input = np.array(input)
        # feed forward
        output = input
        for i in range(len(self.weights) - 1):
            output = self.relu(np.dot(output, self.weights[i]) + self.bases[i])
            self.outputs.append(output)
        output = self.softmax(np.dot(output, self.weights[i+1]) + self.bases[i+1])
        self.outputs.append(output)
        result = np.argmax(self.outputs[-1]) + 1
        return result

    # set the next food variable
    def setNextFood(self, food):
        self.nextFood = food

    # sigmoid activation functions
    def sigmoid(self, mat):
        return 1.0 / (1.0 + np.exp(-mat))

    # relu activation function
    def relu(self, mat):
        return mat * (mat > 0)

    # softmax function
    def softmax(self, mat):
        mat = mat - np.max(mat)
        return np.exp(mat) / np.sum(np.exp(mat), axis=1)
