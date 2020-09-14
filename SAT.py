import sys
import time
import common_functions as common


# Doesn't work
def dlis_heuristic(sudokurules):
    hashmap = {}
    for rule in sudokurules:
        for literal in rule:
            hashmap[literal] = hashmap.get(literal, 0) + 1

    n_time = 0
    for key in hashmap:
        if hashmap.get(key) > n_time:
            to_return = key
            n_time = hashmap.get(key)

    return to_return


if __name__ == "__main__":

    if len(sys.argv) < 4:
        print("Please insert:\narg1: Name of the sudoku file\narg2: Name of the rules file")
    else:
        print("1.0: Start")
        start_time = time.time()
        sudoku_numbers = []
        sudoku_rules = []
        result = []
        version = sys.argv[1]

        print("2.0: Reading the sudoku")
        sudoku_name = sys.argv[2]
        common.read_sudoku(sudoku_name, sudoku_numbers)
        print("3.0: Reading the rules")
        rule_name = sys.argv[3]
        common.read_rules(rule_name, sudoku_rules)

        print("5.0: Starting solving")
        solver = common.chose_solver(version)
        result = solver.solve(sudoku_numbers, sudoku_rules)

        print("6.0: Finish")
        print("Total time in Seconds :" + format(time.time() - start_time, '.2f'))

        print("7.0: Writing the result")
        common.writefile(sudoku_name, result)
