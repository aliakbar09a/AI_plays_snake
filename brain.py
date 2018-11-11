import random
import numpy as np
class brain:
    def __init__(self, layers, width=440, height=440, block=20):
        self.next_step = None
        self.nextFood = None
        self.direction = 'east'
        self.outputs = []
        self.weights = []
        self.bases = []
        self.block = block
        self.width = width
        self.height = height
        # self.cost_weights = np.random.rand(3, 1)
        self.cost_weights = np.array([1,1,1])
        for i in range(len(layers) - 1):
            theta = np.random.rand(layers[i], layers[i+1])
            base = np.random.rand(1, layers[i+1])
            self.weights.append(theta)
            self.bases.append(base)
    def decision_from_nn(self, x, y):
        x, y = pos
        fx, fy = self.nextFood
        max_value = float(400*400)
        food_cost = ((fx - x)**2 + (fy - y)**2)/max_value
        print('food cost = ', food_cost)
        wall_n = ((0 - y)**2)/max_value
        wall_s = ((self.height - y)**2)/max_value
        wall_e = ((self.width - x)**2)/max_value
        wall_w = ((0 - x)**2)/max_value
        wall_cost = wall_n + wall_s + wall_e + wall_w - 1
        print('wall cost->', wall_cost, 'north=', wall_n, 'south=', wall_s, 'west=', wall_w, 'east=', wall_e)
        cost_body = 0
        for i in range(len(snake) - 1, 2, -1):
            # print(i)
            cost_body += ((x - snake[i][0])**2 + (y - snake[i][1])**2)/((i*self.block)**2)
            # print(cost_body)
        cost_body = len(snake) - cost_body
        print('cost body = ', cost_body)
        l = self.block
        input = np.array([])
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
    def cost(self, pos, snake):
        x, y = pos
        fx, fy = self.nextFood
        max_value = float(400*400)
        food_cost = ((fx - x)**2 + (fy - y)**2)/max_value
        print('food cost = ', food_cost)
        wall_n = ((0 - y)**2)/max_value
        wall_s = ((self.height - y)**2)/max_value
        wall_e = ((self.width - x)**2)/max_value
        wall_w = ((0 - x)**2)/max_value
        wall_cost = wall_n + wall_s + wall_e + wall_w - 1
        print('wall cost->', wall_cost, 'north=', wall_n, 'south=', wall_s, 'west=', wall_w, 'east=', wall_e)
        cost_body = 0
        for i in range(len(snake) - 1, 2, -1):
            # print(i)
            cost_body += ((x - snake[i][0])**2 + (y - snake[i][1])**2)/((i*self.block)**2)
            # print(cost_body)
        cost_body = len(snake) - cost_body
        print('cost body = ', cost_body)
        return self.cost_weights[0]*food_cost + self.cost_weights[1]*wall_cost + self.cost_weights[2]*cost_body
    def decision_from_cost(self, x, y, snake):
        min_cost = 1000
        for i in range(3):
            newPos,_ = self.next_position_direction(x, y, i+1, self.direction)
            cost = self.cost(newPos, snake)
            print('cost = ', cost)
            if cost < min_cost:
                result = i+1
                min_cost = cost
        output = np.array([0.0, 0.0, 0.0])
        output[:][result-1] = 1.0
        return output
    def setNextFood(self, food):
        self.nextFood = food
    # def train(self, correct_output):

    # activation functions
    def sigmoid(self, mat):
        return 1.0 / (1.0 + np.exp(-mat))
    def relu(self, mat):
        return mat * (mat > 0)
    def softmax(self, mat):
        mat = mat - np.max(mat)
        return np.exp(mat) / np.sum(np.exp(mat), axis=1)

b = brain([12, 30, 30, 3])
b.setNextFood((100, 300))
b.decision_from_nn(180, 20)
for i in range(2):
    # print(b.weights[i].shape)
    # print(b.bases[i].shape)
    # print(b.outputs[i].shape)
    # print(b.outputs[i])
print(b.decision_from_cost(120, 180, [(120,180),(140,180), (140,160)]))
