# KR_project1

The project is built for solving the sudoku problem using a sat solver.
Please read carefully this README file before use the program.
If you don't have a markdown editor or if you don't see the images, please visit: https://github.com/leobol96/KR_project1 

## Structure
The main program is the **SAT.py**. The latter contains the different logic to execute the software in three possible ways(See the execution options paragraph)

The **common_functions.py** contains all the functions that are used for general scopes (read, write, etc). This file is imported and used not only from the SAT.py but also from the solver.py

The **solver.py** contains the solver class that is the core of the project. The solver class contains the general DPLL algorithm and with the recursion paradigm, it is able to solve general SAT problems.
The solver.py file can be found in the solvers' folder. This dir contains all the different heuristic version of the solver. These heuristics versions overwrite the function **get_literal** that is the one which takes care of choosing the correct literal to use.


![structure](https://github.com/leobol96/KR_project1/blob/master/img/project_structure.jpg)


## Execution options
There are three different options to call the software.
1. ***SAT.py -Sn sudoku-rules.txt sudoku-example.txt***
	- The **first parameter** must be the (Version), it indicates which heuristic will be used
        - S1 **Standard algorithm**: The Standard heuristic chooses the first element of the first clause.
        - S2 **Create unit literals heuristic (CUL)**: The CUL heuristic chooses the first element of the shortest clause. Choosing the shortest clause in the rules there is a high probability to create unit literals. Create unit literals is ever positive as they can only be true.
        - S3 **Random heuristic (RND)**: The RND heuristic chooses a random literal in a random clause of the sudoku rules file. This heuristic is unpredictable, sometimes bring good results while other times bring bad results.
        - S4 **Human heuristic (HUMAN)**: The HUMAN heuristic is designed to reason like a human. A matrix is created. All empty sudoku positions have a score. The more numbers there are in the same column or in the same row of the empty cell the higher the score will be. The cell in the matrix with the higher number is the one with fewer alternatives. Once the ideal position has been found, the first positive literal that can be inserted in that position will be taken. **ALERT**: This heuristic is not general, it can be used only with the sudoku 9x9  
        ![hum heuristic](https://github.com/leobol96/KR_project1/blob/master/img/hum_heuristic_solver.png)
        - S5 **Positive heuristic (CULPOS)**: The CULPOS is an evolution of the CUL heuristic. Not only it looks for the shortest clause but also for one with positive literal (P).
	-   The **second parameter** must be the name of the file with sudoku's rules. The file has to be in DIMACS format.
	-   The **third parameter** must be the name of the sudoku to solve. The file has to be in DIMACS format.
2. ***SAT.py -Sn sudoku_rules_input_merged.txt***
	- The **first parameter** must be the (Version). The possible versions are mentioned above.
	- The **second parameter** must be the name of the file that contains the rules and the sudoku to solve merged into a single file. This file must be in DIMACS format. 
3. ***SAT.py -Sn sudoku-rules.txt sudoku_list.SDK.txt***	
	- The **first parameter** must be the (Version). The possible versions are mentioned above.
	-   The **second parameter** must be the name of the file with sudoku's rules. The file has to be in DIMACS format.
	-   The **third parameter** must be the name of the file containing the list of sudoku to solve. The file has to be in SDK format.
	
	**ALERT**: The sdk file must have the string '.sdk' in the name otherwiswe it will be seen as a DIMACS file
4. ***SAT.py -E general_sudoku_list.SDK.txt xversion_sudoku_list.SDK.txt***
 	
    This mode is used to start the experiment. 
    - The **first parameter** must be -E (Experiment).
    - The **second parameter** must be a collection of 9x9 sudoku valid for the general rules (the number of the sudoku must be the same of the collection used as the third parameter ).
    - The **third parameter** must be a collection of 9x9 sudoku valid for the x-sudoku rules (the number of the sudoku must be the same of the collection used as the second parameter).
    
    If you want to try this version run this:
    
    **python .\SAT.py -E .\test\online_15_23numbers.sdk.txt .\test\online_15_x_23number.sdk.txt**
    
    This mode will run each file with its rules for each heuristic implemented.
    At the end of the experiment will be created the solutions of the SDK in the Experiment folder (The experiment folder must be already present).
    Launching the experiment with the python command the following graph will be printe. In case the experiment is launched from the executable the informations will be printed only on the terminal. 
    
    ![graph](https://github.com/leobol96/KR_project1/blob/master/img/experiment_chart.jpeg)
    
    **ALERT**: the experiment mode could takes a long time, DO NOT USE big SDK format   

## Others 
