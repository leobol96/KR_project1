from solvers import solver
import common_functions as common


class DlisHeuristicSolver(solver.Solver):

    def __init__(self):
        return

    # The function gives the literal to use in the dpll_2 core.
    # The literal given depends from which version is chosen at the start.
    # Parameter 01: List of rules
    def get_literal(self, sudoku_rules):
        occurrences = [0] * 999 * 2
        for rule in sudoku_rules:
            for literal in rule:
                occurrences[self.choose_index(literal)] = occurrences[self.choose_index(literal)] + 1

        n_time = 0
        for idx, counter in enumerate(occurrences):
            if counter > n_time:
                to_return = self.decode_index(idx)
                n_time = counter

        return to_return

    def choose_index(self, value):
        if value[0] == '-':
            return (int(common.negate(value)) - 1) + 999
        else:
            return int(value) - 1

    def decode_index(self, idx):
        if idx > 998:
            return '-' + str(idx - 999 + 1)
        else:
            return str(idx + 1)
