import random

A, B, C, D = 'A', 'B', 'C', 'D'

state = {}
action = None
model = {A: None, B: None, C: None, D: None}  # Internal map

# Map of possible moves from each square
MOVES = {
    A: {'Right': B, 'Down': C},
    B: {'Left': A, 'Down': D},
    C: {'Up': A, 'Right': D},
    D: {'Left': C, 'Up': B}
}

# Environment initialized randomly
Environment = {
    A: 'Dirty',
    B: 'Dirty',
    C: 'Dirty',
    D: 'Dirty',
    'Current': random.choice([A, B, C, D])
}

def INTERPRET_INPUT(percept):
    return percept

def RULE_MATCH(state):
    location, status = state
    if all(model[loc] == 'Clean' for loc in [A, B, C, D]):
        return 'NoOp'
    if status == 'Dirty':
        return 'Suck'

    # Pick a direction toward an unknown or dirty neighbor
    for direction, neighbor in MOVES[location].items():
        if model[neighbor] != 'Clean':
            return direction

    # No known dirty neighbors; pick any valid move randomly
    return random.choice(list(MOVES[location].keys()))

def UPDATE_STATE(state, action, percept):
    location, status = percept
    model[location] = status
    return percept

def REFLEX_AGENT_WITH_STATE(percept):
    global state, action
    state = UPDATE_STATE(state, action, percept)
    action = RULE_MATCH(state)
    return action

def Sensors():
    location = Environment['Current']
    return (location, Environment[location])

def Actuators(action):
    location = Environment['Current']
    if action == 'Suck':
        Environment[location] = 'Clean'
    elif action in MOVES[location]:
        Environment['Current'] = MOVES[location][action]

def run(n):
    print('    Current                        New')
    print('location    status  action  location    status')
    for i in range(1, n + 1):
        (location, status) = Sensors()
        print("{:12s}{:8s}".format(location, status), end='')
        action = REFLEX_AGENT_WITH_STATE((location, status))
        Actuators(action)
        (new_location, new_status) = Sensors()
        print("{:8s}{:12s}{:8s}".format(action, new_location, new_status))
        if action == 'NoOp':
            break

if __name__ == '__main__':
    run(20)