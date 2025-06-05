def minmax_decision(state):
    infinity = float('inf')

    def max_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = -infinity
        for (a, s) in successors_of(state):
            v = max(v, min_value(s))
        print('V: ' + str(v))
        return v

    def min_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = infinity
        for (a, s) in successors_of(state):
            v = min(v, max_value(s))
        return v

    action, state = argmax(successors_of(state), lambda a: min_value(a[1]))
    return action


def is_terminal(state):
    if state[0] == state[1] == state[2]:
        return True
    if state[3] == state[4] == state[5]:
        return True
    if state[6] == state[7] == state[8]:
        return True
    if state[0] == state[3] == state[6]:
        return True
    if state[1] == state[4] == state[7]:
        return True
    if state[2] == state[5] == state[8]:
        return True
    if state[0] == state[4] == state[8]:
        return True
    if state[2] == state[4] == state[6]:
        return True

    for position in state:
        if isinstance(position, int):
            return False
    return True


def utility_of(state):
    if state[0] == state[1] == state[2]:
        if state[0] == "X":
            return 1
        elif state[0] == "O":
            return -1
    if state[3] == state[4] == state[5]:
        if state[3] == "X":
            return 1
        elif state[3] == "O":
            return -1
    if state[6] == state[7] == state[8]:
        if state[6] == "X":
            return 1
        elif state[6] == "O":
            return -1
    if state[0] == state[3] == state[6]:
        if state[0] == "X":
            return 1
        elif state[0] == "O":
            return -1
    if state[1] == state[4] == state[7]:
        if state[1] == "X":
            return 1
        elif state[1] == "O":
            return -1
    if state[2] == state[5] == state[8]:
        if state[2] == "X":
            return 1
        elif state[2] == "O":
            return -1
    if state[0] == state[4] == state[8]:
        if state[4] == "X":
            return 1
        elif state[4] == "O":
            return -1
    if state[2] == state[4] == state[6]:
        if state[4] == "X":
            return 1
        elif state[4] == "O":
            return -1
    return 0


def successors_of(state):
    if state.count("X") > state.count("O"):
        turn = "O"
    else:
        turn = "X"

    l = []
    for i in range(len(state)):
        if isinstance(state[i], int):
            l2 = state.copy()
            l2[i] = turn
            l.append((i, l2))
    print(l)
    return l


def display(state):
    print("-----")
    for c in [0, 3, 6]:
        print(state[c + 0], state[c + 1], state[c + 2])


def main():
    board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    while not is_terminal(board):
        board[minmax_decision(board)] = 'X'
        if not is_terminal(board):
            display(board)
            board[int(input('Your move? '))] = 'O'
    display(board)


def argmax(iterable, func):
    return max(iterable, key=func)


if __name__ == '__main__':
    main()
