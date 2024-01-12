import multiprocessing
from environment.config import Config
from environment.controls import Controller
from environment.tetris import Tetris
from environment.renderer import PyGameRenderer
from agents.DQNAgent import DQNAgent
from utils.plot import ScatterPlot

class Trainer():
    def __init__(self, env, agent) -> None:
        self.env = env
        self.agent = agent
        self.plot = ScatterPlot("Games", "Score", "DQL training score per game") 
        self.render = True
        self.should_plot = True
        self.played = self.last_played = 0
        self.exit_program = False

        
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
        print(f'Episodes:{self.played}\tGames per second:{games_per_sec}\tMean:{mean_score}\tstd:{std_score}\tmax:{max_score}\tmemory:{len(self.agent.memory)}')

    def run_episodes(self, max_episode, max_steps):
        try:
            num_processes = multiprocessing.cpu_count()
            with multiprocessing.Pool(processes = num_processes) as pool:
                rewards = [self.run_episode(i, max_steps, pool) for i in range(max_episode) if not self.exit_program]
                return rewards
        except Exception as error:
            print(error)
            self.exit_program = True
        finally:
            pool.close()
            pool.join()
            return []

    def run_episode(self, episode, max_steps, pool):
        self.played = episode
        current_state = self.env.reset()
        score = 0
        done = False
        step = 0
        
        while not done:
            if self.render:
                self.renderer.render(self.env) 
                self.renderer.wait(1)

            next_actions = env.get_possible_actions()
            next_states = pool.starmap(env._get_state, next_actions)
            next_action_states = {action:next_states[i] for i, action in enumerate(next_actions)}

            best_action = agent.act(next_action_states)
            done, score, reward = env.step(*best_action)

            self.controller.handleEvents()

            agent.add_to_memory(current_state, next_action_states[best_action], reward, done)

            if done or step > max_steps: break

            current_state = next_action_states[best_action]

            step += 1

        agent.replay()

        self.plot.add_point(episode, score, self.should_plot)
        
        return score

    def save(self, name):
        with open(name, 'w') as file:
            for value in env.line_clear_types.values():
                file.write(str(value) + ',')
if __name__ == '__main__':
    width, height = Config.cols, Config.rows
    model_path = f'model_dql_{width}_{height}.pt'

    env = Tetris(width, height, False)
    agent = DQNAgent(5)

    trainer = Trainer(env, agent)
    trainer.run_episodes(10000, 1000)
    trainer.plot.update()
    agent.save(model_path)
    trainer.save("line_clear_types.csv")
    trainer.plot.freeze()
