from tqdm import tqdm
import numpy as np
import multiprocessing
from environment.tetris import Tetris
from agents.GeneticAgent import GeneticAgent

multiprocessing.freeze_support()
from utils.plot import ScatterPlot

level_multi = False
cols = 10
rows = 20
state_size = 5

population_size = 20
elite_pct = 0.1
parent_pct = 0.8

num_generations = 10
max_steps = 1000

mutation_value = 0.02
mutation_rate = 0.05
crossover_rate = 0.7

agent = GeneticAgent(
    state_size,
    elite_pct,
    population_size,
    max_steps,
    num_generations,
    mutation_value,
    mutation_rate,
)


def train():
    envs = [Tetris(cols, rows, level_multi) for _ in range(population_size)]
    plot = ScatterPlot("Games", "Score", "Score per game | training")
    all_scores = np.zeros((num_generations, population_size))
    best_per_gen = np.zeros((num_generations, state_size))
    tqdm.write(
        f"|==== # of generations: {num_generations}\t| Max steps: {max_steps}\t| Pop. size: {population_size}\t| Elite %: {elite_pct} ====|"
    )
    for generation in tqdm(range(agent.num_gens), desc="Generations"):
        args = [(envs[i], weight) for i, weight in enumerate(agent.weights)]
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            fitness_scores = np.array(
                list(
                    tqdm(
                        pool.imap_unordered(agent.get_fitness, args),
                        desc="Population done",
                        leave=False,
                    )
                )
            )

        avg_fitness = np.mean(fitness_scores)
        best_fitness = np.max(fitness_scores)
        print(
            f"Generation {generation + 1}/{num_generations} - Avg Fitness: {avg_fitness:.2f}, Best Fitness: {best_fitness}"
        )

        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = agent.select_parents(agent.weights, fitness_scores)
            if np.random.random() < crossover_rate:
                offspring1, offspring2 = agent.crossover(parent1, parent2)
            else:
                offspring1, offspring2 = parent1, parent2
            new_population.append(agent.mutate(offspring1))
            new_population.append(agent.mutate(offspring2))

        agent.weights = np.array(new_population)[:population_size]

        # agent.weights = agent.weights[fitness_scores.argsort()[::-1]]

        # all_scores[generation] = fitness_scores
        # survivors = int(np.ceil(elite_pct * population_size))
        # parents = agent.weights[: int(population_size * parent_pct) - survivors]

        # for i in range(survivors, population_size, 2):
        #     idx = np.random.randint(0, len(parents), size=2)
        #     parent1, parent2 = parents[idx, :]

        #     best_per_gen[generation] = agent.weights[fitness_scores.argmax()]
        #     if np.random.random() < crossover_rate:
        #         child1, child2 = agent.breed(parent1, parent2)

        #     else:
        #         child1, child2 = parent1, parent2

        #     agent.weights[i] = child1
        #     if i + 1 < population_size:
        #         agent.weights[i + 1] = child2

        for i, fitness_scores in enumerate(fitness_scores):
            plot.add_point(i + generation * population_size, fitness_scores, True)
    tqdm.write(f"Final best weights: {agent.weights[0]}")
    plot.save("genetic_scores.csv")
    np.savetxt("best_weights_per_gen.csv", best_per_gen, delimiter=",")


if __name__ == "__main__":
    train()
