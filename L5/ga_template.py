import random


p_mutation = 0.2
num_of_generations = 30


def genetic_algorithm(population, fitness_fn, minimal_fitness):
    for generation in range(num_of_generations):
        print("Generation {}:".format(generation))
        print_population(population, fitness_fn)

        new_population = set()

        for i in range(len(population)):
            mother, father = random_selection(population, fitness_fn)
            child = reproduce(mother, father)

            if random.uniform(0, 1) < p_mutation:
                child = mutate(child)

            new_population.add(child)

        # Add new population to population, use union to disregard
        # duplicate individuals
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
    Reproduce two individuals with single-point crossover
    Return the child individual
    '''


    r = random.randint(0, 1)
    if r == 0:
        child = [mother[0], father[1], father[2]]
    else:
        child = [mother[0], mother[1], father[2]]

    r1 = random.uniform(0, 1)

    if r1 <= 1:
        return mutate(child)
    return child


def mutate(individual):
    '''
    Mutate an individual by randomly assigning one of its bits
    Return the mutated individual
    '''
    r = random.randint(0, 2)
    l = []
    for i in range(len(individual)):
        if r == i:
            if individual[i] == 0:
                l.append(1)
            else:
                l.append(0)
        else:
            l.append(individual[i])

    return tuple(l)


def random_selection(population, fitness_fn):
    """
    Compute fitness of each in population according to fitness_fn and add up
    the total. Then choose 2 from sequence based on percentage contribution to
    total fitness of population
    Return selected variable which holds two individuals that were chosen as
    the mother and the father
    """

    # Python sets are randomly ordered. Since we traverse the set twice, we
    # want to do it in the same order. So let's convert it temporarily to a
    # list.
    ordered_population = list(population)
    total_fitness = sum(fitness_fn(individual) for individual in ordered_population)
    fitness = list()
    parents = list()

    for individual in ordered_population:
        if ordered_population.index(individual) <= 0:
            fitness.append(fitness_fn(individual))
        else:
            fitness.append(fitness_fn(individual) + fitness[ordered_population.index(individual) - 1])


    r = random.randint(0, total_fitness)



    for fit in fitness:
        if fit >= r:
            parents.append(ordered_population[fitness.index(fit)])
            break

    r = random.randint(0, total_fitness)

    for fit in fitness:
        if fit >= r:
            parents.append(ordered_population[fitness.index(fit)])
            break

    return parents


def fitness_function(individual):
    '''
    Computes the decimal value of the individual
    Return the fitness level of the individual

    Explanation:
    enumerate(list) returns a list of pairs (position, element):

    enumerate((4, 6, 2, 8)) -> [(0, 4), (1, 6), (2, 2), (3, 8)]

    enumerate(reversed((1, 1, 0))) -> [(0, 0), (1, 1), (2, 1)]
    '''

    num = 0
    for two, bit in enumerate(individual[::-1]):
        num += bit * 2 ** two

    return num

    #return fitness


def get_fittest_individual(iterable, func):
    return max(iterable, key=func)


def get_initial_population(n, count):
    '''
    Randomly generate count individuals of length n
    Note since its a set it disregards duplicate elements.
    '''
    return set([
        tuple(random.randint(0, 1) for _ in range(n))
        for _ in range(count)
    ])


def main():
    minimal_fitness = 7

    # Curly brackets also creates a set, if there isn't a colon to indicate a dictionary
    initial_population = {
        (1, 1, 0),
        (0, 0, 0),
        (0, 1, 0),
        (1, 0, 0)
    }
    # initial_population = get_initial_population(3, 4)

    fittest = genetic_algorithm(initial_population, fitness_function, minimal_fitness)
    print('Fittest Individual: ' + str(fittest))


if __name__ == '__main__':
    pass
    main()
