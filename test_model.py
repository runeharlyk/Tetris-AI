from tqdm import tqdm
import argparse
import time
import os

from environment.controls import Controller
from environment.tetris import Tetris
from environment.renderer import PyGameRenderer
from utils.plot import ScatterPlot

from agents.DQNAgent import DQNAgent
from agents.DumbAgent import DumbAgent


def load_agent(model, model_path):
    tqdm.write(f"Loading model:{model} from {model_path}")
    match model:
        case "dqn":
            return DQNAgent(5, model_path, epsilon=0)
        case "genetic":
            return DumbAgent(5, model_path)


parser = argparse.ArgumentParser(
    prog="Test model", description="Test and evaluate model"
)
parser.add_argument("--model", choices=["dqn", "genetic"], default="dqn")
parser.add_argument("--path", default="models/dqn_10_20.pt")
parser.add_argument("--render", action=argparse.BooleanOptionalAction)
parser.add_argument("--plot", action=argparse.BooleanOptionalAction)
parser.add_argument("--cols", nargs="?", default=10)
parser.add_argument("--rows", nargs="?", default=20)
parser.add_argument("--max_steps", nargs="?", default=1000)
parser.add_argument("--samples", nargs="?", default=50)
parser.add_argument("--out", nargs="?", default="results")
parser.add_argument("--level_multi", action=argparse.BooleanOptionalAction)
args = parser.parse_args()

env = Tetris(args.cols, args.rows, args.level_multi)
agent = load_agent(args.model, args.path)
if args.plot:
    plot = ScatterPlot("Games", "Score", "Score per game")

if args.render:
    renderer = PyGameRenderer(30)
    controller = Controller()

now = str(time.time()).split(".")[0]
path = f"{args.out}/{args.model}_{now}"
os.makedirs(path, exist_ok=True)
scores = open(f"{path}/scores.txt", "w", newline="")
line_history = open(f"{path}/line_history.txt", "w", newline="")

for game in tqdm(range(args.samples)):
    env.reset()
    steps = 0
    done = False
    while not done:
        if args.render:
            renderer.render(env)
            renderer.wait(1)
            controller.handleEvents()

        next_states = env.get_possible_states()
        best_action = agent.act(next_states)
        done, score, _ = env.step(*best_action)

        steps += 1

        if steps > args.max_steps:
            break

    if args.plot:
        plot.add_point(game, score, args.plot)

    scores.write(f"{score}\n")
    line_history.write(f'{" ".join(map(str, list(env.line_clear_types.values())))}\n')

scores.close()
line_history.close()

if args.plot:
    plot.update()
    plot.freeze()
