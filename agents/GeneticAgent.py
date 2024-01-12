import numpy as np


class GeneticAgent():
    def __init__(self, state_size, elite, population_size, max_steps, num_gens, mutation_value, mutation_chance) -> None:
        self.state_size = state_size
        self.elite = elite
        self.max_steps = max_steps
        self.population_size = population_size
        self.num_gens = num_gens
        self.mutation_value = mutation_value
        self.mutation_chance = mutation_chance
        
        self.weights = np.random.uniform(-1, 1, (population_size, state_size))
        
    def mutate(self,weights):
        for i in range(len(weights)):
            if np.random.random() < self.mutation_chance:
                weights[i] += np.random.uniform(-self.mutation_value, self.mutation_value)       
        return weights
          
    
    def act(self, states, weights):
        return max(states.items(), key=lambda x: (sum(x[1][i] * weight for i, weight in enumerate(weights))))[0]       
        
    def get_fitness(self, args):
        env, weights = args
        env.reset()
        steps = 0
        done = False
        while not done:
            next_states = env.get_possible_states()
            best_action = self.act(next_states, weights)
            done, score, _ = env.step(*best_action)
            
            steps += 1
            
            if steps > self.max_steps:
                break
            
        return score        
    
    def breed(self, parent1, parent2):
        crossover = np.random.randint(1, len(parent1))
        child1 = np.concatenate([parent1[:crossover], parent2[crossover:]])
        child2 = np.concatenate([parent2[:crossover], parent1[crossover:]])
        
        return child1, child2