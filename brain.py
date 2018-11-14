import random
import numpy as np
class brain:
    def __init__(self, layers, width=440, height=440, block=20):
        self.nextFood = None
        self.outputs = []
        self.weights = []
        self.prev_result = 1
        self.bases = []
        self.block = block
        self.width = width
        self.height = height
        for i in range(len(layers) - 1):
            theta = np.random.uniform(low=-1.0, high=1.0, size=(layers[i], layers[i+1]))
            base = np.random.uniform(low=-0.05, high=0.05, size=(1, layers[i+1]))
            self.weights.append(theta)
            self.bases.append(base)
    def direction_one_hot_encoding(self, direction):
        if direction == 'north':
            return np.array([1., .0, .0, .0])
        elif direction == 'east':
            return np.array([.0, 1., .0, .0])
        elif direction == 'south':
            return np.array([.0, .0, 1., .0])
        else:
            return np.array([.0, .0, .0, 1.])
    def ifAteFood(self, x, y):
        if x == self.nextFood[0] and y == self.nextFood[1]:
            return True
        else:
            return False
    def decision_from_nn(self, x, y, snake, direction):
        fx, fy = self.nextFood
        max_value = float((self.width-2*self.block)*(self.height-2*self.block))
        food_cost = ((fx - x)**2 + (fy - y)**2)/max_value
        # food_cost /= 10
        # print('food cost = ', food_cost)
        wall_n = ((0 - y)**2)/max_value
        wall_s = ((self.height - y)**2)/max_value
        wall_e = ((self.width - x)**2)/max_value
        wall_w = ((0 - x)**2)/max_value
        # print('north=', wall_n, 'south=', wall_s, 'west=', wall_w, 'east=', wall_e)
        cost_body = 0
        for i in range(len(snake) - 1, 2, -1):
            # print(i)
            cost_body += ((x - snake[i][0])**2 + (y - snake[i][1])**2)/(max_value)
            # print(cost_body)
        # cost_body = len(snake) - cost_body
        # print('cost body = ', cost_body)
        dir = self.direction_one_hot_encoding(direction)
        # dir = dir/4
        # print(dir)
        input = np.array([food_cost, wall_n, wall_s, wall_e, wall_w, cost_body])
        input = np.append(input, dir)
        # print(input, end='\t')
        # feed forward
        output = input
        for i in range(len(self.weights) - 1):
            output = self.relu(np.dot(output, self.weights[i]) + self.bases[i])
            self.outputs.append(output)
        output = self.softmax(np.dot(output, self.weights[i+1]) + self.bases[i+1])
        # output = self.relu(np.dot(output, self.weights[i+1]) + self.bases[i+1])
        self.outputs.append(output)
        result = np.argmax(self.outputs[-1]) + 1
        # print('result', result, end='\t')
        # print(output)
        return result, self.ifAteFood(snake[0][0], snake[0][1])
    # def cost(self, pos, snake):
    #     x, y = pos
    #     fx, fy = self.nextFood
    #     max_value = float(400*400)
    #     food_cost = ((fx - x)**2 + (fy - y)**2)/max_value
    #     print('food cost = ', food_cost)
    #     wall_n = ((0 - y)**2)/max_value
    #     wall_s = ((self.height - y)**2)/max_value
    #     wall_e = ((self.width - x)**2)/max_value
    #     wall_w = ((0 - x)**2)/max_value
    #     wall_cost = wall_n + wall_s + wall_e + wall_w - 1
    #     print('wall cost->', wall_cost, 'north=', wall_n, 'south=', wall_s, 'west=', wall_w, 'east=', wall_e)
    #     print('food cost = ', food_cost)
    #     wall_n = ((20 - y)**2)/max_value
    #     wall_s = ((self.height - 20 - y)**2)/max_value
    #     wall_e = ((self.width - 20 - x)**2)/max_value
    #     wall_w = ((20 - x)**2)/max_value
    #     wall_cost = 4 - (wall_n + wall_s + wall_e + wall_w)
    #     print('wall cost = ', wall_cost)
    #     cost_body = 0
    #     for i in range(len(snake) - 1, 2, -1):
    #         # print(i)
    #         cost_body += ((x - snake[i][0])**2 + (y - snake[i][1])**2)/((i*self.block)**2)
    #         # print(cost_body)
    #     cost_body = len(snake) - cost_body
    #     print('cost body = ', cost_body)
    #     return 10*food_cost + 0.1*wall_cost + cost_body
    # def decision_from_cost(self, x, y, snake):
    #     min_cost = 1000
    #     # finding cost for all three possibilities
    #     for i in range(3):
    #         newPos,_ = self.next_position_direction(x, y, i+1, self.direction)
    #         cost = self.cost(newPos, snake)
    #         print('cost = ', cost)
    #         if cost < min_cost:
    #             result = i+1
    #             min_cost = cost
    #     output = np.array([0.0, 0.0, 0.0])
    #     output[:][result-1] = 1.0
    #     return output
    def setNextFood(self, food):
        self.nextFood = food

    # activation functions
    def sigmoid(self, mat):
        return 1.0 / (1.0 + np.exp(-mat))
    def relu(self, mat):
        return mat * (mat > 0)
    def softmax(self, mat):
        mat = mat - np.max(mat)
        return np.exp(mat) / np.sum(np.exp(mat), axis=1)

if __name__ == '__main__':
    b = brain([10, 8, 3])
    b.setNextFood((100, 300))
    b.decision_from_nn(80, 80, ((80, 80), (60, 80)), 'east')
    b.decision_from_nn(80, 80, ((80, 80), (60, 80)), 'west')
    b.decision_from_nn(80, 80, ((80, 80), (60, 80)), 'north')
    b.decision_from_nn(80, 80, ((80, 80), (60, 80)), 'south')

    # print(b.decision_from_cost(80, 80, ((80, 80), (60, 80))))
