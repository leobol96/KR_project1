from solvers import solver


class PosHeuristicSolver(solver.Solver):
    """
    The PosHeuristicSolver extends the class solver. All the methods are inherited.
    The POS heuristic aims at changing the split phase of the general dpll algorithm,
    for this purpose it overwrites the get_lieral method.

    See the documentation of the get_literal method to have more information about the split phase

    """

    def __init__(self):
        self.result = []
        self.backtrack_number = 0

    def get_literal(self, sudoku_rules, sudoku_numbers):
        """
        The method gives the literal to use in the dpll core. The aim of the POS heuristic is to create unit
        literals, deleting the POS-itive ones. For this reason, will be chose the shortest clause containing
        positives literal (P) instead of the negatives (-P) and will be return the first element of it.
        After the execution of the remove and shorten clause will be a high chance to find a new unit literal.

        Args:
            sudoku_rules: List of rules
            sudoku_numbers: List of numbers already present in the sudoku solution

        Returns:
            The literal to use in the dpll core

        """

        for x in range(2, 10):
            for rule in sudoku_rules:
                if rule[0][0] != '-' and len(rule) == x:
                    return rule[0]

    def get_name(self):
        """
        The method returns the name of the heuristic.

        Returns:
            Name of the heuristic

        """
        return 'Pos'


