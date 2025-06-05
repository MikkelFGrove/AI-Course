import heapq
import itertools

class Node:
    def __init__(self, state, parent=None, depth=0, cost=0, heuristic=0):
        self.STATE = state
        self.PARENT_NODE = parent
        self.DEPTH = depth
        self.COST = cost
        self.HEURISTIC = heuristic
        self.TOTAL_COST = cost + heuristic

    def path(self):
        current_node = self
        path = [self]
        while current_node.PARENT_NODE:
            current_node = current_node.PARENT_NODE
            path.append(current_node)
        return list(reversed(path))

    def display(self):
        print(self)

    def __repr__(self):
        return f"State: {self.STATE} - Depth: {self.DEPTH} - Cost: {self.COST} - Heuristic: {self.HEURISTIC}"

# New heuristic values
HEURISTIC_VALUES = {
    'A': 6, 'B': 5, 'C': 5, 'D': 2, 'E': 4, 'F': 5,
    'G': 4, 'H': 1, 'I': 2, 'J': 1, 'K': 0, 'L': 0
}

# New weighted edges
STATE_SPACE = {
    'A': [('B', 1), ('C', 2), ('D', 4)],
    'B': [('F', 5), ('E', 4)],
    'C': [('E', 1)],
    'D': [('H', 1), ('I', 4), ('J', 2)],
    'E': [('G', 2), ('H', 3)],
    'F': [('G', 1)],
    'G': [('K', 6)],
    'H': [('K', 6), ('L', 5)],
    'I': [('L', 3)],
    'J': [],
    'K': [],
    'L': []
}

GOAL_STATES = {'K', 'L'}  # Set of goal states
INITIAL_STATE = 'A'

def heuristic(state):
    return HEURISTIC_VALUES.get(state, 99)

def path_cost(from_node, to_state):
    for (neighbor, cost) in STATE_SPACE[from_node.STATE]:
        if neighbor == to_state:
            return from_node.COST + cost
    return from_node.COST + 9999  # fallback large cost if not found

def successor_fn(state):
    return STATE_SPACE[state]  # now returns list of (child, cost)

def PRIORITY_TREE_SEARCH(weight=1.0, use_astar=True):
    fringe = []
    counter = itertools.count()
    h = heuristic(INITIAL_STATE)
    initial_node = Node(INITIAL_STATE, cost=0, heuristic=h)
    priority = initial_node.COST + weight * h if use_astar else h
    heapq.heappush(fringe, (priority, next(counter), initial_node))

    while fringe:
        _, _, node = heapq.heappop(fringe)
        if node.STATE in GOAL_STATES:
            return node.path()

        for (child_state, edge_cost) in successor_fn(node.STATE):
            new_cost = node.COST + edge_cost
            h = heuristic(child_state)
            total = new_cost + weight * h if use_astar else h
            child_node = Node(child_state, node, node.DEPTH + 1, new_cost, h)
            heapq.heappush(fringe, (total, next(counter), child_node))

    return None

def run_search(strategy_name, weight=1.0, use_astar=True):
    print(f"\n=== {strategy_name} ===")
    path = PRIORITY_TREE_SEARCH(weight=weight, use_astar=use_astar)
    if path:
        for node in path:
            node.display()
        print("Final path:", ' -> '.join(n.STATE for n in path))
    else:
        print("No path found.")

def run():
    run_search("Greedy Best-First Search", use_astar=False)
    run_search("A* Search", weight=1.0, use_astar=True)
    run_search("Weighted A* Search (w=2)", weight=2.0, use_astar=True)

if __name__ == '__main__':
    run()