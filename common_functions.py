# File used fot the common function
import math
from solvers import cul_heuristic_solver as he2, rnd_heuristic_solver as he3, solver, hum_heuristic_solver as he4, \
    pos_heuristic_solver as he5


def read_sudoku(filename, sudoku_numbers):
    """
    The function reads the problem given in DIMACS format

    Args:
        filename: Name of the file to read
        sudoku_numbers: List of numbers already present in the sudoku solution

    """

    with open(filename, "r") as sudoku:
        for number in sudoku:
            end_number = number.split()
            sudoku_numbers.append(end_number[0])


def read_rules(filename):
    """
    The function reads the rules of the problem in DIMACS format

    Args:
        filename: Name of the file to read

    """

    sudoku_rules = []
    with open(filename, "r") as rules:
        for row in rules:
            if row[0] == "p":
                pass
            else:
                splitrow = row.split()
                splitrow.pop()
                sudoku_rules.append(splitrow)
    return sudoku_rules


def read_sdk(filename):
    """
    The function reads a list of SAT problems in a sdk format

    Args:
        filename: Name of the file in sdk formats

    Returns:

    """

    to_return = []
    with open(filename, "r") as sdk:
        for line in sdk:
            sudoku = []
            line = line.rstrip("\n")
            max_row = int(math.sqrt(len(line)))
            col = row = 1
            for char in line:
                if char != '.':
                    sudoku.append(str(col) + str(row) + char)
                if row == max_row:
                    row = 1
                    col += 1
                else:
                    row += 1
            to_return.append(sudoku)
    return to_return


def writefile(filename, result, type):
    """
    The function writes the solution.
    The solution could be written in the two different formats DIMACS and SDK

    Args:
        filename: Name of the file to create
        result: Result to write in the DIMACS file
        type: Dimacs or SDK, it depends from the type of the file to write

    """

    with open(filename.replace('.txt', '.out.txt'), 'w') as output:
        if result:
            if type == 'dimacs':
                for idx, number in enumerate(result):
                    output.write(number + ' 0\n')
            elif type == 'sdk':
                for sudoku in result:
                    for literal in sudoku:
                        output.write(literal[2])
                    output.write('\n')


def negate(literal):
    """
    The function denies the literal passed as parameter

    Args:
        literal: Literal to deny

    Returns:
        The denied of the literal passed as parameter
    """

    if literal[0] == '-':
        return literal[1:]
    else:
        return '-' + literal


def chose_solver(version):
    """
    The function returns the correct instance of the solver given the argument passed as parameter

    Args:
        version: Version of the solver

    Returns:
        Instance of the solver chosen

    """
    if version == '-S2':
        return he2.CulHeuristicSolver()
    elif version == '-S3':
        return he3.RndHeuristiSolver()
    elif version == '-S4':
        return he4.HumHeuristicSolver()
    elif version == '-S5':
        return he5.PosHeuristicSolver()
    else:
        return solver.Solver()


def deep_copy_personalized(type, list):
    """
    The function deepcopy the object passed as parameter.
    The function has been developed because the copy.deepcopy is to expensive

    Args:
        type: Type of list to copy (list of literal or list of rules)
        list: List to copy

    Returns:
        Deepcopy of the list
    """

    to_return = []
    if type == 'literal':
        for literal in list:
            to_return.append(literal)
    elif type == 'rules':
        for rules in list:
            rule = []
            for literal in rules:
                rule.append(literal)
            to_return.append(rule)
    return to_return


def filter_sat_solution(sat_solution):
    """
    Function to filter the sat solution.
    The function returns only the element used in the sudoku

    Args:
        sat_solution: Sat solution to be filtered

    Returns:
        Sudoku solution

    """
    result = []
    for literal in sat_solution:
        if literal[0] != '-':
            result.append(literal)
    result.sort()
    return result

