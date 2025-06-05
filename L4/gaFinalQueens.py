import random
from queens_fitness import fitness_fn_positive

# Params you might wanna tweak for experiments or if exam asks:
p_mutation = 0.2            # mutation chance, higher means more randomness
num_of_generations = 20    # max loops to try evolving solution
population_size = 20         # how many candidate solutions at once
n = 8                        # board size AND number of queens

def genetic_algorithm(population, fitness_fn, max_fitness):
    for generation in range(num_of_generations):  # just keep going for set generations
        print(f"Generation {generation}:")
        print_population(population, fitness_fn)  # see what's inside population

        new_population = set()

        # fill up the next gen population by making new children
        while len(new_population) < population_size:
            mother, father = random_selection(population, fitness_fn)  # pick 2 parents, fitness based
            child1, child2 = reproduce(mother, father)  # crossover to get kids

            # chance to randomly change one queen pos to keep diversity
            if random.uniform(0, 1) < p_mutation:
                child1 = mutate(child1)
            if random.uniform(0, 1) < p_mutation:
                child2 = mutate(child2)

            new_population.add(child1)
            if len(new_population) < population_size:
                new_population.add(child2)

        # combine old and new, keep the best only (based on fitness)
        combined = population.union(new_population)
        population = set(sorted(combined, key=fitness_fn, reverse=True)[:population_size])

        fittest_individual = get_fittest_individual(population, fitness_fn)
        best_fitness = fitness_fn(fittest_individual)
        print(f"Best fitness: {best_fitness}\n")

        # stop early if we hit max fitness, solution found
        if best_fitness >= max_fitness:
            print(f"Solution found at generation {generation}")
            break

    print("Final population:")
    print_population(population, fitness_fn)
    return fittest_individual


def print_population(population, fitness_fn):
    # just print each individual + its fitness
    for individual in population:
        fitness = fitness_fn(individual)
        print(f"{individual} - fitness: {fitness}")


def reproduce(mother, father):
    # cut & mix genes at a random crossover point
    crossover_point = random.randint(1, len(mother) - 1)
    child1 = mother[:crossover_point] + father[crossover_point:]
    child2 = father[:crossover_point] + mother[crossover_point:]
    return tuple(child1), tuple(child2)


def mutate(individual):
    # randomly pick a queen and put it in a new row (1-indexed)
    mutated = list(individual)
    index_to_mutate = random.randint(0, len(individual) - 1)
    new_row = random.randint(1, n)
    while new_row == mutated[index_to_mutate]:
        new_row = random.randint(1, n)
    mutated[index_to_mutate] = new_row
    return tuple(mutated)


def random_selection(population, fitness_fn):
    # roulette wheel style selection based on fitness values
    ordered_population = list(population)
    fitness_values = [fitness_fn(ind) for ind in ordered_population]
    total_fitness = sum(fitness_values)

    # if all fitness 0, just pick random parents
    if total_fitness == 0:
        return random.choice(ordered_population), random.choice(ordered_population)

    cumulative_fitness = []
    running_total = 0
    for fitness in fitness_values:
        running_total += fitness
        cumulative_fitness.append(running_total)

    def select_one():
        r = random.uniform(0, total_fitness)
        for i, cf in enumerate(cumulative_fitness):
            if r <= cf:
                return ordered_population[i]

    return select_one(), select_one()


def get_fittest_individual(population, func):
    # returns the individual with best fitness
    return max(population, key=func)


def get_initial_population(n, count):
    # create starting population, tuples of queen positions (1-indexed rows)
    return set(
        tuple(random.randint(1, n) for _ in range(n))
        for _ in range(count)
    )


def main():
    # max fitness = all pairs of queens non-attacking: n choose 2 basically
    max_fitness = n * (n - 1) // 2

    # get initial random population
    population = get_initial_population(n, population_size)

    # run GA to find solution
    solution = genetic_algorithm(population, fitness_fn_positive, max_fitness)
    print(f"Fittest Individual: {solution}")
    print(f"Fitness: {fitness_fn_positive(solution)}")


if __name__ == "__main__":
    main()