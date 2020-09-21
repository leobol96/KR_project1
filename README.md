# KR_project1

The project is built for solving the sudoku problem using a sat solver.

## Structure
The main program is the **SAT.py**. The latter contains the main program and the different logic to execute the software in three possible ways(See the execution options paragraph)

The **common_functions.py** contains all the functions that are used for general scopes (read, write, etc). This file is imported and used not only from the SAT.py but also from the solver.py

The **solver.py** contains the solver class that is the core of the project. The solver class contains the general dpll algorithm and with the recursion paradigm it is able to solve general SAT problems.
The solver.py file can be found in the solvers folder. This dir contains all the different heuristic version of the solver. These heurists versions overwrite the function **get_literal** that is the one which takes care of chose the correct literal to use.


![structure](https://github.com/leobol96/KR_project1/blob/heuristics_implementation/img/project_structure.jpg)


## Execution options
There are three different options to call the software.
1. ***SAT.py -S1 sudoku-example.txt sudoku-rules.txt***
	- The **first parameter** must be the (Version), it indicates which heuristic will be used
        - S1 **Standard algorithm**:The standard splitting method used is based on picking in the first clause that we come across in the sudoku rules. If there needs to be a split the first literal in the first clause in the sudoku rule is chosen.
        - S2 **Create unit literals heuristic (CUL)**: The CUL heuristic chose first element of the shortest clause. Choosing the shortest clause in the rules there is a high probability to create unit literals. Create unit literals is ever positive as they can only be true.
        - S3 **Random heuristic (RND)**: The RND heuristic chooses a random literal in a random clause of the sudoku rules file. This heuristic is unpredictable, sometimes brings good results while other times brings bad results.
        - S4 **Human heuristic (HUM)**: The HUM heuristic is designed to reason like a human. A matrix is created. All empty sudoku positions have a score. The more numbers there are in the same column or in the same row of the empty cell the higher the score will be. The literal chosen from this heuristic will be the one in the matrix with the highest score.
        - S5 **Positive heuristic (POS)**: The POS is an evolution of the CUL heuristic. Not only it looks for the shortest clause but also for one with positive literal (P).
	-   The **second parameter** must be the name of the sudoku to solve. The file has to be present in dimacs format in the directory.
	-   The **third parameter** must be the name of the file with sudoku's rules. The file has to be present in dimacs format in the directory.
2. ***SAT.py sudoku_file.sdk.txt***-	
	- The **first parameter** must be the name of the file with all the sudoku in sdk format
4. ***SAT.py -E sudoku_file.sdk.txt***
	- This option it's used to launch the experiment    

## Others 
