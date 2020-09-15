import sys
import time
import common_functions as common


if __name__ == "__main__":

    print("Starting ...")
    start_time = time.time()

    if len(sys.argv) == 4:

        sudoku_numbers = []
        sudoku_rules = []
        result = []
        version = sys.argv[1]

        sudoku_name = sys.argv[2]
        common.read_sudoku(sudoku_name, sudoku_numbers)
        rule_name = sys.argv[3]
        sudoku_rules = common.read_rules(rule_name)

        solver = common.chose_solver(version)
        result = solver.solve(sudoku_numbers, sudoku_rules)

        common.writefile(sudoku_name, result, 'dimacs')

    elif len(sys.argv) == 2:
        result = []
        sudoku_list = common.read_sdk(sys.argv[1])
        solver = common.chose_solver('-S2')
        rule_name = 'sudoku-rules.txt'
        sudoku_rules = common.read_rules(rule_name)

        for sudoku in sudoku_list:
            result.append(solver.solve(sudoku, common.deep_copy_personalized('rules', sudoku_rules)))
        common.writefile(sys.argv[1], result, 'sdk')

    print("Finish !")
    print("Total time in Seconds :" + format(time.time() - start_time, '.2f'))




