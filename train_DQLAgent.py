from environment.config import Config
from environment.controls import Controller
from environment.tetris import Tetris
from environment.renderer import PyGameRenderer
from agents.DQLAgent import DQLAgent
from utils.plot import ScatterPlot

class Trainer():
    def __init__(self, env, agent) -> None:
        self.env = env
        self.agent = agent
        self.plot = ScatterPlot("Games", "Score", "DQL training score per game") 
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
        self.controller.addEvent(Config.delay_id, Config.down_delay)
        self.controller.addEvent(Config.print_id, Config.print_delay)

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
        print(f'Episodes:{self.played}\tGames per second:{games_per_sec}\tMean:{mean_score}\tstd:{std_score}\tmax:{max_score}\tmemory:{len(self.agent.memory)}')

    def run_episodes(self, max_episode, max_steps):
        try:
            rewards = [self.run_episode(i, max_steps) for i in range(max_episode)]
            return rewards
        except Exception as error:
            print(error)
        finally:
            return []

    def run_episode(self, episode, max_steps):
        self.played = episode
        current_state = self.env.reset()
        score = 0
        done = False
        max_steps = 25000
        step = 0
        self.exit_program = False
        while not self.exit_program:
            if self.render:
                self.renderer.render(self.env) 
                self.renderer.wait(1)
            next_states = self.env.get_possible_states()
            best_action = agent.act(next_states)
            done, score, reward = env.step(*best_action)

            self.controller.handleEvents()

            agent.add_to_memory(current_state, next_states[best_action], reward, done)

            if done or step > max_steps: break

            current_state = next_states[best_action]

            step += 1

        agent.replay()

        self.plot.add_point(episode, score, self.should_plot)
        
        return score

if __name__ == '__main__':
    width, height = Config.cols, Config.rows
    model_path = f'model_dql_{width}_{height}.pt'

    env = Tetris(width, height)
    agent = DQLAgent(4)

    trainer = Trainer(env, agent)
    trainer.run_episodes(10000, 25000)
    trainer.plot.update()
    agent.save(model_path)
    trainer.plot.freeze()
