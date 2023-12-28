import random


class ChaoticAgent():
    def act(self, states):
        return random.choice(list(states.keys()))