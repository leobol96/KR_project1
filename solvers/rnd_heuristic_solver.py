import random
from solvers import solver


class RndHeuristiSolver(solver.Solver):
    """
    The RndHeuristiSolver extends the class solver. All the methods are inherited.
    The RND heuristic aims at changing the split phase of the general dpll algorithm,
    for this purpose it overwrites the get_lieral method.

    See the documentation of the get_literal method to have more information about the split phase

    """

    def __init__(self):
        self.result = []
        self.backtrack_number = 0

    def get_literal(self, sudoku_rules, sudoku_numbers):
        """
        The method gives the literal to use in the dpll core. The aim of the RND heuristic is to chose RaNDom
        literals. For this reason, will be chose a random clause and will be return a random element of it.
        ALERT: this method could be very inefficient

        Args:
            sudoku_rules: List of rules
            sudoku_numbers: List of numbers already present in the sudoku solution

        Returns:
            The literal to use in the dpll core

        """
        return random.choice(random.choice(sudoku_rules))

    def get_name(self):
        """
        The method returns the name of the heuristic.

        Returns:
            Name of the heuristic

        """
        return 'Random'
