import sys
import time
import common_functions as common
import numpy as np
import matplotlib.pyplot as plt

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

        print("-----------------------------------")
        print("Finish !")
        print("Total time in Seconds :" + format(time.time() - start_time, '.2f'))


    # Case with one file.sdk
    # The output file will be a sdk.out with the solutions of all the sudoku present in the input file
    elif len(sys.argv) == 2:

        result_list = []
        back_track_list = []
        rule_name = 'sudoku-rules.txt'

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
            print('The number of backtrack is :', backtrack_number)
        # Writing the file sdk.out with all the sudoku solved
        common.writefile(sys.argv[1], result_list, 'sdk')
        print("-----------------------------------")
        print('The average of backtrack is :' + str(sum(back_track_list) / len(back_track_list)))
        print('The average time is :' + format((time.time() - start_time) / len(back_track_list), '.2f'))

        print("-----------------------------------")
        print("Finish !")
        print("Total time in Seconds :" + format(time.time() - start_time, '.2f'))


    # Case with sdk for the experiment
    elif len(sys.argv) == 3 and sys.argv[1] == '-E':

        rules_files = ['sudoku-rules.txt', 'sudoku-rules-x.txt']
        solvers = ['-S1', '-S2', '-S3', 's4', '-S5']
        solvers_name = []
        solvers_averages_times = []
        solvers_averages_backtrack = []
        solvers_averages_times_x_sudoku = []
        solvers_averages_backtrack_x_sudoku = []

        # Read the list of sudoku to solve
        sudoku_list = common.read_sdk(sys.argv[2])
        for idx_rule,rule in enumerate(rules_files):
            # Read the rules file, with the sdk option the rules file will be always the 9x9
            sudoku_rules = common.read_rules(rule)

            # For each heuristic solvers
            for solver in solvers:
                solver = common.chose_solver(solver)
                result_list = []
                back_track_list = []
                start_time = time.time()
                for idx, sudoku in enumerate(sudoku_list):
                    result, backtrack_number = solver.solve(common.deep_copy_personalized('literal', sudoku),
                                                            common.deep_copy_personalized('rules', sudoku_rules))
                    result_list.append(result)
                    back_track_list.append(backtrack_number)
                    print(rule, '| Line:', idx + 1, '| Algorithm:', solver.get_name(), '| The number of backtrack is:',
                          backtrack_number)
                print('--------------------------------------')

                if idx_rule == 0:
                    solvers_name.append(solver.get_name())
                if rule == 'sudoku-rules.txt':
                    solvers_averages_backtrack.append(sum(back_track_list) / len(back_track_list))
                    solvers_averages_times.append(format((time.time() - start_time) / len(back_track_list), '.2f'))
                    common.writefile(sys.argv[2], result_list, 'sdk')
                else:
                    solvers_averages_backtrack_x_sudoku.append(sum(back_track_list) / len(back_track_list))
                    solvers_averages_times_x_sudoku.append(format((time.time() - start_time) / len(back_track_list), '.2f'))
                    common.writefile(sys.argv[2].replace('.txt', 'x.txt'), result_list, 'sdk')

        # Draw plot
        n_algorithm = np.arange(len(solvers_name))
        bar_width = 0.35
        fig, ax = plt.subplots()
        Normal = ax.bar(n_algorithm - bar_width/2, solvers_averages_backtrack, bar_width, label="Normal")
        x_sudoku = ax.bar(n_algorithm + bar_width/2, solvers_averages_backtrack_x_sudoku, bar_width, label="X-Sudoku")
        ax.set_xlabel('Algorithm')
        ax.set_ylabel('BackTrack')
        ax.set_title('Average of BackTrack in normal sudoku and x sudoku')
        ax.set_xticks(n_algorithm)
        ax.set_xticklabels(solvers_name)
        ax.legend()
        plt.show()

        print("---------- Average BackTrack----------------")
        print(solvers_name)
        print('Normal', solvers_averages_backtrack)
        print('X sudoku', solvers_averages_backtrack_x_sudoku)

        print("---------- Average Time------------------")
        print(solvers_name)
        print('Normal', solvers_averages_times)
        print('X sudoku', solvers_averages_times_x_sudoku)



    # Help
    else:
        print('This is the sat solver for the Knowledge Representation project')
        print('Here are the possibles commands')
        print('-------------------------')
        print('01: Version + Problem in Dimacs format + Rules in Dimacs format')
        print('   - The version must be -S + [1,5]')
        print('-------------------------')
        print('02: SDK')
        print('   - The sdk must contains 9x9 sudoku')
        print('-------------------------')
        print('03: -E + SDK')
        print('   - This mode is used to start the experiment')
        print('   - ALLERT: the experiment mode could takes a long time, DO NOT USE big sdk format')
