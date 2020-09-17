import sys
import time
import common_functions as common

if __name__ == "__main__":

    print("Starting ...")
    start_time = time.time()

    # Case with one sudoku.txt e one sudoku_rules.txt
    # The output will be a DIMACS file
    if len(sys.argv) == 4:

        sudoku_numbers = []
        sudoku_rules = []
        result = []
        version = sys.argv[1]
        sudoku_name = sys.argv[2]
        rule_name = sys.argv[3]

        # Reading the sudoku given
        common.read_sudoku(sudoku_name, sudoku_numbers)
        # Reading the rules file
        sudoku_rules = common.read_rules(rule_name)
        # Creating a new instance of the solver using the version given from command line
        solver = common.chose_solver(version)
        # Solving the sudoku
        result, backtrack_number = solver.solve(sudoku_numbers, sudoku_rules)
        print('The number of backtrack is :', backtrack_number)
        # Writing the solution in DIMACS format
        common.writefile(sudoku_name, result, 'dimacs')

    # Case with one file.sdk
    # The output file will be a sdk.out with the solutions of all the sudoku present in the input file
    elif len(sys.argv) == 2:

        result_list = []
        back_track_list = []
        rule_name = 'sudoku-rules.txt'
        solvers = ['-S1', '-S2', '-S3', '-S5']

        # Read the rules file, with the sdk option the rules file will be always the 9x9
        sudoku_rules = common.read_rules(rule_name)
        # Read the list of sudoku to solve
        sudoku_list = common.read_sdk(sys.argv[1])

        # Creating a new instance of the sudoku, using the best heuristic of the solver
        solver = common.chose_solver('-S1')
        for sudoku in sudoku_list:
            result, backtrack_number = solver.solve(sudoku, common.deep_copy_personalized('rules', sudoku_rules))
            result_list.append(result)
            back_track_list.append(backtrack_number)
            # print('The number of backtrack is :', backtrack_number)
        # Writing the file sdk.out with all the sudoku solved
        common.writefile(sys.argv[1], result_list, 'sdk')
        print("-----------------------------------")
        print('The average of backtrack is :' + str(sum(back_track_list) / len(back_track_list)))
        print('The average time is :' + format((time.time() - start_time) / len(back_track_list), '.2f'))

    print("-----------------------------------")
    print("Finish !")
    print("Total time in Seconds :" + format(time.time() - start_time, '.2f'))
