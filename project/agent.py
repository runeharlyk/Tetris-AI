import random

class Agent():
    def __init__(self) -> None:
        self.epsilon = 1
        pass

    def get_best_state(self, states):
        if random.random() <= self.epsilon:
            return random.choice(list(states))