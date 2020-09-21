# KR_project1

The project is built for solving the sudoku problem using a sat solver.

## Structure
The main program is the **SAT.py**. The latter contains the main program and the the differet logic to execute the software in three possible ways(See the option paragraph)

The **common_functions.py** contains all the functions that are used for general scopes (read,write, ecc). This file is imported and used not only from the SAT.py but also from the solver.py

The **solver.py** contains the solver class that is the core of the project. The solver class contains the general dpll algorithm and with the recursion paradigm it is able to solve general SAT problems.
The solver.py file can be found in the solvers folder. This contains all the different heuristic version of the solver. These heurists versions overwrite the function **get_literal** that is the one which takes care of chose the correct literal to use.

![structure](https://github.com/leobol96/KR_project1/blob/heuristics_implementation/img/project_structure.jpg)

## Execution options
There are three different options to call the software.
1. ***SAT.py -S1 sudoku-example.txt sudoku-rules.txt***
	- The **first parameter** must be the (Version), it indicates which heruristic will be used
        - S1 **General algorithm**:
        - S2 **Create unit literals heuristic (CUL)**:
        - S3 **Random heuristic (RND)**: 
        - S4 **Human heuristic (HUM)**:
        - S5 **Positive heuristic (POS)**:
	-   The **second parameter** must be the name of the sudoku to solve. The file has to be present in dimacs format in the directory.
	-   The **third parameter** must be the name of the file with sudoku's rules. The file has to be present in dimacs format in the directory.
2. ***SAT.py sudoku_file.sdk.txt***-	
	- The **first parameter** must be the name of the file with all the sudoku in sdk forma
4. ***SAT.py -E sudoku_file.sdk.txt***
	- This option it's used to launch the experiment    

## Others 
