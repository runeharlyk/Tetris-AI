import random
import numpy as np
import multiprocessing
from environment.tetris import Tetris
from agents.GeneticAgent import GeneticAgent
multiprocessing.freeze_support()
from utils.plot import ScatterPlot

level_multi     = False
cols            = 10
rows            = 20
state_size      = 5

population_size = 10
elite_pct       = 0.1
parent_pct      = 0.7

num_gens        = 20
max_steps       = 500

mutation_value  = 0.02
mutation_chance = 0.95
crossover_rate  = 0.5

agent = GeneticAgent(state_size, elite_pct, population_size, max_steps, num_gens, mutation_value, mutation_chance)

def print_gen_stats(gen,gen_scores,all_scores):
    print(f'|==\tMin./Mean/Max./Std. [Gen {gen+1}]: {np.min(gen_scores)} | {np.round(np.mean(gen_scores),2)} | {np.max(gen_scores)} | {np.round(np.std(gen_scores),2)}\t|| Min./Mean/Max./Std. [Overall]: {np.min(all_scores[:gen+1])} | {np.round(np.mean(all_scores[:gen+1]),2)} | {np.max(all_scores[:gen+1])} | {np.round(np.std(all_scores),2)}\t==|')

def train(plotting):
    if plotting: plot = ScatterPlot("Games", "Score", "Score per game | training")
    all_scores = np.zeros((num_gens, population_size))
    
    print(f'||==\t# of generations: {num_gens}\t| Max steps: {max_steps}\t| Pop. size: {population_size}\t| Elite %: {elite_pct}\t==||')
    
    num_processes = multiprocessing.cpu_count()
    for gen in range(agent.num_gens):
        args = [(Tetris(cols, rows, level_multi), weight) for weight in agent.weights]
        try:
            with multiprocessing.Pool(processes = num_processes) as pool:
                gen_scores = np.array(pool.starmap(agent.get_fitness, args))
        except Exception as error:
            print(error)
        finally:
            pool.close()
            pool.join()
            pass

        agent.weights = agent.weights[gen_scores.argsort()[::-1]]
        
        all_scores[gen] = gen_scores
        survivors = int(np.ceil(elite_pct*population_size))
        
        print_gen_stats(gen,gen_scores,all_scores)
        
        parents = agent.weights[:int(population_size*parent_pct)-survivors]
        
        for i in range(survivors, population_size, 2):
            idx = np.random.randint(0, len(parents), size=2)
            parent1, parent2 = parents[idx,:]
            
            if np.random.random() < crossover_rate:
                child1, child2 = agent.breed(parent1, parent2)
                
            else:   
                child1, child2 = parent1, parent2
            
            agent.weights[i] = child1
            if i + 1 < population_size:
                agent.weights[i+1] = child2
        for i, score in enumerate(gen_scores):
            if plotting: plot.add_point(i+gen*population_size,score, True)
            
    print(f'Final best weights: {agent.weights[0]}')  

if __name__ == '__main__': 
    train(False)
