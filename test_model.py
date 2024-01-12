from tqdm import tqdm
import argparse
import time
import csv
import statistics
import os

from environment.controls import Controller
from environment.tetris import Tetris
from environment.renderer import PyGameRenderer
from utils.plot import ScatterPlot

from agents.DQNAgent import DQNAgent
from agents.DumbAgent import DumbAgent

def load_agent(model, model_path):
    match model:
        case "DQN":
            return DQNAgent(5, model_path, 0)
        case "genetic":
            return DumbAgent(5, model_path)

parser = argparse.ArgumentParser(prog='Test model', description='Test and evaluate model')
parser.add_argument('--model', choices=['DQN', 'genetic'], default="DQN")
parser.add_argument('--path', default="model_dqn_10_20.pt")
parser.add_argument('--render', action=argparse.BooleanOptionalAction)
parser.add_argument('--plot', action=argparse.BooleanOptionalAction)
parser.add_argument('--cols', nargs='?', default=10) 
parser.add_argument('--rows', nargs='?', default=20)
parser.add_argument('--max_steps', nargs='?', default=200)
parser.add_argument('--samples', nargs='?', default=10)
parser.add_argument('--out', nargs='?', default="results")
args = parser.parse_args()

env = Tetris(args.cols, args.rows)
agent = load_agent(args.model, args.path)
if args.plot:
    plot = ScatterPlot("Games", "Score", "Score per game") 

if args.render:
    renderer = PyGameRenderer(30)
    controller = Controller()

scores = []
reward_counts = []
def save_results():
    now = str(time.time()).split('.')[0]
    path = f"{args.out}/{args.model}_{now}"
    os.makedirs(path, exist_ok=True)
    with open(f'{path}/scores.csv', 'w') as file:
        for score in scores:
            file.write(f'{score}\n')
    with open(f'{path}/piece_history.csv', 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(reward_counts)

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
        
    scores.append(score)
    reward_counts.append(list(env.line_clear_types.values()))

save_results()

if args.plot:
    plot.update()
    plot.freeze()
