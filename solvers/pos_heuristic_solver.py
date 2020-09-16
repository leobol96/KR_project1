from solvers import solver


class PosHeuristicSolver(solver.Solver):

    def __init__(self):
        self.result = []
        self.backtrack_number = 0

    # The function gives the literal to use in the dpll_2 core.
    # The literal given depends from which version is chosen at the start.
    # Parameter 01: List of rules
    def get_literal(self, sudoku_rules):
        for x in range(2, 10):
            for rule in sudoku_rules:
                if rule[0][0] != '-' and len(rule) == x:
                    return rule[0]

