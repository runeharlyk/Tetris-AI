import random
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
        self.env = Tetris(self.cols,self.rows)
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