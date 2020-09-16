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
        result, backtrack_number = solver.solve(sudoku_numbers, sudoku_rules)
        print('The number of backtrack is :', backtrack_number)
        common.writefile(sudoku_name, result, 'dimacs')

    elif len(sys.argv) == 2:
        result_list = []
        sudoku_list = common.read_sdk(sys.argv[1])
        rule_name = 'sudoku-rules.txt'
        sudoku_rules = common.read_rules(rule_name)

        for sudoku in sudoku_list:
            solver = common.chose_solver('-S1')
            result, backtrack_number = solver.solve(sudoku, common.deep_copy_personalized('rules', sudoku_rules))
            result_list.append(result)
            print('The number of backtrack is :', backtrack_number)
        common.writefile(sys.argv[1], result_list, 'sdk')

    print("Finish !")
    print("Total time in Seconds :" + format(time.time() - start_time, '.2f'))




