import numpy as np


class DumbAgent():
    def __init__(self, state_size):
        self.weights = np.array([0.064, -0.31, -0.29, -0.89])

    def act(self, states):
        return max(states.items(), key=lambda x: (sum(x[1][i] * self.weights[i] for i in range(0, 3))))[0]
