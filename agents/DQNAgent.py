import os
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import numpy as np
import random


class Net(nn.Module):
    def __init__(self, state_size):
        super(Net, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(state_size, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
        )

    def forward(self, x):
        return self.layers(x)


class DQNAgent:
    def __init__(
        self,
        state_size: int,
        path: str = None,
        memory_size: int = 30000,
        discount: int = 0.95,
        epsilon: int = 1.0,
        epsilon_min: int = 0.01,
        epsilon_end_episode: int = 1500,
        batch_size: int = 512,
        replay_start: int = 2000,
        lr: float = 0.001,
    ):
        self.state_size = state_size
        self.memory = deque(maxlen=memory_size)
        self.discount = discount
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_end_episode = epsilon_end_episode
        self.epsilon_decay = (
            self.epsilon - self.epsilon_min
        ) / self.epsilon_end_episode

        self.batch_size = batch_size
        self.replay_start = replay_start

        self.model = self.initialize_model(state_size, path)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.random_generator = np.random.RandomState()

    def initialize_model(self, state_size: int, path: str = None):
        model = Net(state_size)
        if path and os.path.isfile(path):
            try:
                print("Using pre-trained model")
                model.load_state_dict(torch.load(path))
            except Exception as e:
                print(f"Error loading model: {e}")
        return model

    def add_to_memory(self, current_state, next_state, reward, done):
        self.memory.append([current_state, next_state, reward, done])

    def get_action_by_state(self, states, best_state):
        return next(
            (action for action, state in states.items() if (best_state == state).all()),
            None,
        )

    def act(self, states):
        if np.random.random() <= self.epsilon:
            return random.choice(list(states.keys()))

        state_tensors = torch.FloatTensor(np.array(list(states.values())))
        with torch.no_grad():
            values = self.model(state_tensors)
            return self.get_action_by_state(
                states, list(states.values())[torch.argmax(values).item()]
            )

    def save(self, path):
        torch.save(self.model.state_dict(), path)

    def replay(self):
        if len(self.memory) < self.replay_start:
            return

        batch = random.sample(self.memory, min(len(self.memory), self.batch_size))

        next_states = torch.FloatTensor(np.array([s[1] for s in batch]))
        next_qvalues = self.model(next_states).detach()

        x = np.zeros((len(batch), self.state_size))
        y = np.zeros(len(batch))

        for i, b in enumerate(batch):
            state, _, reward, done = b
            new_q = reward
            if not done:
                new_q += self.discount * next_qvalues[i]

            x[i] = state
            y[i] = new_q

        x_tensor = torch.FloatTensor(x)
        y_tensor = torch.FloatTensor(y)

        self.optimizer.zero_grad()
        outputs = self.model(x_tensor)
        loss = nn.MSELoss()(outputs.squeeze(), y_tensor)
        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon -= self.epsilon_decay
