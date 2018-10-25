import random
import numpy as np

class brain:
    weights = []
    def __init__(self, layers):
        self.layers = layers
        for i in range(len(layers) - 1):
            theta = np.random.rand(layers[i], layers[i+1])
            self.weights.append(theta)

b = brain([12, 32, 32, 3])
