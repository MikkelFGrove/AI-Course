import functools
import random
from pprint import pformat


def multiply_vector_elements(vector):
    """ return the multiplication of the vector elements """
    def mult(x, y):
        return x * y
    return functools.reduce(mult, vector, 1)


class Variable(object):
    """ Node in the network. Represents a random Variable. """

    def __init__(self, name, assignments, probability_table, parents=None, children=None):
        """
        params:
          name: string, name of this random variable
          assignments: tuple of possible values (e.g. ('false','true'))
          probability_table: dict mapping parent‐assignment‐tuples → tuple of probabilities
                             (ordered in the same order as `assignments`)
          parents: list of Variable objects (default empty list)
          children: list of Variable objects (default empty list)
        """
        self.name = name

        # build a mapping from assignment→index
        self.assignments = {}
        for i, a in enumerate(assignments):
            self.assignments[a] = i

        # verify probability_table rows match length of assignments
        for key, val in probability_table.items():
            if len(val) != len(assignments):
                raise ValueError(
                    f"Probability‐table for {name} has row of length {len(val)}, "
                    f"but {len(assignments)} possible assignments."
                )
        self.probability_table = probability_table

        # parents / children
        self.parents = [] if parents is None else parents[:]
        self.children = [] if children is None else children[:]

        # placeholder for marginal probabilities (will be a list of length len(assignments))
        self.marginal_probabilities = [0.0] * len(assignments)
        self.ready = False  # become True once marginal_probabilities is filled

    def get_name(self):
        return self.name

    def get_assignments(self):
        return self.assignments

    def get_assignment_index(self, assignment):
        return self.assignments[assignment]

    def get_probability(self, value, parents_values):
        """
        Return P(self = value | parents_values).  Here `parents_values` is
        a tuple/list of parent assignments, in the same order as self.parents.
        """
        return self.probability_table[tuple(parents_values)][ self.assignments[value] ]

    def get_conditional_probability(self, value, partial_parents_values):
        """
        Return P(self = value | parents = partial_parents_values), where
        partial_parents_values is a dict { parent_name: parent_value }.
        If not all parents are specified, this computes the appropriate
        marginal over the unspecified parents (using their marginals).
        """
        res = 0.0
        # first, figure out which parents are “given” versus need to be summed out
        given_pairs = []       # list of (parent_index, parent_value_string)
        marginal_indices = []  # list of parent_indices that we will sum over
        for i, parent in enumerate(self.parents):
            if parent.name in partial_parents_values:
                given_pairs.append((i, partial_parents_values[parent.name]))
            else:
                marginal_indices.append(i)

        # iterate over every row in self.probability_table
        for row_key, row_probs in self.probability_table.items():
            # row_key is a tuple of parent‐assignment‐strings (one for each parent),
            # row_probs is a tuple (P(self=‘false’|that row), P(self=‘true’|that row)) etc.
            valid = True
            for (p_idx, p_val) in given_pairs:
                if row_key[p_idx] != p_val:
                    valid = False
                    break
            if not valid:
                continue

            # multiply P(self=value | this complete parent‐row) by the marginals of any missing parents
            p_row = row_probs[self.assignments[value]]
            multiplier = 1.0
            for mi in marginal_indices:
                parent_node = self.parents[mi]
                parent_assignment_in_row = row_key[mi]
                multiplier *= parent_node.get_marginal_probability(parent_assignment_in_row)

            res += p_row * multiplier

        return res

    def calculate_marginal_probability(self):
        """
        Fill self.marginal_probabilities = [ P(self=assign_0), P(self=assign_1 ), … ].
        We assume Boolean (two assignments) throughout, but code works for n‐ary too.
        Parents should already have their marginals computed.
        """
        if self.ready:
            return

        # If no parents, there's exactly one row: key=() and value=(P(a0), P(a1), …).
        if not self.parents:
            # probability_table has exactly one entry: key=()
            only_row = next(iter(self.probability_table.values()))
            # copy it directly
            self.marginal_probabilities = list(only_row)
            self.ready = True
            return

        # if there are parents, sum over all parent‐assignments:
        # P(self = a_i) = sum_{all parent‐rows r} [ P(self=a_i | parents=r) * Π_j P(parent_j = r[j]) ]
        num_assignments = len(self.assignments)
        marginals = [0.0] * num_assignments

        for parent_row, child_probs in self.probability_table.items():
            # parent_row is a tuple of strings, child_probs is a tuple of length num_assignments
            # First compute P(parents = that exact row) = Π_j P(parent_j = parent_row[j])
            p_parents = 1.0
            for j, parent_node in enumerate(self.parents):
                p_parents *= parent_node.get_marginal_probability(parent_row[j])

            # now distribute that weight into each child assignment
            for i in range(num_assignments):
                marginals[i] += child_probs[i] * p_parents

        self.marginal_probabilities = marginals
        self.ready = True

    def get_marginal_probability(self, val):
        return self.marginal_probabilities[self.assignments[val]]

    def add_child(self, node):
        self.children.append(node)

    def add_parent(self, node):
        self.parents.append(node)

    def get_children(self):
        return self.children

    def is_child_of(self, node):
        """
        Return True if `node` is one of our parents.
        """
        return any(parent.name == node.name for parent in self.parents)


