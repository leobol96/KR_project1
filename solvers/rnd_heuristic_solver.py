import random
from solvers import solver


class RndHeuristiSolver(solver.Solver):

    def __init__(self):
        self.result = []
        self.backtrack_number = 0

    # The function gives the literal to use in the dpll_2 core.
    # The literal given depends from which version is chosen at the start.
    # Parameter 01: List of rules
    def get_literal(self, sudoku_rules, sudoku_numbers):
        return random.choice(random.choice(sudoku_rules))

    # The function returns the name of the algorithm
    def get_name(self):
        return 'Random heuristic'
