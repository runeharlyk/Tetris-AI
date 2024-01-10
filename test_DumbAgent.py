from environment.config import Config
from environment.controls import Controller
from environment.tetris import Tetris
from environment.renderer import PyGameRenderer
from agents.DumbAgent import DumbAgent
from utils.plot import ScatterPlot

class Tester():
    def __init__(self, env, agent) -> None:
        self.env = env
        self.agent = agent
        self.plot = ScatterPlot("", "", "") 
        self.render = True
        self.should_plot = True
        self.played = self.last_played = 0
        
        self.key_actions = {
            "quit":     self.quit,
            "pause":    self.pause,
            "down":     self.env.down,
            "render":   self.toggle_render,
            "plot":     self.toggle_plot,
            "print":    self.print

        }

        self.renderer = PyGameRenderer(Config.cell_size)
        self.renderer.render(self.env)
    
        self.controller = Controller(self.key_actions)
        self.controller.setEventTimer(Config.delay_id, Config.down_delay)
        self.controller.setEventTimer(Config.print_id, Config.print_delay)

    def toggle_render(self):
        self.render = not self.render

    def toggle_plot(self):
        self.should_plot = not self.should_plot

    def quit(self):
        self.exit_program = True

    def pause(self):
        self.env.paused = not self.env.paused

    def print(self):
        games_per_sec = self.played - self.last_played
        self.last_played = self.played
        mean_score, std_score, max_score = self.plot.stats()
        print(f'Games per second:{games_per_sec}\tMean:{mean_score}\tstd:{std_score}\tmax:{max_score}')

    def run(self, games):
        for i in range(games):
            self.play(i)

    def play(self, game):
        self.played = game
        self.env.reset()
        score = 0
        total_reward = 0
        done = False
        self.exit_program = False
        while not self.exit_program:
            if self.render:
                self.renderer.render(self.env) 
                self.renderer.wait(1)
            next_states = self.env.get_possible_states()
            best_action = agent.act(next_states)
            done, score, reward = env.step(*best_action)
            total_reward += reward

            if done: break
            self.controller.handleEvents()

        self.plot.add_point(game, score, self.should_plot)
        
        return score

if __name__ == '__main__':
    width, height = Config.cols, Config.rows
    model_path = f'model_dql_{width}_{height}.pt'

    env = Tetris(width, height)
    agent = DumbAgent(5)

    tester = Tester(env, agent)
    tester.run(1000)
    tester.plot.update()
    tester.plot.freeze