class BayesianNetwork(object):
    """ Simple Bayesian Network class for exact inference on small graphs. """

    def __init__(self):
        self.variables = []
        self.varsMap = {}  # name → Variable object
        self.ready = False

    def calculate_marginal_probabilities(self):
        """
        Iterate over self.variables in order, calling calculate_marginal_probability()
        on each.  We assume that `self.variables` is topologically sorted so that
        parents come before children.
        """
        for var in self.variables:
            var.calculate_marginal_probability()
        self.ready = True

    def get_variables(self):
        return self.variables

    def get_variable(self, varName):
        return self.varsMap[varName]

    def add_variable(self, var, index=-1):
        if index < 0:
            self.variables.append(var)
        else:
            self.variables.insert(index, var)
        self.varsMap[var.name] = var
        self.ready = False

    def set_variables(self, varList):
        """
        Quickly set the list of nodes.  They must already be topologically sorted!
        """
        self.variables = varList[:]
        self.varsMap = {var.name: var for var in varList}
        self.ready = False

    def sub_vals(self, var, values):
        """
        Helper: for a Variable `var`, and a full assignment‐dict `values` (var_name→value),
        return the tuple of that variable's parents' values, in the same order as var.parents.
        """
        return tuple(values[p.name] for p in var.parents)

    def get_joint_probability(self, values):
        """
        Given a full assignment `values` (dict var_name → 'true'/'false'), return
        P(values) = Π_{X in network} P(X = values[X] | parents(X) = values_of_parents).
        """
        joint = 1.0
        for var_name, val in values.items():
            var = self.varsMap[var_name]
            parent_tuple = self.sub_vals(var, values)
            p = var.get_probability(val, parent_tuple)
            joint *= p
        return joint

    def get_conditional_probability(self, query_vars, evidence_vars):
        """
        If `query_vars` are children of `evidence_vars`, compute
           P(query_vars | evidence_vars)
        by assuming independence among query nodes given their parents.

        Otherwise, assume query_vars are parents and evidence_vars are children,
        and apply Bayes’ Rule (limited to one level).
        This is the same structure as in your original code.
        """
        # check if we are doing P(children | parents)
        # i.e. each variable in query_vars is a child of every variable in evidence_vars
        first_q = next(iter(query_vars))
        is_child_check = all(
            self.varsMap[first_q].is_child_of(self.varsMap[e])
            for e in evidence_vars
        )
        if is_child_check:
            # P(Q | E) = ∏ P(q_i | parents_of_q_i = evidence_vars)
            result = 1.0
            for q_name, q_val in query_vars.items():
                var_q = self.varsMap[q_name]
                result *= var_q.get_conditional_probability(q_val, evidence_vars)
            return result

        # else assume P(parents | children) via Bayes
        # Here we only handle the “one‐level” case, same as before.
        # Let A = query_vars (parents), B = evidence_vars (children).
        # P(A|B) = P(B|A) P(A) / [ P(B|A) P(A) + P(B|¬A) P(¬A) ]  (if only one parent in A)
        # If multiple parents, we assume independent within that level, etc.
        # We will do exactly what your prior code did:
        #    1) joint_marginal_parents = Π P(A_i)
        #    2) joint_marginal_children = Π P(B_j)
        #    3) joint_conditional_children = Π P(B_j | A)
        #    4) marginal_of_evidents = Π P(B_j | A with one bit flipped)  [this is odd but matches your code]
        # Then use Bayes denominator.

        # first compute Π P(parent = value)
        joint_marginal_parents = 1.0
        for a_name, a_val in query_vars.items():
            joint_marginal_parents *= self.varsMap[a_name].get_marginal_probability(a_val)

        joint_marginal_children = 1.0
        joint_conditional_children = 1.0
        marginal_of_evidents = 1.0

        # choose the first parent to flip when computing the “complementary” assignment
        first_parent_name = next(iter(query_vars))

        for child_name, child_val in evidence_vars.items():
            child_node = self.varsMap[child_name]

            # multiply Π P(child = child_val)  (marginal of each child)
            joint_marginal_children *= child_node.get_marginal_probability(child_val)

            # multiply Π P(child = child_val | all parents = query_vars)
            joint_conditional_children *= child_node.get_conditional_probability(child_val, query_vars)

            # build complementary assignment: flip the first parent in query_vars
            complement_assignment = query_vars.copy()
            orig = complement_assignment[first_parent_name]
            complement_assignment[first_parent_name] = (
                'false' if orig == 'true' else 'true'
            )
            # multiply P(child = child_val | parents = complement_assignment)
            marginal_of_evidents *= child_node.get_conditional_probability(child_val, complement_assignment)

        numerator = joint_conditional_children * joint_marginal_parents
        denominator = numerator + marginal_of_evidents * (1.0 - joint_marginal_parents)
        return numerator / denominator

    def get_marginal_probability(self, var, val):
        return var.get_marginal_probability(val)


