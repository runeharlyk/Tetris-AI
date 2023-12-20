import os
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import numpy as np
import random
import sys

class Net(nn.Module):
    def __init__(self, state_size):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(state_size, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 32)
        self.fc4 = nn.Linear(32, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        return self.fc4(x)

class Agent:
    def __init__(self, state_size, path=None):
        self.state_size = state_size
        self.memory = deque(maxlen=30000)
        self.discount = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.001 
        self.epsilon_end_episode = 2000
        self.epsilon_decay = (self.epsilon - self.epsilon_min) / self.epsilon_end_episode

        self.batch_size = 512
        self.replay_start = 3000
        self.epochs = 1

        self.model = Net(state_size)
        if path and os.path.isfile(path):
            self.model.load_state_dict(torch.load(path))
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)

    def add_to_memory(self, current_state, next_state, reward, done):
        self.memory.append([current_state, next_state, reward, done])

    def act(self, states):
        max_value = -sys.maxsize - 1
        best = None

        if random.random() <= self.epsilon:
            return random.choice(list(states))
        else:
            with torch.no_grad():
                for state in states:
                    state_tensor = torch.FloatTensor(state).unsqueeze(0)
                    value = self.model(state_tensor).item()
                    if value > max_value:
                        max_value = value
                        best = state

        return best
    
    def save(self, path):
        torch.save(self.model.state_dict(), path)

    def replay(self):
        if len(self.memory) > self.replay_start:
            batch = random.sample(self.memory, self.batch_size)

            next_states = torch.FloatTensor([s[1] for s in batch])
            next_qvalues = self.model(next_states).detach()

            x = []
            y = []

            for i in range(self.batch_size):
                state, _, reward, done = batch[i]
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