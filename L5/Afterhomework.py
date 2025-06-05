def is_terminal(state):
    # Terminal if no pile can be split (i.e., all piles are <= 2 or cannot be split into unequal parts)
    for pile in state:
        if len(valid_splits(pile)) > 0:
            return False
    return True


def utility_of(state):
    # If it's terminal, the last player to move won. Since we assume MAX just moved, MIN wins: +1
    return +1  # MIN wins


def valid_splits(pile):
    # Returns all valid (a, b) such that a + b = pile, a ≠ b, and both > 0
    splits = []
    for i in range(1, pile):
        j = pile - i
        if i != j and j > 0:
            splits.append((min(i, j), max(i, j)))
    return splits


def successors_of(state):
    # Generate all successors from current state by splitting one pile
    successors = []
    for i, pile in enumerate(state):
        for split in valid_splits(pile):
            new_state = state[:i] + list(split) + state[i+1:]
            new_state.sort()
            successors.append(new_state)
    return successors


def minmax_decision(state):
    infinity = float('inf')

    def max_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = -infinity
        for s in successors_of(state):
            v = max(v, min_value(s))
        return v

    def min_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = infinity
        for s in successors_of(state):
            v = min(v, max_value(s))
        return v

    return argmax(successors_of(state), lambda s: min_value(s))


def alpha_beta_decision(state):
    infinity = float('inf')

    def max_value(state, alpha, beta):
        if is_terminal(state):
            return utility_of(state)
        v = -infinity
        for s in successors_of(state):
            v = max(v, min_value(s, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if is_terminal(state):
            return utility_of(state)
        v = infinity
        for s in successors_of(state):
            v = min(v, max_value(s, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    return argmax(successors_of(state), lambda s: min_value(s, -infinity, infinity))


def argmax(iterable, func):
    return max(iterable, key=func)


# --- Gameplay Loop ---

def user_select_pile(list_of_piles):
    print("\n    Current piles: {}".format(list_of_piles))

    i = -1
    while i < 0 or i >= len(list_of_piles) or list_of_piles[i] < 3:
        print("Which pile (from 1 to {}, must be > 2)?".format(len(list_of_piles)))
        i = int(input()) - 1

    print("Selected pile {}".format(list_of_piles[i]))

    max_split = list_of_piles[i] - 1

    j = 0
    while j < 1 or j > max_split or j == list_of_piles[i] - j:
        print("How much is the first split (must be non-equal, between 1 and {})?".format(max_split))
        j = int(input())

    k = list_of_piles[i] - j
    new_list_of_piles = list_of_piles[:i] + [j, k] + list_of_piles[i + 1:]
    new_list_of_piles.sort()
    print("    New piles: {}".format(new_list_of_piles))
    return new_list_of_piles


def main():
    state = [15]  # You can change this to 7 or 203

    while not is_terminal(state):
        # MIN (user)
        state = user_select_pile(state)
        if is_terminal(state):
            break

        # MAX (computer)
        print("\nMAX (Computer) is thinking...")
        # Uncomment one of the two:
        state = minmax_decision(state)         # Minimax
        # state = alpha_beta_decision(state)   # Alpha-Beta
        print("MAX moves to: {}".format(state))

    print("    Final state: {}".format(state))
    print("Game Over. MIN wins!")


if __name__ == '__main__':
    main()