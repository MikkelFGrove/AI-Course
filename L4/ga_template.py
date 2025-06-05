import random

# Parameters
p_mutation = 0.2
num_of_generations = 30


def genetic_algorithm(population, fitness_fn, minimal_fitness):
    for generation in range(num_of_generations):
        print("Generation {}:".format(generation))
        print_population(population, fitness_fn)

        new_population = set()

        for _ in range(len(population)):
            mother, father = random_selection(population, fitness_fn)
            child = reproduce(mother, father)

            if random.uniform(0, 1) < p_mutation:
                child = mutate(child)

            new_population.add(child)

        # Combine populations and remove duplicates
        population = population.union(new_population)

        fittest_individual = get_fittest_individual(population, fitness_fn)

        if minimal_fitness <= fitness_fn(fittest_individual):
            break

    print("Final generation {}:".format(generation))
    print_population(population, fitness_fn)

    return fittest_individual


def print_population(population, fitness_fn):
    for individual in population:
        fitness = fitness_fn(individual)
        print("{} - fitness: {}".format(individual, fitness))


def reproduce(mother, father):
    '''
    Perform single-point crossover between two parents.
    '''
    crossover_point = random.randint(1, len(mother) - 1)
    child = mother[:crossover_point] + father[crossover_point:]
    return tuple(child)


def mutate(individual):
    '''
    Mutate an individual by flipping one random bit.
    '''
    index_to_mutate = random.randint(0, len(individual) - 1)
    mutated = list(individual)
    mutated[index_to_mutate] = 1 - mutated[index_to_mutate]  # flip bit
    return tuple(mutated)


def random_selection(population, fitness_fn):
    '''
    Perform roulette-wheel (fitness-proportional) selection.
    Returns two individuals as mother and father.
    '''
    ordered_population = list(population)
    fitness_values = [fitness_fn(ind) for ind in ordered_population]
    total_fitness = sum(fitness_values)

    # Compute cumulative fitness
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

    return (select_one(), select_one())


def fitness_function(individual):
    '''
    Computes the decimal value of the 3-bit individual.
    '''
    return sum(bit * (2 ** idx) for idx, bit in enumerate(reversed(individual)))


def get_fittest_individual(iterable, func):
    return max(iterable, key=func)


def get_initial_population(n, count):
    '''
    Generate a set of random n-bit individuals.
    '''
    return set([
        tuple(random.randint(0, 1) for _ in range(n))
        for _ in range(count)
    ])


def main():
    minimal_fitness = 7

    # Starting with fixed initial population
    initial_population = {
        (1, 1, 0),
        (0, 0, 0),
        (0, 1, 0),
        (1, 0, 0)
    }

    # Or you can use a random initial population:
    # initial_population = get_initial_population(3, 4)

    fittest = genetic_algorithm(initial_population, fitness_function, minimal_fitness)
    print('Fittest Individual: ' + str(fittest))


if __name__ == '__main__':
    main()
