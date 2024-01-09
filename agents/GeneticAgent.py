import numpy as np


class GeneticAgent():
    def __init__(self, state_size, elite, population_size, max_steps, num_parents, num_gens) -> None:
        self.state_size = state_size
        self.elite = elite
        self.max_steps = max_steps
        self.population_size = population_size
        self.num_parents = num_parents
        self.num_gens = num_gens
        
        self.weights = np.random.uniform(-1, 1, (population_size, state_size))
    def mutate(self,weights):
        return [w + np.random.uniform(-0.02, 0.02) for w in weights]        
    
    def act(self, states, weights):
        return max(states.items(), key=lambda x: (sum(x[1][i] * weights[i] for i in range(0, 4))))[0]       
        
    def get_fitness(self, env, weights):
        env.reset()
        steps = 0
        done = False
        while not done:
            next_states = env.get_possible_states()
            best_action = self.act(next_states,weights)
            done, score, _ = env.step(*best_action)
            
            steps += 1
            
            if steps > self.max_steps:
                break
            
        return score        
    
    def breed(self,parent1,parent2):
        split = np.random.randint(1, len(parent1) - 1)
        child = np.concatenate([parent1[:split], parent2[split:]]) 
        return self.mutate(child)