import random

# Define environment with all locations Dirty
Environment = {
    'A': 'Dirty',
    'B': 'Dirty',
    'C': 'Dirty',
    'D': 'Dirty',
    'Current': random.choice(['A', 'B', 'C', 'D'])  # Random starting square
}

# Define possible movements from each location
MOVES = {
    'A': {'Left': 'B', 'Down': 'C'},
    'B': {'Right': 'A', 'Down': 'D'},
    'C': {'Up': 'A', 'Right': 'D'},
    'D': {'Up': 'B', 'Left': 'C'}
}


# Agent logic
def REFLEX_VACUUM_AGENT(loc_st):
    location, status = loc_st
    if status == 'Dirty':
        return 'Suck'

    # If clean, choose a random valid move from this location
    possible_moves = list(MOVES[location].keys())
    return random.choice(possible_moves)


# Sense current state
def Sensors():
    location = Environment['Current']
    return (location, Environment[location])


# Apply action to environment
def Actuators(action):
    location = Environment['Current']
    if action == 'Suck':
        Environment[location] = 'Clean'
    elif action in MOVES[location]:
        Environment['Current'] = MOVES[location][action]


# Run simulation
def run(n):
    print('    Current                        New')
    print('location    status  action  location    status')
    for i in range(1, n + 1):
        (location, status) = Sensors()
        print("{:12s}{:8s}".format(location, status), end='')
        action = REFLEX_VACUUM_AGENT((location, status))
        Actuators(action)
        (new_location, new_status) = Sensors()
        print("{:8s}{:12s}{:8s}".format(action, new_location, new_status))


if __name__ == '__main__':
    run(20)