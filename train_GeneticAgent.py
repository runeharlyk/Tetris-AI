import random
import numpy as np
from environment.tetris import Tetris
from agents.GeneticAgent import GeneticAgent
from utils.plot import ScatterPlot

state_size      = 5
elite           = 2
population_size = 20
max_steps       = 500
num_parents     = 8
num_gens        = 10
mutation_value  = 0.02
mutation_chance = 0.9
crossover_rate  = 0.7

agent = GeneticAgent(state_size, elite, population_size, max_steps, num_parents, num_gens, mutation_value, mutation_chance)
env = Tetris(10, 20)

plot = ScatterPlot("Games", "Score", "Score per game | training")
    
total_scores = []

print(f'|==== # of generations: {num_gens}\t| Max steps: {max_steps}\t| Pop. size: {population_size}\t| # of elite/parents: {elite}/{num_parents} ====|')
for gen in range(agent.num_gens):
    weight_score = [(weights, agent.get_fitness(env, weights)) for weights in agent.weights]
    for i, (_, score) in enumerate(weight_score):
        plot.add_point(i + gen * population_size, score, True)

    weight_score.sort(key=lambda x: x[1], reverse=True)
    
    scores = [score for _, score in weight_score]
    weights = [weight for weight, _ in weight_score]
    
    total_scores += scores
    print(f'| Generation: {gen+1:0{len(str(num_gens))}d}\t| Min./Mean/Max. [Gen {gen+1}]: {np.min(scores)} / {np.round(np.mean(scores),2)} / {np.max(scores)}\t| Min./Mean/Max. [Overall]: {np.min(total_scores)} / {np.round(np.mean(total_scores),2)} / {np.max(total_scores)}\t|')
    
    next_gen    = weights[:agent.elite]
    parents     = weights[:agent.num_parents]
    
    while len(next_gen) < population_size:
        parent1, parent2 = random.sample(parents, 2)
        if np.random.random() < crossover_rate:
            child1, child2 = agent.breed(parent1, parent2)
        else:   
            child1, child2 = parent1, parent2
        
        next_gen.append(child1)
        if len(next_gen) % 2 == 1:
            next_gen.append(child2)
    
    agent.weights = next_gen
    
print(f'Final best weights: {agent.weights[0]}')

plot.update()
plot.freeze()   
