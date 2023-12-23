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

class Cost:
    def __init__(self):
        pass

    def calculate(self, state, cleared_lines, done):
        state_penalties =  np.sum(np.array([0, -0.1, -0.1, -0.01]) * state) # cleared_lines, holes, bumpiness, height
        death_penalty = done * -20
        cleared_lines_reward = cleared_lines ** 2 * 10 + 1
        return death_penalty + cleared_lines_reward + state_penalties

class DumbAgent:
    def __init__(self, state_size):
        self.weights = np.array([-1, -0.5, -0.1])

    def act(self, states):
        return max(states.items(), key=lambda x: (x[1][0], sum(x[1][1:] * self.weights)))[0]


    def add_to_memory(self, current_state, next_state, reward, done):
        pass

    def replay(self):
        pass

class DQLAgent:
    def __init__(self, state_size, path=None, lr=0.001):
        self.costCalc = Cost()
        self.state_size = state_size
        self.memory = deque(maxlen=30000)
        self.discount = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.05 
        self.epsilon_end_episode = 2000
        self.epsilon_decay = (self.epsilon - self.epsilon_min) / self.epsilon_end_episode

        self.batch_size = 512
        self.replay_start = self.batch_size

        self.model = Net(state_size)
        if path and os.path.isfile(path):
            print("Using pre-trained model")
            self.model.load_state_dict(torch.load(path))
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)

    def add_to_memory(self, current_state, next_state, reward, done):
        self.memory.append([current_state, next_state, reward, done])

    def get_action_by_state(self, states, best_state):
        return next((action for action, state in states.items() if (best_state == state).all()), None)
    
    def act(self, states):
        if random.random() <= self.epsilon:
            return random.choice(list(states.keys()))
        
        state_tensors = torch.FloatTensor(np.array(list(states.values())))
        with torch.no_grad():
            values = self.model(state_tensors)
            return self.get_action_by_state(states, list(states.values())[ torch.argmax(values).item()]) #states[torch.argmax(values).item()]
    
    def save(self, path):
        torch.save(self.model.state_dict(), path)

    def replay(self):
        if len(self.memory) < self.replay_start: return

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