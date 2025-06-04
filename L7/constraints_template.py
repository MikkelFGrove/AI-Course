from random import shuffle


class CSP:
    def __init__(self, variables, domains, neighbours, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbours = neighbours
        self.constraints = constraints

    def backtracking_search(self):
        return self.recursive_backtracking({})

    def recursive_backtracking(self, assignment):
        if (self.is_complete(assignment)):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.recursive_backtracking(assignment)
                if result is not None:
                    return result
                assignment.pop(var)
        return var



    def select_unassigned_variable(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return variable

    def is_complete(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return False
        return True

    def order_domain_values(self, variable, assignment):
        all_values = self.domains[variable][:]
        # shuffle(all_values)
        return all_values

    def is_consistent(self, variable, value, assignment):
        if not assignment:
            return True

        for constraint in self.constraints.values():
            for neighbour in self.neighbours[variable]:
                if neighbour not in assignment:
                    continue

                neighbour_value = assignment[neighbour]
                if not constraint(variable, value, neighbour, neighbour_value):
                    return False
        return True


def create_australia_csp():
    cr, pa, co, ve, gu, su, gf, ec, pe, br, bo, pg, ur, ar, ch = 'CR', 'PA', 'CO', 'VE', 'GU', 'SU', 'GF', 'EC', 'PE', 'BR', 'BO', 'PG', 'UR', 'AR', 'CH'
    #wa, q, t, v, sa, nt, nsw = 'WA', 'Q', 'T', 'V', 'SA', 'NT', 'NSW'
    values = ['Red', 'Green', 'Blue', 'Yellow']
    #values = ['Red', 'Green', 'Blue']
    variables = [cr, pa, co, ve, gu, su, gf, ec, pe, br, bo, pg, ur, ar, ch]
    #variables = [wa, q, t, v, sa, nt, nsw]
    domains = {}
    for variable in variables:
        domains[variable] = values[:]

    #domains = {
    #    wa: values[:],
    #    q: values[:],
    #    t: values[:],
    #    v: values[:],
    #    sa: values[:],
    #    nt: values[:],
    #    nsw: values[:],
    #}

    neighbours = {
        cr: [pa],
        pa: [co, cr],
        co: [cr, ve, ec, pe, br],
        ve: [co, gu, br],
        gu: [ve, su, br,],
        su: [gu, gf, br],
        gf: [su, br],
        ec: [co, pe],
        pe: [br, ec, co, bo, ch],
        br: [co, ve, gu, su, gf, pe, br, bo, pg, ur, ar],
        bo: [br, pe, pg, ar, ch],
        pg: [br, bo, ar],
        ur: [br, ar],
        ar: [ur, br, pg, ch, bo],
        ch: [ar, bo, pe],
    }

    def constraint_function(first_variable, first_value, second_variable, second_value):
        return first_value != second_value

    constraints = {
        cr: constraint_function,
        pa: constraint_function,
        co: constraint_function,
        ve: constraint_function,
        gu: constraint_function,
        su: constraint_function,
        gf: constraint_function,
        ec: constraint_function,
        pe: constraint_function,
        br: constraint_function,
        bo: constraint_function,
        pg: constraint_function,
        ur: constraint_function,
        ar: constraint_function,
        ch: constraint_function,
    }
    #constraints = {
    #    wa: constraint_function,
    #    q: constraint_function,
    #    t: constraint_function,
    #    v: constraint_function,
    #    sa: constraint_function,
    #    nt: constraint_function,
    #    nsw: constraint_function,
    #}

    return CSP(variables, domains, neighbours, constraints)


if __name__ == '__main__':
    australia = create_australia_csp()
    result = australia.backtracking_search()
    for area, color in sorted(result.items()):
        print("{}: {}".format(area, color))

    # Check at https://mapchart.net/australia.html
