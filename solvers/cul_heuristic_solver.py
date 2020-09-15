from solvers import solver


class CulHeuristicSolver(solver.Solver):

    def __init__(self):
        self.result = []
        self.backtrack_number = 0

    # The function gives the literal to use in the dpll_2 core.
    # The literal given depends from which version is chosen at the start.
    # Parameter 01: List of rules
    def get_literal(self, sudoku_rules):
        idx_len_clauses = 2
        while True:
            for rule in sudoku_rules:
                if len(rule) == idx_len_clauses:
                    return rule[0]
            idx_len_clauses += 1