def create_random_sample(network):
    """
    Draw one sample from the full joint by ancestral sampling.
    Assumes Boolean variables in assignment order ('false','true').
    """
    sample = {}
    for var in network.variables:
        r = random.random()
        # assignment1 = the first key in var.assignments (which is 'false')
        assignment1 = list(var.assignments.keys())[0]
        assignment2 = list(var.assignments.keys())[1]
        parent_tuple = network.sub_vals(var, sample)
        p_false = var.get_probability(assignment1, parent_tuple)  # P(var='false' | parents=…)
        # if r <= P('false'), then we pick 'false'; else 'true'
        if r <= p_false:
            sample[var.name] = assignment1
        else:
            sample[var.name] = assignment2
    return sample


def pad(string, pad=4):
    lines = string.split('\n')
    padded_lines = [(' ' * pad) + line for line in lines]
    return '\n'.join(padded_lines)


def print_conditional_probability(network, conditionals_vars, conditionals_evidents):
    print('Given')
    print(pad(pformat(conditionals_evidents)))
    print('conditional probability of')
    print(pad(pformat(conditionals_vars)))
    print("is {:f}".format(
        network.get_conditional_probability(
            conditionals_vars,
            conditionals_evidents
        )
    ))


def print_joint_probability(network, values):
    print('Joint probability of')
    print(pad(pformat(values)))
    print("is {:f}".format(network.get_joint_probability(values)))


def print_marginal_probabilities(network):
    print("Marginal probabilities:")
    for variable in network.get_variables():
        print("    {}".format(variable.get_name()))
        for assignment in variable.get_assignments().keys():
            print("        {}: {:f}".format(
                assignment,
                variable.get_marginal_probability(assignment))
            )


def car_network():
    t_DT = {
        (): (0.7, 0.3)
    }
    DT = Variable('DT', ('false', 'true'), t_DT)


    t_EM = {
        (): (0.7, 0.3)
    }
    EM = Variable('EM', ('false', 'true'), t_EM)

    t_FTL = {
        (): (0.8, 0.2)
    }
    FTL = Variable('FTL', ('false', 'true'), t_FTL)


    t_SMS = {
        # in the order (DT, EM)
        ('true',  'true'):  (0.95, 0.05),
        ('true',  'false'): (0.40, 0.60),
        ('false', 'true'):  (0.70, 0.30),
        ('false', 'false'): (0.30, 0.70)
    }
    SMS = Variable('SMS', ('false', 'true'), t_SMS, parents=[DT, EM])

    t_V = {
        ('true',):  (0.30, 0.70),
        ('false',):(0.90, 0.10)
    }
    V = Variable('V', ('false', 'true'), t_V, parents=[DT])

    t_HC = {
        ('true',  'true',  'true'):   (0.10, 0.90),
        ('true',  'true',  'false'):  (0.20, 0.80),
        ('true',  'false', 'true'):   (0.70, 0.30),
        ('true',  'false', 'false'):  (0.80, 0.20),
        ('false', 'true',  'true'):   (0.40, 0.60),
        ('false', 'true',  'false'):  (0.50, 0.50),
        ('false', 'false', 'true'):   (0.90, 0.10),
        ('false', 'false', 'false'):  (0.99, 0.01)
    }
    HC = Variable('HC', ('false', 'true'), t_HC, parents=[DT, FTL, EM])

    # (Optionally—if you want to maintain child links)
    DT.children.extend([SMS, V, HC])
    EM.children.extend([SMS, HC])
    FTL.children.append(HC)

    # Build network in topological order:
    variables = [DT, EM, FTL, SMS, V, HC]
    network = BayesianNetwork()
    network.set_variables(variables)

    # Pre‐compute all marginals:
    network.calculate_marginal_probabilities()

    # Print marginals:
    print_marginal_probabilities(network)
    print()

    # Example #1: Joint probability
    joint_values = {
        'DT': 'true',
        'EM': 'false',
        'FTL': 'true',
        'SMS': 'true',
        'V': 'false',
        'HC': 'true'
    }
    print_joint_probability(network, joint_values)
    print()

    # Example #2: Conditional probability P(HC = true | DT = true, EM = false, FTL = true)
    conditionals_vars = {'HC': 'true'}
    conditionals_evidents = {
        'DT': 'true',
        'EM': 'false',
        'FTL': 'true'
    }
    print_conditional_probability(network, conditionals_vars, conditionals_evidents)
    print()


    # Pre‐compute marginals
    network.calculate_marginal_probabilities()
    print_conditional_probability(
        network,
        conditionals_vars    = {'FTL': 'true'},
        conditionals_evidents = {'HC': 'true'}
    )

    # Example #3: Generate one random sample and show its joint probability
    sample = create_random_sample(network)
    print("Random sample drawn (ancestral sampling):")
    print(pformat(sample))
    print_joint_probability(network, sample)
    print()


if __name__ == '__main__':
    car_network()
