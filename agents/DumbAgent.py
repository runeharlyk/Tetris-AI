import os
import numpy as np


class DumbAgent:
    def __init__(self, state_size, model_path=None):
        if model_path and os.path.isfile(model_path):
            try:
                self.weights = np.loadtxt(model_path)[:state_size]
                print("Using pre-trained model")
            except Exception as e:
                print(f"Error loading model: {e}")
        else:
            self.weights = np.array(
                [0.15638274, -0.02244227, -0.00440706, -0.2977388, 0.94267344]
            )[:state_size]

    def act(self, states):
        return max(states.items(), key=lambda x: (np.dot(x[1], self.weights)))[0]
