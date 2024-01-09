import random
import numpy as np
from environment.tetris import Tetris
from agents.GeneticAgent import GeneticAgent
from utils.plot import ScatterPlot
from environment.renderer import PyGameRenderer

agent = GeneticAgent(state_size=5, 
                     elite=             2, 
                     population_size=   10, 
                     max_steps=         500, 
                     num_parents=       4, 
                     num_gens=          10)

env = Tetris(10, 20)
renderer = PyGameRenderer(25)

def render(env):
    renderer.render(env)
    renderer.wait(1)
    
def play(agent):
    population = agent.weights
    total_scores = []
    for gen in range(agent.num_gens):
        weight_score = [(weights, agent.get_fitness(env, weights)) for weights in population]
        weight_score.sort(key=lambda x: x[1], reverse=True)
        
        scores = [score for _, score in weight_score]
        total_scores += scores
        
        print(f'| Generation: {gen + 1}\t| Max steps: {agent.max_steps}\t| Pop. size: {agent.population_size}\t| High score: {np.max(scores)}\t| Mean score [Gen {gen+1}]: {np.round(np.mean(scores),2)}\t| Mean score [overall]: {np.round(np.mean(total_scores),2)}\t|')
        
        elite = [weights for weights, _ in weight_score[:agent.elite]]
        parents = [weights for weights, _ in weight_score[:agent.num_parents]]
        
        next_gen = elite[:]
        for _ in range(len(population)-len(elite)):
            parent1, parent2 = random.sample(parents, 2)
            child = agent.breed(parent1, parent2)
            next_gen.append(child)
        
        population = next_gen
        if gen == agent.num_gens-1: print(f'Final best weights: {population[0]}')
    
    
if __name__ == "__main__":
    play(agent)
        
