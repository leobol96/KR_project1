# File used fot the common function
import math
from solvers import cul_heuristic_solver as he2, rnd_heuristic_solver as he3, solver, dlis_heuristic_solver as he4, pos_heuristic_solver as he5


# The function reads the single sudoku in DIMACS format
# Parameter 01: DIMACS sudoku filename
# Parameter 02: List where insert the numbers of the sudoku given at the start
def read_sudoku(sudoku_filename, sudokunumbers):
    with open(sudoku_filename, "r") as sudoku:
        for number in sudoku:
            end_number = number.split()
            sudokunumbers.append(end_number[0])


# The function reads the rules in DIMACS format
# Parameter 01: DIMACS rule filename
# Parameter 02: List where insert the rules
def read_rules(rules_filename):
    sudoku_rules = []
    with open(rules_filename, "r") as rules:
        for row in rules:
            if row[0] == "p":
                pass
            else:
                splitrow = row.split()
                splitrow.pop()
                sudoku_rules.append(splitrow)
    return sudoku_rules

# The function reads the file in sdk format
# Parameter 01: SDK file
def read_sdk(sdk_filename):
    to_return = []
    with open(sdk_filename, "r") as sdk:
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


# The function writes the solution of the input in a DIMACS format,
# the name of the file created will be = Name of the input file + 'out.txt'
# Parameter 01: Name of the input file
# Parameter 02: List containing the solution of the sat problem
def writefile(sudoku_out_name, result, type):
    with open(sudoku_out_name.replace('.txt', '.out.txt'), 'w') as output:
        if result:
            if type == 'dimacs':
                for idx, number in enumerate(result):
                    output.write(number + ' 0\n')
            elif type == 'sdk':
                for sudoku in result:
                    for literal in sudoku:
                        output.write(literal[2])
                    output.write('\n')


# The functions read a literal P and returns -P
# Parameter 01: Literal to deny
# Return : The denied of the literal passed as parameter
def negate(literal_to_negate):
    if literal_to_negate[0] == '-':
        return literal_to_negate[1:]
    else:
        return '-' + literal_to_negate


# The function return the correct instance of the solver given the argument passed as parameter
# Parameter 01: Argument passed in command line
# Return: the correct instance of the solver
def chose_solver(version):
    if version == '-S2':
        return he2.CulHeuristicSolver()
    elif version == '-S3':
        return he3.RndHeuristiSolver()
    elif version == '-S4':
        return he4.DlisHeuristicSolver()
    elif version == '-S5':
        return he5.PosHeuristicSolver()
    else:
        return solver.Solver()


# The function has been developed because the copy.deepcopy is to expensive
# Parameter 01: Type of list to copy
# Parameter 02: List to copy
def deep_copy_personalized(type, list):
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
