from multiprocessing import Pool
from tqdm import tqdm
import argparse
import time
import os

from environment.tetris import Tetris
from environment.renderer import PyGameRenderer
from agents.DQNAgent import DQNAgent
from agents.DumbAgent import DumbAgent

renderer = PyGameRenderer(20)

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
parser.add_argument("--render", action=argparse.BooleanOptionalAction, default=True)
parser.add_argument("--plot", action=argparse.BooleanOptionalAction, default=True)
parser.add_argument("--benchmark", action=argparse.BooleanOptionalAction)
parser.add_argument("--cols", nargs="?", default=10)
parser.add_argument("--rows", nargs="?", default=20)
parser.add_argument("--max_steps", nargs="?", default=2000)
parser.add_argument("--samples", nargs="?", default=5)
parser.add_argument("--out", nargs="?", default="results")
parser.add_argument("--level_multi", action=argparse.BooleanOptionalAction)


def worker_function(args):
    env = Tetris(args.cols, args.rows, args.level_multi)
    agent = load_agent(args.model, args.path)
    env.reset()
    steps = 0
    done = False
    while not done:
        if args.render and not args.benchmark:
            renderer.render(env) 
            renderer.wait(1)
        next_states = env.get_possible_states()
        best_action = agent.act(next_states)
        done, score, _ = env.step(*best_action)

        steps += 1

        if steps > args.max_steps:
            break
    return score, list(env.line_clear_types.values())


def benchmark():
    scores = open(f"{path}/scores.txt", "w", newline="")
    line_history = open(f"{path}/line_history.txt", "w", newline="")

    with Pool() as pool:
        results = list(
            tqdm(
                pool.imap_unordered(
                    worker_function,
                    [args for _ in range(args.samples)],
                    chunksize=1,
                ),
                total=args.samples,
            )
        )

    with open(f"{path}/scores.txt", "w", newline="") as scores, open(
        f"{path}/line_history.txt", "w", newline=""
    ) as line_history:
        for score, line_history_data in results:
            scores.write(f"{score}\n")
            line_history.write(f'{" ".join(map(str, list(line_history_data)))}\n')


if __name__ == "__main__":
    args = parser.parse_args()

    now = str(time.time()).split(".")[0]
    path = f"{args.out}/{args.model}_{now}"
    os.makedirs(path, exist_ok=True)

    if args.benchmark:
        benchmark()
    else:
        while True:
            worker_function(args)