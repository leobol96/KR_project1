from solvers import solver


class HumHeuristicSolver(solver.Solver):
    """
    The HumHeuristicSolver extends the class solver. All the methods are inherited.
    The HUM heuristic aims at changing the split phase of the general dpll algorithm,
    for this purpose it overwrites the get_lieral method.

    See the documentation of the get_literal method to have more information about the split phase

    """

    def __init__(self):
        self.result = []
        self.backtrack_number = 0

    def get_literal(self, sudoku_rules, sudoku_numbers):
        """
        The method gives the literal to use in the dpll core. The aim of the HUM heuristic is to chose a literal in
        same way a HUMan would do it. For this reason, a matrix is created. All empty sudoku
        positions have a score. The more numbers there are in the same column or in the same row of the empty cell
        the higher the score will be. The literal chosen from this heuristic will be the one in the matrix with the
        highest score.

        4x4 example:

        Sudoku numbers
            1 * * *
            1 * * *
            * * * 1
            * * * *

        Matrix with score
            * 1 1 2
            * 1 1 2
            3 1 1 *
            2 0 0 1

        Args:
            sudoku_rules: List of rules
            sudoku_numbers: List of numbers already present in the sudoku solution

        Returns:
            The literal to use in the dpll core

        """

        position_list = []
        best_point = 0
        best_position = ''

        # List with position
        for literal in sudoku_numbers:
            position_list.append(literal[0] + literal[1])

        # Matrix with points
        matrix = [[0 for col in range(9)] for row in range(9)]

        # +1 if there is a number in the col or in the row
        for k in range(9):
            for x in range(9):
                for literal in sudoku_numbers:
                    # row
                    if (str(x + 1) == literal[1] or str(k + 1) == literal[0]) and str(k + 1) + str(
                            x + 1) not in position_list:
                        matrix[k][x] += 1

        # Chose the position with the maximum score
        for k in range(9):
            for x in range(9):
                if matrix[k][x] > best_point:
                    best_point = matrix[k][x]
                    best_position = str(k + 1) + str(x + 1)

        # return the literal
        for rule in sudoku_rules:
            for literal in rule:
                if literal[0] + literal[1] == best_position:
                    return literal

    def get_name(self):
        """
        The method returns the name of the heuristic.

        Returns:
            Name of the heuristic

        """
        return 'Hum'
