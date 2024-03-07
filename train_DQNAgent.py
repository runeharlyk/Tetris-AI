import argparse
import multiprocessing
from tqdm import tqdm
from environment.config import Config
from environment.controls import Controller
from environment.tetris import Tetris
from environment.renderer import PyGameRenderer
from agents.DQNAgent import DQNAgent
from utils.plot import ScatterPlot


parser = argparse.ArgumentParser(prog="Train DQN model")
parser.add_argument("--path", default="models/dqn_10_20.pt")
parser.add_argument("--render", action=argparse.BooleanOptionalAction)
parser.add_argument("--plot", action=argparse.BooleanOptionalAction)
parser.add_argument("--cols", nargs="?", default=10)
parser.add_argument("--rows", nargs="?", default=20)
parser.add_argument("--max_steps", nargs="?", default=1000)
parser.add_argument("--episodes", nargs="?", default=4000)
parser.add_argument("--discount", nargs="?", default=0.99)
parser.add_argument("--epsilon", nargs="?", default=1)
parser.add_argument("--memory_size", nargs="?", default=30000)
parser.add_argument("--epsilon_min", nargs="?", default=0.01)
parser.add_argument("--epsilon_end_episode", nargs="?", default=2000)
parser.add_argument("--batch_size", nargs="?", default=64)
parser.add_argument("--replay_start", nargs="?", default=2000)
parser.add_argument("--lr", nargs="?", default=0.001)
args = parser.parse_args()


class Trainer:
    def __init__(self, env, agent) -> None:
        self.env = env
        self.agent = agent
        self.plot = ScatterPlot("Games", "Score", "DQL training score per game")
        self.render = args.render
        self.should_plot = args.plot
        self.played = self.last_played = 0
        self.exit_program = False
        self.delays = [1, 5, 25, 50, 100]
        self.delays_idx = 0

        self.key_actions = {
            "quit": self.quit,
            "pause": self.pause,
            "down": self.env.down,
            "render": self.toggle_render,
            "plot": self.toggle_plot,
            "print": self.print,
            "up": self.update_delay,
        }

        self.renderer = PyGameRenderer(Config.cell_size)
        self.renderer.render(self.env)

        self.controller = Controller(self.key_actions)
        self.controller.setEventTimer(Config.delay_id, Config.down_delay)
        self.controller.setEventTimer(Config.print_id, Config.print_delay)

    def update_delay(self):
        self.delays_idx += 1

    def toggle_render(self):
        self.render = not self.render

    def toggle_plot(self):
        self.should_plot = not self.should_plot

    def quit(self):
        self.exit_program = True

    def pause(self):
        self.env.paused = not self.env.paused

    def print(self):
        mean_score, std_score, max_score = self.plot.stats()
        tqdm.write(
            f"\tMean:{mean_score}\tstd:{std_score}\tmax:{max_score}\tmemory:{len(self.agent.memory)}"
        )

    def run_episodes(self, max_episode, max_steps):
        try:
            num_processes = multiprocessing.cpu_count()
            with multiprocessing.Pool(processes=num_processes) as pool:
                for i in tqdm(range(max_episode)):
                    self.run_episode(i, max_steps, pool)
                    if self.exit_program:
                        break
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
                self.renderer.wait(self.delays[self.delays_idx % len(self.delays)])

            next_actions = env.get_possible_actions()
            next_states = pool.starmap(env._get_state, next_actions)
            next_action_states = {
                action: next_states[i] for i, action in enumerate(next_actions)
            }

            best_action = agent.act(next_action_states)
            done, score, reward = env.step(*best_action)

            self.controller.handleEvents()

            agent.add_to_memory(
                current_state, next_action_states[best_action], reward, done
            )

            if done or step > max_steps:
                break

            current_state = next_action_states[best_action]

            step += 1

        agent.replay()

        self.plot.add_point(episode, score, self.should_plot)

        return score

    def save(self, name):
        with open(name, "w") as file:
            for value in env.line_clear_types.values():
                file.write(str(value) + ",")


if __name__ == "__main__":
    env = Tetris(args.cols, args.rows, False)
    agent = DQNAgent(
        5,
        None,
        args.memory_size,
        args.discount,
        args.epsilon,
        args.epsilon_min,
        args.epsilon_end_episode,
        args.batch_size,
        args.replay_start,
        args.lr,
    )

    trainer = Trainer(env, agent)
    trainer.run_episodes(args.episodes, args.max_steps)
    trainer.plot.update()
    agent.save(args.path)
    trainer.plot.save("DQN_scores.csv")
    trainer.save("line_clear_types.csv")
    trainer.plot.freeze()
