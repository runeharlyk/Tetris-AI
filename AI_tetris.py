from Tetris import Tetris
import numpy as np
import pygame
from collections import defaultdict 
import matplotlib.pyplot as plt

class AI:
    def __init__(self, data = dict(), gamma = 0.9, render = False) -> None:
        self.startValue = 100
        self.qTable = defaultdict(lambda: 4*[self.startValue], data)
        self.env = Tetris()
        self.x, self.y, self.has_key = self.env.get_state()
        self.actions = ['left', 'right', 'up', 'down']
        self.exit_program = False
        self.action_taken = False
        self.slow = False
        self.runai = True
        self.render = render
        self.done = False

        self.gamma = gamma
        self.prev_rew = 0
        self.tick = 0
        self.steps = 0
        self.won = 0
        self.wins = 30
        self.res = np.zeros(self.wins)
        self.clock = pygame.time.Clock()


    def  play(self, board_index = 0):
        self.env.reset()
        while not self.exit_program:
            self.tick += 1
            self.steps += 1
            if self.render:
                self.env.render()
            
            # Slow down rendering to 5 fps
            if self.slow and self.runai:
                self.clock.tick(5)
                
            # Automatic reset environment in AI mode
            if self.done and self.runai:
                self.env.reset(board_index)
                self.x, self.y, self.has_key = self.env.get_state()
                
            # Process game events
            for event in pygame.event.get():
                # if event.type == pygame.QUIT:
                #     exit_program = True
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                        exit_program = True
                    if event.key == pygame.K_r:
                        self.env.reset()   
                    if event.key == pygame.K_d:
                        self.render = not self.render
                    if event.key == pygame.K_s:
                        self.slow = not self.slow
                    if event.key == pygame.K_a:
                        self.runai = not self.runai
                        self.clock.tick(5)
            
            # AI controller (enable/disable by pressing 'a')
            if self.runai:

                q_current = self.qTable[(self.x, self.y, self.has_key)]    
                action_num =  np.argmax(q_current)
                action = self.actions[action_num]  
                # 2. step the environment
                (self.x, self.y, self.has_key), reward, self.done = self.env.step(action)
                # 3. update q table
                q_next = self.qTable[(self.x, self.y, self.has_key)]
                q_current[action_num] = reward + self.gamma * np.max(q_next)

                if (reward > self.prev_rew) and self.done and reward != -1:
                    print(self.tick)
                    self.res[self.won] = self.tick
                    self.won += 1
                    self.tick = 0            
                self.prev_rew = reward
                

            if self.won == self.wins:
                return self.res

    def reset(self, board_index):
        self.env.reset(board_index)
        self.prev_rew = 0
        self.tick = 0
        self.steps = 0
        self.won = 0
        self.qTable = defaultdict(lambda: 4*[self.startValue], dict())

    def close(self):
        self.env.close()



if __name__ == '__main__':
    numSamples = 2
    norms = [14, 9, 18, 55]
    descriptions = ['Med vægge', 'Uden vægge']
    res = []
    fig, ax = plt.subplots()
    ax.set(xlabel='Win number', ylabel='Number actions (normalized)', title='Number of action til win')

    AIPlayer = AI(render=True)
    for i in range(numSamples):
        AIPlayer.reset(i) 
        res.append(AIPlayer.play(i))
        ax.plot(res[i] / norms[i], label= descriptions[i])

    print(res)
    plt.show()

    868.0, 58.0, 48.0, 384.0, 63.0, 110.0, 58.0, 273.0, 244.0, 28.0, 156.0, 121.0, 115.0, 63.0, 254.0, 82.0, 99.0, 26.0, 53.0, 81.0, 100.0, 96.0, 103.0, 92.0, 50.0, 20.0, 29.0, 42.0, 28.0, 71.0