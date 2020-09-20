import numpy as np

from solvers import solver


class HumHeuristicSolver(solver.Solver):

    def __init__(self):
        self.result = []
        self.backtrack_number = 0

    # The function gives the literal to use in the dpll_2 core.
    # The literal given depends from which version is chosen at the start.
    # Parameter 01: List of rules
    def get_literal(self, sudoku_rules, sudoku_numbers):

        position_list = []
        best_point = 0
        best_position = ''

        # List with position
        for literal in sudoku_numbers:
            position_list.append(literal[0]+literal[1])

        # Matrix with points
        matrix = [[0 for col in range(9)] for row in range(9)]

        # +1 if there is a number in the col or in the row
        for k in range(9):
            for x in range(9):
                for literal in sudoku_numbers:
                    # row
                    if (str(x+1) == literal[1] or str(k+1) == literal[0]) and str(k+1)+str(x+1) not in position_list:
                        matrix[k][x] += 1

        # Chose the position with the maximum score
        for k in range(9):
            for x in range(9):
                if matrix[k][x] > best_point:
                    best_point = matrix[k][x]
                    best_position = str(k+1)+str(x+1)

        # return the literal
        for rule in sudoku_rules:
            for literal in rule:
                if literal[0]+literal[1] == best_position:
                    return literal

    # The function returns the name of the algorithm
    def get_name(self):
        return 'Hum Heuristic'


