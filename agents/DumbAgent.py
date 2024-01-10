import numpy as np


class DumbAgent():
    def __init__(self, state_size):
        self.weights = np.array([0.27803437,-0.62152025,-0.15910121,-0.94336524,0.36147187])

    def act(self, states):
        return max(states.items(), key=lambda x: (sum(x[1][i] * self.weights[i] for i in range(0, 3))))[0]
