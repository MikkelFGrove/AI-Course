class Node:
    def __init__(self, state, parent=None, depth=0):
        self.STATE = state
        self.PARENT_NODE = parent
        self.DEPTH = depth

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
        return f'State: {self.STATE} - Depth: {self.DEPTH}'


def INSERT(node, queue):
    queue.append(node)  # BFS: insert at end (FIFO)
    return queue

def INSERT_ALL(nodes, queue):
    for node in nodes:
        queue = INSERT(node, queue)
    return queue

def REMOVE_FIRST(queue):
    return queue.pop(0)

def EXPAND(node):
    successors = []
    children = successor_fn(node.STATE)
    for child in children:
        s = Node(child, node, node.DEPTH + 1)
        successors.append(s)
    return successors

def successor_fn(state):
    return STATE_SPACE.get(state, [])

def TREE_SEARCH():
    fringe = []
    initial_node = Node(INITIAL_STATE)
    fringe = INSERT(initial_node, fringe)
    visited = set()

    while fringe:
        node = REMOVE_FIRST(fringe)
        if node.STATE in visited:
            continue
        visited.add(node.STATE)

        if node.STATE[1] == 'Clean' and node.STATE[2] == 'Clean':
            return node.path()

        children = EXPAND(node)
        fringe = INSERT_ALL(children, fringe)
        print("Fringe:", [n.STATE for n in fringe])

    return None


# Define the initial state
INITIAL_STATE = ('A', 'Dirty', 'Dirty')

# Generate the state space manually
STATE_SPACE = {
    ('A', 'Dirty', 'Dirty'): [('A', 'Clean', 'Dirty'), ('B', 'Dirty', 'Dirty')],
    ('A', 'Clean', 'Dirty'): [('B', 'Clean', 'Dirty')],
    ('B', 'Clean', 'Dirty'): [('B', 'Clean', 'Clean'), ('A', 'Clean', 'Dirty')],
    ('B', 'Clean', 'Clean'): [('A', 'Clean', 'Clean')],
    ('B', 'Dirty', 'Dirty'): [('B', 'Dirty', 'Clean'), ('A', 'Dirty', 'Dirty')],
    ('B', 'Dirty', 'Clean'): [('B', 'Clean', 'Clean'), ('A', 'Dirty', 'Clean')],
    ('A', 'Dirty', 'Clean'): [('A', 'Clean', 'Clean'), ('B', 'Dirty', 'Clean')],
    ('A', 'Clean', 'Clean'): [('B', 'Clean', 'Clean')],
}

def run():
    path = TREE_SEARCH()
    if path:
        print('\nSolution path:')
        for node in path:
            node.display()
    else:
        print("No solution found.")

if __name__ == '__main__':
    run()