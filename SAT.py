# SAT solvers - Project 1 Knowledge Representation
import numpy as np

# The function is used to encode the given rules 
def readRules():
    rules = open("sudoku-rules.txt", "r")
    return rules.read()

# The function is used to encode the given sudoku in a numpy matrix
# The value returned is the sudoku puzle to be solved
def encodePuzle(dimension):
    # Creating an array N * N dimension with only zeros
    sudoku = np.zeros((dimension, dimension)) 
    with open("sudoku-example_6_6.txt","r") as puzle_file:
        for line in puzle_file:
            # Filling the matrix with the numbers token from the file 
            sudoku[int(line[0])-1,int(line[1])-1] = int(line[2])
        return sudoku


# Returns true if the sudoku passed as a parameter follows the rules of the game  
def checkValidity(sudoku,dimension):
    # For every sudoku's cell 
    for idx_col in range(dimension):
        for idx_row in range(dimension):
            for k in range(dimension):
                #col
                if (idx_col != k and sudoku[idx_col][idx_row] == sudoku[k][idx_row]):
                    return False
                #row
                if (idx_row != k and sudoku[idx_col][idx_row] == sudoku[idx_col][k]):
                    return False        
    return True
            
# This function used the Davis Putman algorithm to solve the sat problem
def DP_algorithm():
    print('to_do')

# This function used the recursion to solve the sat problem 
def heuristic_algorithm_recursive(sudoku,dimension,col,row):

    # Last element of the sudoku 
    if (col == dimension - 1 and row == dimension):
        return checkValidity(sudoku,dimension)
          
    # Last element of the row
    if (row == dimension):
        col += 1 
        row = 0

    # Element already assigned
    if (sudoku[col][row] != 0):
        return heuristic_algorithm_recursive(sudoku,dimension,col,row+1)
    
    # Recursion
    for k in range(1, dimension + 1):
        sudoku[col][row] = k
        if (heuristic_algorithm_recursive(sudoku,dimension,col,row + 1)):
            return True
        sudoku[col][row] = 0

    return False

# This will be the second heuristic method to solve the SAT problem
def heuristic_algorithm_two():
    print('to_do')

# Main function  
if __name__=="__main__": 
    
    dimension = 6
    sudoku = encodePuzle(dimension)
    print("Sudoku to solve")
    print(sudoku)
    if (heuristic_algorithm_recursive(sudoku,dimension,0,0)):
        print("This is the solution:")
        print(sudoku)
    else:
        print("There aren't solutions")