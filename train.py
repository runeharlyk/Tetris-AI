from config import *
from controls import Controller
from game import Tetris
from renderer import PyGameRenderer
from agent import DQLAgent, DumbAgent
from plot import ScatterPlot

class Trainer():
    def __init__(self, env, agent) -> None:
        self.env = env
        self.agent = agent
        self.plot = ScatterPlot("", "", "") 
        
        self.key_actions = {
            "quit":     self.quit,
            "pause":    self.pause,
            "down":     self.env.down
        }

        self.renderer = PyGameRenderer(config['cell_size'])
        self.renderer.render(self.env)
    
        self.controller = Controller(self.key_actions)
        self.controller.addEvent(config['delay'])

    def quit(self):
        self.exit_program = True

    def pause(self):
        self.env.paused = not self.env.paused

    def run_episodes(self, max_episode, max_steps):
        rewards = [self.run_episode(i, max_steps) for i in range(max_episode)]
        return rewards

    def run_episode(self, episode, max_steps):
        current_state = self.env.reset()
        score = 0
        total_reward = 0
        done = False
        max_steps = 25000
        step = 0
        self.exit_program = False
        while not self.exit_program:
            self.renderer.render(self.env) 
            next_states = self.env.get_possible_states()
            best_action = agent.act(next_states)
            done, score, reward = env.step(*best_action)
            total_reward += reward

            if done or step > max_steps: break
            self.controller.handleEvents()

            agent.add_to_memory(current_state, next_states[best_action], reward, done)

            current_state = next_states[best_action]

            step += 1
            self.renderer.wait(1)

        agent.replay()

        if agent.epsilon > agent.epsilon_min:
            agent.epsilon -= agent.epsilon_decay

        self.plot.add_point(episode, score, True)
        print(f'Run episode: {episode}\tscore:{score}')
        
        return score

if __name__ == '__main__':
    env = Tetris(config['cols'], config['rows'])
    # agent = DumbAgent(4)
    agent = DQLAgent(4)

    trainer = Trainer(env, agent)
    trainer.run_episodes(4000, 25000)
    trainer.plot.freeze
