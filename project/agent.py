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
            nn.Linear(32, 1)
        )

    def forward(self, x):
        return self.layers(x)

class Agent:
    def __init__(self, state_size, path=None, lr=0.001):
        self.state_size = state_size
        self.memory = deque(maxlen=30000)
        self.discount = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01 
        self.epsilon_end_episode = 200
        self.epsilon_decay = (self.epsilon - self.epsilon_min) / self.epsilon_end_episode

        self.batch_size = 512
        self.replay_start = 00
        self.epochs = 1

        self.model = Net(state_size)
        if path and os.path.isfile(path):
            print("Using pre-trained model")
            self.model.load_state_dict(torch.load(path))
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)

    def add_to_memory(self, current_state, next_state, reward, done):
        self.memory.append([current_state, next_state, reward, done])

    def act(self, states):
        states = list(states)
        state_tensors = torch.FloatTensor(states)
        if random.random() <= self.epsilon:
            return random.choice(states)
        with torch.no_grad():
            values = self.model(state_tensors)
            return states[torch.argmax(values).item()]
    
    def save(self, path):
        torch.save(self.model.state_dict(), path)

    def replay(self):
        # if len(self.memory) > self.replay_start:
        batch = random.sample(self.memory, min(len(self.memory), self.batch_size))

        next_states = torch.FloatTensor([s[1] for s in batch])
        next_qvalues = self.model(next_states).detach()

        x = []
        y = []

        for i, b in enumerate(batch):
            state, _, reward, done = b
            new_q = reward
            if not done:
                new_q += self.discount * next_qvalues[i]

            x.append(state)
            y.append(new_q)

        x_tensor = torch.FloatTensor(x)
        y_tensor = torch.FloatTensor(y)

        self.optimizer.zero_grad()
        outputs = self.model(x_tensor)
        loss = nn.MSELoss()(outputs.squeeze(), y_tensor)
        loss.backward()
        self.optimizer.step()