import common_functions as common


class Solver:
    """
    The Solver is in charge of solving the SAT problem.
    Inside it contains the dpll_2 algorithm in a general version.

    """

    def __init__(self):
        self.result = []
        self.backtrack_number = 0

    def remove_clauses(self, literal, sudoku_rules):
        """
        This method removes the clauses from the rules list that have the literal passed as parameter.

        Args:
            literal: Literal to remove
            sudoku_rules: List of clauses where delete the literal

        """

        for rule in sudoku_rules[:]:
            for number in rule[:]:
                if isinstance(literal, list):
                    if number in literal:
                        sudoku_rules.remove(rule)
                        break
                else:
                    # For the strings (397 in -397) is true, this behaviour is not valid for lists
                    if number == literal:
                        sudoku_rules.remove(rule)
                        break

    def shorten_clauses(self, literal, sudoku_rules):
        """
        This function shorts the clauses from the rules list that have the literal passed as parameter.

        Args:
            literal: Literal to use for shortening the clauses
            sudoku_rules: List of clauses to be shortened

        """

        for rule in sudoku_rules[:]:
            for number in rule[:]:
                if isinstance(literal, list):
                    if common.negate(number) in literal:
                        rule.remove(number)
                else:
                    # For the strings (397 in -397) is true, this behaviour is not valid for lists
                    if common.negate(number) == literal:
                        rule.remove(number)

    def check_delete_unit_literals(self, sudoku_rules, sudoku_numbers):
        """
        This function iterates over the rules to find unit literals.
        If a unit literal is found, the remove and shorten functions are called over it.

        Args:
            sudoku_rules: List of rules
            sudoku_numbers: List of numbers already present in the sudoku solution

        """
        number_unit_literals = 0
        literal_list = []
        for rule in sudoku_rules[:]:
            if len(rule) == 1:
                number_unit_literals += 1
                if rule[0] not in sudoku_numbers: sudoku_numbers.append(rule[0])
                # Check also for the negate, because creating a list with P and -P it causes problem
                if rule[0] not in literal_list and common.negate(rule[0]) not in literal_list: literal_list.append(
                    rule[0])

        # Optimizing shorten and remove
        if literal_list:
            self.remove_clauses(literal_list, sudoku_rules)
            self.shorten_clauses(literal_list, sudoku_rules)

        if number_unit_literals > 1 and [] not in sudoku_rules:
            self.check_delete_unit_literals(sudoku_rules, sudoku_numbers)

    def get_literal(self, sudoku_rules, sudoku_numbers):
        """
        The methods return the literal to use in the next iteration of the dpll core

        Args:
            sudoku_rules: List of rules
            sudoku_numbers: List of literals already present in the sudoku solution

        Returns:
            The literal to use in the dpll core

        """

        return sudoku_rules[0][0]

    def get_name(self):
        """
        The method returns the name of the heuristic.

        Returns:
            Name of the heuristic

        """
        return 'General'

    def dpll_2(self, sudoku_rules, literal, sudoku_numbers):
        """
        The function is the core part of the algorithm Davis-Putnam.
        With the recursion paradigm it solves the SAT problem.

        Args:
            sudoku_rules: List of rules
            literal: Literal to delete from the rules and to add at the solution
            sudoku_numbers: List of literals already present in the sudoku solution

        Returns:
            True if the problem has a solution, false otherwise
        """

        self.remove_clauses(literal, sudoku_rules)
        self.shorten_clauses(literal, sudoku_rules)
        self.check_delete_unit_literals(sudoku_rules, sudoku_numbers)

        if not sudoku_rules:
            sudoku_numbers.sort()
            self.result = sudoku_numbers[:]
            return True
        if [] in sudoku_rules:
            self.backtrack_number += 1
            return False

        literal_to_use = self.get_literal(sudoku_rules, sudoku_numbers)

        back_sudoku_rules = common.deep_copy_personalized('rules', sudoku_rules)
        back_sudoku_number = common.deep_copy_personalized('literal', sudoku_numbers)

        if literal_to_use not in sudoku_numbers:
            sudoku_numbers.append(literal_to_use)

        if self.dpll_2(sudoku_rules, literal_to_use, sudoku_numbers):
            return True
        else:
            if common.negate(literal_to_use) not in back_sudoku_number:
                back_sudoku_number.append(common.negate(literal_to_use))
            return self.dpll_2(back_sudoku_rules, common.negate(literal_to_use), back_sudoku_number)

    def solve(self, sudoku_numbers, sudoku_rules):
        """
        This function is the start point of the solving part
        Some steps are performed before the dpll core in order to optimizing the solver.

        Args:
            sudoku_numbers: List of literals already present in the sudoku solution
            sudoku_rules: List of rules

        Returns:
            List of positive literal present in the solution and number of backtrack found during the resolution of the problem
        """

        self.result = []
        self.backtrack_number = 0

        # print("Solving ...")
        self.remove_clauses(sudoku_numbers, sudoku_rules)
        self.shorten_clauses(sudoku_numbers, sudoku_rules)
        self.check_delete_unit_literals(sudoku_rules, sudoku_numbers)

        if not sudoku_rules:
            self.result = sudoku_numbers[:]
            self.result.sort()
        else:

            literal_to_use = self.get_literal(sudoku_rules, sudoku_numbers)
            back_sudoku_rules = common.deep_copy_personalized('rules', sudoku_rules)
            back_sudoku_number = common.deep_copy_personalized('literal', sudoku_numbers)

            if literal_to_use not in sudoku_numbers:
                sudoku_numbers.append(literal_to_use)

            if not self.dpll_2(sudoku_rules, literal_to_use, sudoku_numbers):
                if common.negate(literal_to_use) not in back_sudoku_number:
                    back_sudoku_number.append(common.negate(literal_to_use))
                self.dpll_2(back_sudoku_rules, common.negate(literal_to_use), back_sudoku_number)

        return self.result, self.backtrack_number



