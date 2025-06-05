import queue

class Node:  # Node has only PARENT_NODE, STATE, DEPTH
    def __init__(self, state, parent=None, depth=0, heuristic=0, edge=0):
        self.STATE = state
        self.PARENT_NODE = parent
        self.DEPTH = depth
        self.HEURISTIC = heuristic
        self.EDGE = edge

    def path(self):  # Create a list of nodes from the root to this node.
        current_node = self
        path = [self]
        while current_node.PARENT_NODE:  # while current node has parent
            current_node = current_node.PARENT_NODE  # make parent the current node
            path.append(current_node)   # add current node to path
        return path

    def display(self):
        print(self)

    def __repr__(self):
        return 'State: ' + str(self.STATE) + ' - Depth: ' + str(self.DEPTH)

    def __lt__(self, other):
        return self.HEURISTIC < other.HEURISTIC

'''
Search the tree for the goal state and return path from initial state to goal state
'''
algorithmChoice = 1

def TREE_SEARCH():
    fringe = queue.PriorityQueue()
    initial_node = Node(INITIAL_STATE)
    fringe = INSERT_GREEDY(initial_node, fringe)
    while fringe is not None:
        node = REMOVE_FIRST_GREEDY(fringe)
        if GOAL_STATE.__contains__(node.STATE):
            return node.path()
        children = EXPAND(node)
        fringe = INSERT_ALL_GREEDY(children, fringe)
        print("fringe: {}".format(list(fringe.queue)))


'''
Expands node and gets the successors (children) of that node.
Return list of the successor nodes.
'''
def EXPAND(node: Node):
    successors = []
    children = successor_fn(node.STATE)
    for child in children:
        s = Node(node)  # create node for each in state list
        s.STATE = child[0]  # e.g. result = 'F' then 'G' from list ['F', 'G']
        s.PARENT_NODE = node
        s.HEURISTIC = HEURISTICS_DICT[s.STATE]
        s.EDGE = child[1] + node.EDGE
        s.DEPTH = node.DEPTH + 1
        successors = INSERT(s, successors)
    return successors


'''
Insert node in to the queue (fringe).
'''
def INSERT(node, queue):
    queue.append(node)
    return queue

def INSERT_GREEDY(node, queue: queue.PriorityQueue):
    cost = CALCULATE_GREEDY_COST(node)
    queue.put((cost, node))
    return queue

def CALCULATE_GREEDY_COST(node):
    if algorithmChoice == 1:
        return HEURISTICS_DICT[node.STATE]
    else:
        return HEURISTICS_DICT[node.STATE] + node.EDGE



def CALCULATE_A_COST(node):
    return HEURISTICS_DICT[node.STATE] + node[1]


'''
Insert list of nodes into the fringe
'''

def INSERT_ALL(list, queue):
    for i in list:
        queue.append(i)
    return queue

'''
Insert list of nodes into the fringe using greedy cost function
'''
def INSERT_ALL_GREEDY(list, queue: queue.PriorityQueue):
    for i in list:
        cost = CALCULATE_GREEDY_COST(i)
        queue.put((cost, i))
    return queue


'''
Removes and returns the first element from fringe
'''
def REMOVE_FIRST(queue):
    return queue.pop(len(queue) - 1)


def REMOVE_FIRST_GREEDY(queue: queue.PriorityQueue):
    item = queue.get()
    return item[1]
'''
Successor function, mapping the nodes to its successors
'''
def successor_fn(state):  # Lookup list of successor states
    return STATE_SPACE[state]  # successor_fn( 'C' ) returns ['F', 'G']


INITIAL_STATE = 'A'
GOAL_STATE = ['L', 'K']
STATE_SPACE = {'A': [['B', 1], ['C', 2], ['D', 4]],
               'B': [['E', 4], ['F', 5]],
               'F': [['G', 1]],
               'E': [['G', 2], ['H', 3]],
               'G': [['K', 6]],
               'H': [['K', 6], ['L', 5]],
               'C': [['E', 4]],
               'D': [['I', 4], ['H', 1], ['J', 2]],
               'I': [['L', 3]],
               'J': [],
               'K': [],
               'L': []
               }

HEURISTICS_DICT = {
    'A': 6,
    'B': 5,
    'C': 5,
    'D': 2,
    'E': 4,
    'F': 5,
    'G': 4,
    'H': 1,
    'J': 1,
    'I': 2,
    'L': 0,
    'K': 0
}


'''
Run tree search and display the nodes in the path to goal node
'''
def run():
    path = TREE_SEARCH()
    print('Solution path:')
    for node in path:
        node.display()


if __name__ == '__main__':
    run()
