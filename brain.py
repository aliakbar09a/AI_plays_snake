import random
import numpy as np
class brain:
    weights = []
    bases = []
    outputs = []
    next_step = None
    direction = 'east'
    def __init__(self, layers, width=420, height=420, block=20):
        self.block = block
        self.width = width
        self.height = height
        self.cost_weights = np.random.rand(1,3)
        for i in range(len(layers) - 1):
            theta = np.random.rand(layers[i], layers[i+1])
            base = np.random.rand(1, layers[i+1])
            self.weights.append(theta)
            self.bases.append(base)
    def decision_from_nn(self, x, y):
        l = self.block
        input = np.array([x, y-l, x+l, y, x, y+l, x-l, y])
        # feed forward
        output = input
        for i in range(len(self.weights) - 1):
            output = self.relu(np.dot(output, self.weights[i]) + self.bases[i])
            self.outputs.append(output)
        output = self.softmax(np.dot(output, self.weights[i+1]) + self.bases[i+1])
        self.outputs.append(output)
        result = np.argmax(self.outputs[-1]) + 1
        print('result', result)
        return output
    def next_position_direction(self, x, y, result, direction):
        l = self.block
        if direction == 'north':
            if result == 1:
                return (x, y - l)
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
    def cost(self, pos, food, snake):
        x, y = pos
        fx, fy = food
        max_value = float(400*400)
        food_cost = ((fx - x)**2 + (fy - y)**2)/max_value
        # print('food cost = ', food_cost)
        wall_n = ((20 - y)**2)/max_value
        wall_s = ((self.height - 20 - y)**2)/max_value
        wall_e = ((self.width - 20 - x)**2)/max_value
        wall_w = ((20 - x)**2)/max_value
        wall_cost = 4 - (wall_n + wall_s + wall_e + wall_w)
        # print('wall cost = ', wall_cost)
        cost_body = 0
        for i in range(len(snake), 3, -1):
            cost_body += ((x - snake[i][0])**2 + (y - snake[i][1])**2)/max_value
        cost_body = len(snake) - cost_body
        # print('cost body = ', cost_body)
        return 10*food_cost + 0.1*wall_cost + cost_body
    def decision_from_cost(self, x, y, food, snake):
        min_cost = 1000
        # finding cost for all three possibilities
        for i in range(3):
            newPos,_ = self.next_position_direction(x, y, i+1, self.direction)
            cost = self.cost(newPos, food, snake)
            print('cost = ', cost)
            if cost < min_cost:
                result = i+1
                min_cost = cost
        output = np.array([0.0, 0.0, 0.0])
        output[:][result-1] = 1.0
        return output
    def sigmoid(self, mat):
        return 1.0 / (1.0 + np.exp(-mat))
    def relu(self, mat):
        return mat * (mat > 0)
    def softmax(self, mat):
        mat = mat - np.max(mat)
        return np.exp(mat) / np.sum(np.exp(mat), axis=1)

b = brain([8, 32, 3])
b.decision_from_nn(80, 80)
print(b.outputs[-1])
print(b.decision_from_cost(80, 80, (100, 80), ((80, 80), (60, 80))))
