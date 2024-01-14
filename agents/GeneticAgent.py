import numpy as np


class GeneticAgent:
    def __init__(
        self,
        state_size,
        elite,
        population_size,
        max_steps,
        num_gens,
        mutation_value,
        mutation_rate,
    ) -> None:
        self.state_size = state_size
        self.elite = elite
        self.max_steps = max_steps
        self.population_size = population_size
        self.num_gens = num_gens
        self.mutation_value = mutation_value
        self.mutation_rate = mutation_rate

        self.weights = np.random.uniform(-1, 1, (population_size, state_size))

    def mutate(self, individual):
        for i in range(len(individual)):
            if np.random.random() < self.mutation_rate:
                individual[i] += np.random.normal(0, 0.1)
        return individual

    def select_parents(self, population, fitness_scores, tournament_size=3):
        parents = []
        for _ in range(2):  # Select two parents
            tournament = np.random.choice(len(population), tournament_size)
            best_individual = tournament[
                np.argmax(np.array(fitness_scores)[tournament])
            ]
            parents.append(population[best_individual])
        return parents

    def crossover(self, parent1, parent2):
        crossover_point = np.random.randint(1, len(parent1))
        offspring1 = np.concatenate(
            [parent1[:crossover_point], parent2[crossover_point:]]
        )
        offspring2 = np.concatenate(
            [parent2[:crossover_point], parent1[crossover_point:]]
        )
        return offspring1, offspring2

    def act(self, states, weights):
        return max(states.items(), key=lambda x: (np.dot(x[1], weights)))[0]

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
