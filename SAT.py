import sys
import time
import common_functions as common


if __name__ == "__main__":

    if len(sys.argv) == 4:
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
        sudoku_rules = common.read_rules(rule_name)

        print("5.0: Starting solving")
        solver = common.chose_solver(version)
        result = solver.solve(sudoku_numbers, sudoku_rules)

        print("6.0: Finish")
        print("Total time in Seconds :" + format(time.time() - start_time, '.2f'))

        print("7.0: Writing the result")
        common.writefile(sudoku_name, result)

    elif len(sys.argv) == 2:
        result = []
        sudoku_list = common.read_sdk(sys.argv[1])
        solver = common.chose_solver('-S1')
        rule_name = 'sudoku-rules.txt'
        for sudoku in sudoku_list:
            #print('------------------------')
            #print(sudoku)
            #print('------------------------')
            result.append(solver.solve(sudoku, common.read_rules(rule_name)))

        for sudoku in result:
            print('------------------------')
            print(sudoku)
            print('------------------------')




