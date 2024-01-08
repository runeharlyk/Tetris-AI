import random
import numpy as np
from environment.tetris import Tetris

class GeneticAgent():
    
    def __init__(self, state_size, elite, rows=20,cols=10, population_size=40) -> None:
        self.state_size = state_size
        self.rows = rows
        self.cols = cols
        self.elite = elite
        
        self.weights = [[random.uniform(-1,1) for _ in range(4)] for _ in range(population_size)]
    
    def mutate(self,weights):
        return [w + random.uniform(-0.02,0.02) for w in weights]        
    
    def act(self, states, weights):
        return max(states.items(), key=lambda x: (sum(x[1][i] * weights[i] for i in range(0, 4))))[0]       
        
    def get_fitness(self,weights,max_steps = 1000):
        self.env = Tetris(self.rows,self.cols)
        game_over = False
        
        steps = 0
        while not game_over:
            next_states = self.env.get_possible_states()
            best_action = self.act(next_states,weights)
            done, score, _ = self.env.step(*best_action)
            
            steps += 1
            
            if done or steps > max_steps:
                game_over = True
            
        return score        
    
    def breed(self,parent1,parent2):
        split = random.randint(1, len(parent1) - 1)
        child = parent1[:split] + parent2[split:]
        return self.mutate(child)
    
    def generation(self, weights, steps):
        self.env = Tetris(self.rows,self.cols)
        
        game_results = {} 
        for _ in range(steps):
            weights = self.mutate(weights)
            score = self.get_fitness(weights)
            
            game_results[tuple(w for w in weights)] = score
        
        sorted_results = list(game_results.items()).sort(key = lambda x: x[1])
        best_results = sorted_results[:steps//5]
        
        return best_results
       
    def play(self, num_parents=20, num_gens = 10):
        population = self.weights
        
        for gen in range(num_gens):
            weight_score = [(weights, self.get_fitness(weights)) for weights in population]
            weight_score.sort(key=lambda x: x[1], reverse=True)
            
            scores = [score for _, score in weight_score]
            
            print(f'Generation: {gen + 1} | High score: {np.max(scores)} | Mean score: {np.mean(scores)}')
            elite = [weights for weights, _ in weight_score[:self.elite]]
            parents = [weights for weights, _ in weight_score[:num_parents]]
            
            next_gen = elite[:]
            for _ in range(len(population)-len(elite)):
                parent1, parent2 = random.sample(parents, 2)
                child = self.breed(parent1, parent2)
                next_gen.append(child)
                
            population = next_gen
        
    
if __name__ == "__main__":
    agent = GeneticAgent(state_size=5,elite=3)
    agent.play(100)
        
