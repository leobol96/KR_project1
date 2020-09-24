import sys
import time
import common_functions as common
import numpy as np
import matplotlib.pyplot as plt
import statistics

"""
Welcome in the main part of the SAT solver.
This program has been developed for the project of Knowledge Representation Master's degree in Artificial intelligence.
This python file allows to call in three differences way. If you not yet read the README.md please do it.
Calling the sat.py without parameters allows you to have a small help, to understand better the operation.

"""

if __name__ == "__main__":

    print("Starting ...")
    solvers = ['-S1', '-S2', '-S3', '-S4', '-S5']

    if len(sys.argv) == 4 and sys.argv[1] in solvers:

        version = sys.argv[1]
        rule_file = sys.argv[2]
        input_file = sys.argv[3]
        result_single = []

        sudoku_rules = common.read_rules(rule_file)
        solver = common.chose_solver(version)

        if 'sdk' not in input_file:
            """
            This part of the software deals with the option 1 of the README.md
            Input : Rules in DIMACS format and problem in DIMACS format.
            Output : Solution in DIMACS format.
            """

            sudoku_numbers = []

            common.read_sudoku(input_file, sudoku_numbers)
            start_time = time.time()
            # Solving
            result_single, backtrack_number = solver.solve(sudoku_numbers, sudoku_rules)
            # Printing and writing results
            print('The number of backtrack is :', backtrack_number)
            end_time = format(time.time() - start_time, '.2f')
            common.writefile(input_file, result_single, 'dimacs')

            print("-----------------------------------")
            print("Finish !")

        else:
            """
            This part of the software deals with the option 2 of the README.md
            Input : Rules in DIMACS format and problem in SDK format.
            Output : Solution in SDK format.
            """

            result_list = []
            back_track_list = []
            times_list = []
            sudoku_list = common.read_sdk(input_file)

            for sudoku in sudoku_list:
                start_time = time.time()
                # Solving
                result_single, backtrack_number = solver.solve(sudoku,
                                                               common.deep_copy_personalized('rules', sudoku_rules))
                times_list.append(time.time() - start_time)
                result_list.append(common.filter_sat_solution(result_single))
                back_track_list.append(backtrack_number)
                print('The number of backtrack is :', backtrack_number)

            common.writefile(input_file, result_list, 'sdk')
            print("-----------------------------------")
            print('The average of backtrack is :' + str(sum(back_track_list) / len(back_track_list)))
            print('The average time is :' + format(sum(times_list) / len(times_list), '.2f'))

            print("-----------------------------------")
            print("Finish !")


    elif len(sys.argv) == 4 and sys.argv[1] == '-E':
        """
        This part of the software deals with the option 3 of the README.md
        Input : Two files in SDK format (general sudoku, x-sudoku)
        Output : Chart and solutions in SDK format in the experiment dir.
        """

        rules_files = ['sudoku-rules.txt', 'sudoku-rules-x.txt']
        solvers_name = []

        solvers_averages_times = []
        solvers_averages_times_x_sudoku = []

        solvers_averages_backtrack = []
        solvers_averages_backtrack_x_sudoku = []

        solvers_medians_backtrack = []
        solvers_medians_backtrack_x_sudoku = []

        solvers_std_backtrack = []
        solvers_std_backtrack_x_sudoku = []

        total_list = []
        total_x_list = []

        for idx_rule, rule in enumerate(rules_files):
            # Read the list of sudoku to solve
            if rule == rules_files[0]:
                sudoku_list = common.read_sdk(sys.argv[2])
            else:
                sudoku_list = common.read_sdk(sys.argv[3])

            # Read the rules file, with the sdk option the rules file will be always the 9x9
            sudoku_rules = common.read_rules(rule)

            # For each heuristic solvers
            for solver in solvers:
                solver = common.chose_solver(solver)
                result_list = []
                back_track_list = []
                times_list = []

                # For each problem to solve
                for idx, sudoku in enumerate(sudoku_list):
                    start_time = time.time()
                    result_single, backtrack_number = solver.solve(common.deep_copy_personalized('literal', sudoku),
                                                                   common.deep_copy_personalized('rules', sudoku_rules))
                    times_list.append(time.time() - start_time)
                    result_list.append(common.filter_sat_solution(result_single))
                    back_track_list.append(backtrack_number)
                    print(rule, '| Line:', idx + 1, '| Algorithm:', solver.get_name(), '| The number of backtrack is:',
                          backtrack_number)
                print('--------------------------------------')

                if idx_rule == 0:
                    solvers_name.append(solver.get_name())
                if rule == rules_files[0]:
                    solvers_averages_backtrack.append(sum(back_track_list) / len(back_track_list))
                    solvers_averages_times.append(format(sum(times_list) / len(times_list), '.2f'))
                    solvers_medians_backtrack.append(statistics.median(back_track_list))
                    solvers_std_backtrack.append(statistics.stdev(back_track_list))
                    total_list.append(back_track_list)
                else:
                    solvers_averages_backtrack_x_sudoku.append(sum(back_track_list) / len(back_track_list))
                    solvers_averages_times_x_sudoku.append(format(sum(times_list) / len(times_list), '.2f'))
                    solvers_medians_backtrack_x_sudoku.append(statistics.median(back_track_list))
                    solvers_std_backtrack_x_sudoku.append(statistics.stdev(back_track_list))
                    total_x_list.append(back_track_list)

                common.writefile(('experiment/' + rule + '_' + solver.get_name()).replace('.txt', '') + 'out.txt',
                                 result_list, 'sdk')

        # Create a csv with the numbers of backtrack for each solver
        common.create_csv(solvers_name, total_list, total_x_list)

        print('-----------------')
        print(solvers_name)
        print('avg BK', solvers_averages_backtrack)
        print('avg time', solvers_averages_times)
        print('median', solvers_medians_backtrack)
        print('std', solvers_std_backtrack)
        print('-----------------')
        print(solvers_name)
        print('avg BK', solvers_averages_backtrack_x_sudoku)
        print('avg time', solvers_averages_times_x_sudoku)
        print('median', solvers_medians_backtrack_x_sudoku)
        print('std', solvers_std_backtrack_x_sudoku)

        # Draw plot to check the hypothesis of the experiment
        n_algorithm = np.arange(len(solvers_name))
        bar_width = 0.35
        fig, ax = plt.subplots(nrows=2, ncols=2)
        Normal = ax[0, 0].bar(n_algorithm - bar_width / 2, solvers_averages_backtrack, bar_width, label="Normal")
        x_sudoku = ax[0, 0].bar(n_algorithm + bar_width / 2, solvers_averages_backtrack_x_sudoku, bar_width,
                                label="X-Sudoku")
        ax[0, 0].set_ylabel('BackTrack')
        ax[0, 0].set_title('Average BackTrack')
        ax[0, 0].set_xticks(n_algorithm)
        ax[0, 0].set_xticklabels(solvers_name)
        ax[0, 0].legend()

        Normal = ax[1, 0].bar(n_algorithm - bar_width / 2, solvers_averages_times, bar_width, label="Normal")
        x_sudoku = ax[1, 0].bar(n_algorithm + bar_width / 2, solvers_averages_times_x_sudoku, bar_width,
                                label="X-Sudoku")
        ax[1, 0].set_ylabel('Seconds')
        ax[1, 0].set_title('Average time')
        ax[1, 0].set_xticks(n_algorithm)
        ax[1, 0].set_xticklabels(solvers_name)
        ax[1, 0].legend()

        Normal = ax[0, 1].bar(n_algorithm - bar_width / 2, solvers_medians_backtrack, bar_width, label="Normal")
        x_sudoku = ax[0, 1].bar(n_algorithm + bar_width / 2, solvers_medians_backtrack_x_sudoku, bar_width,
                                label="X-Sudoku")
        ax[0, 1].set_ylabel('BackTrack')
        ax[0, 1].set_title('Median BackTrack')
        ax[0, 1].set_xticks(n_algorithm)
        ax[0, 1].set_xticklabels(solvers_name)
        ax[0, 1].legend()

        Normal = ax[1, 1].bar(n_algorithm - bar_width / 2, solvers_std_backtrack, bar_width, label="Normal")
        x_sudoku = ax[1, 1].bar(n_algorithm + bar_width / 2, solvers_std_backtrack_x_sudoku, bar_width,
                                label="X-Sudoku")
        ax[1, 1].set_ylabel('BackTrack')
        ax[1, 1].set_title('Standard deviation BackTrack')
        ax[1, 1].set_xticks(n_algorithm)
        ax[1, 1].set_xticklabels(solvers_name)
        ax[1, 1].legend()

        plt.show()

    else:
        print('This is the sat solver for the Knowledge Representation project')
        print(
            'If you are watching this, it means that either you called the program without parameter or you used '
            'wrong parameters')
        print('Here are the possibles commands')
        print('-------------------------')
        print('01: Version + Rules in Dimacs format + Problem in Dimacs format')
        print('   - The version must be -Sn where n is between 1 and 5')
        print('-------------------------')
        print('02: Version + Rules in Dimacs format + Problem in SDK format')
        print('   - The version must be -Sn where n is between 1 and 5')
        print('-------------------------')
        print('03: -E + SDK format for normal rule + SDK format for x-sudoku rules')
        print('   - This mode is used to start the experiment')
        print('   - Both SDK file must contain 9x9 sudoku because the rules are taken automatically ')
        print('   - ALERT: the experiment mode could takes a long time, DO NOT USE big sdk format')
