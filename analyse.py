import argparse
import numpy as np


parser = argparse.ArgumentParser(prog='Analyse results', description='Analyse and compare models')
parser.add_argument('--path', default="results/genetic_1705104088")
args = parser.parse_args()

def analyse(path = None):
    model_path = path or args.path
    scores = np.loadtxt(f'{model_path}/scores.txt')
    line_history = np.loadtxt(f'{model_path}/line_history.txt')

    print(f"n samples:\t{len(scores)}")
    print(f"Mean:\t{np.mean(scores)}")
    print(f"Std:\t{np.std(scores)}")
    print(f"Min:\t{np.min(scores)}")
    print(f"Quantile:\t{np.quantile(scores, [0.25, 0.50, 0.75])}")
    print(f"Max:\t{np.max(scores)}")
    avg_reward = np.sum(scores) / np.sum(np.sum(line_history))
    print(f"Avg score per move:\t{avg_reward}")

if __name__ == "__main__":
    analyse()