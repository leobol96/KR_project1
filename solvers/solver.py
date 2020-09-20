import common_functions as common
import copy


class Solver:

    def __init__(self):
        self.result = []
        self.backtrack_number = 0

    # This function removes the clauses from the rules list that have the literal passed as parameter.
    # Parameter 01: Literal used to remove the clauses
    # Parameter 02: List of clauses where to apply the function
    def remove_clauses(self, literal, sudoku_rules):
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

    # This function shorts the clauses from the rules list that have the literal passed as parameter.
    # Parameter 01: Literal used to remove the clauses
    # Parameter 02: List of clauses where to apply the function
    def shorten_clauses(self, literal, sudoku_rules):
        # The symbol [:] it 's used to work with a copy of the original element. Deleting objects where you are working
        # could cause problems
        for rule in sudoku_rules[:]:
            for number in rule[:]:
                if isinstance(literal, list):
                    if common.negate(number) in literal:
                        rule.remove(number)
                else:
                    # For the strings (397 in -397) is true, this behaviour is not valid for lists
                    if common.negate(number) == literal:
                        rule.remove(number)

    # This function iterates over the rule to find any pure literals.
    # If a pure literal is found, the remove and shorten functions are called.
    # At the end the function calls itself if it finds some pure literals
    # Parameter 01: List of rules
    # Parameter 02: List of number given at the start
    def check_delete_unit_literals(self, sudoku_rules, sudoku_numbers):
        number_unit_literals = 0
        literal_list = []
        for rule in sudoku_rules[:]:
            if len(rule) == 1:
                number_unit_literals += 1
                if rule[0][0] != '-':
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

    # The function gives the literal to use in the dpll_2 core.
    # The literal given depends from which version is chosen at the start.
    # For the heuristics versions, this method is overwritten
    # Parameter 01: List of rules
    def get_literal(self, sudoku_rules, sudoku_numbers):
        return sudoku_rules[0][0]

    # The function returns the name of the algorithm
    def get_name(self):
        return 'General'

    # The function is the core part of the algorithm Davis-Putman.
    # With the recursion paradigm ir solves the SAT problem.
    # Parameter 01: The list of rules
    # Parameter 02: Literal to delete from the rules
    # Parameter 03: List of numbers used in the solution
    def dpll_2(self, sudoku_rules, literal, sudoku_numbers):

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

        if literal_to_use[0] != '-' and literal_to_use not in sudoku_numbers:
            sudoku_numbers.append(literal_to_use)

        if self.dpll_2(sudoku_rules, literal_to_use, sudoku_numbers):
            return True
        else:
            if (common.negate(literal_to_use))[0] != '-' and common.negate(literal_to_use) not in back_sudoku_number:
                back_sudoku_number.append(common.negate(literal_to_use))
            return self.dpll_2(back_sudoku_rules, common.negate(literal_to_use), back_sudoku_number)

    # This function is the start point of the solving part
    # Some steps are performed before the dpll core in order to optimizing the solver.
    # Parameter 01: List of number given at the start.
    # Parameter 02: List of rules 
    def solve(self, sudoku_numbers, sudoku_rules):

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

            if literal_to_use[0] != '-' and literal_to_use not in sudoku_numbers:
                sudoku_numbers.append(literal_to_use)

            if not self.dpll_2(sudoku_rules, literal_to_use, sudoku_numbers):
                if (common.negate(literal_to_use))[0] != '-' and common.negate(
                        literal_to_use) not in back_sudoku_number:
                    back_sudoku_number.append(common.negate(literal_to_use))
                self.dpll_2(back_sudoku_rules, common.negate(literal_to_use), back_sudoku_number)

        return self.result, self.backtrack_number
