import random
import numpy as np
from environment.tetris import Tetris
from agents.GeneticAgent import GeneticAgent

agent = GeneticAgent(state_size=5,elite=3)
       
    
def play(agent, num_parents=20, num_gens = 10):
    population = agent.weights
    
    
    for gen in range(num_gens):
        
        weight_score = [(weights, agent.get_fitness(weights)) for weights in population]
        weight_score.sort(key=lambda x: x[1], reverse=True)
        
        scores = [score for _, score in weight_score]
        
        
        print(f'Generation: {gen + 1} | High score: {np.max(scores)} | Mean score: {np.mean(scores)}')
        elite = [weights for weights, _ in weight_score[:agent.elite]]
        parents = [weights for weights, _ in weight_score[:num_parents]]
        
        next_gen = elite[:]
        for _ in range(len(population)-len(elite)):
            parent1, parent2 = random.sample(parents, 2)
            child = agent.breed(parent1, parent2)
            next_gen.append(child)
            
        population = next_gen
    
    
if __name__ == "__main__":
    play(agent, 100)
        
