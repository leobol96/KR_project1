import solver
import cul_heuristic_solver as he3


# File used fot the common function

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
def read_rules(rules_filename, sudokurules):
    with open(rules_filename, "r") as rules:
        for row in rules:
            if row[0] == "p":
                pass
            else:
                splitrow = row.split()
                splitrow.pop()
                sudokurules.append(splitrow)


# The function writes the solution of the input in a DIMACS format,
# the name of the file created will be = Name of the input file + 'out.txt'
# Parameter 01: Name of the input file
# Parameter 02: List containing the solution of the sat problem
def writefile(sudoku_out_name, result):
    with open(sudoku_out_name.replace('.txt', '.out.txt'), 'w') as output:
        if result:
            for idx, number in enumerate(result):
                output.write(number + ' 0\n')


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
    if version == '-S3':
        return he3.CulHeuristicSolver()
    else:
        return solver.Solver()
