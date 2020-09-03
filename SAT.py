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
    with open("sudoku-example.txt","r") as puzle_file:
        for line in puzle_file:
            # Filling the matrix with the numbers token from the file 
            sudoku[int(line[0])-1,int(line[1])-1] = int(line[2])
        return sudoku

# Check if the value is in the row
def check_row(arr, row, num, dimension): 
    for i in range(dimension): 
        if(arr[row][i] == num): 
            return True
    return False
  
# Check if the value is in the col
def check_col(arr, col, num, dimension): 
    for i in range(dimension): 
        if(arr[i][col] == num): 
            return True
    return False
  
# Check if the value is in the box 
def check_box(arr, row, col, num): 
    for i in range(3): 
        for j in range(3): 
            if(arr[i + row][j + col] == num): 
                return True
    return False

# Row + col + box
def check_all(arr, row, col, num, dimension): 
    return not check_row(arr, row, num, dimension) and not check_col(arr, col, num, dimension) and not check_box(arr, row - row % 3, col - col % 3, num) 
  
            
# This function used the Davis Putman algorithm to solve the sat problem
def DP_algorithm():
    print('to_do')

# This function used the recursion to solve the sat problem 
def heuristic_algorithm_recursive(sudoku,dimension,col,row):

    # Last element of the sudoku 
    if (col == dimension - 1 and row == dimension):
        return True
          
    # Last element of the row
    if (row == dimension):
        col += 1 
        row = 0

    # Element already assigned
    if (sudoku[col][row] != 0):
        return heuristic_algorithm_recursive(sudoku,dimension,col,row+1)
    
    # Recursion
    for k in range(1, dimension + 1):
        # Check if the sudoku is valid with the new value
        if (check_all(sudoku,col,row,k,dimension)):
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
    
    dimension = 9
    sudoku = encodePuzle(dimension)
    print("Sudoku to solve")
    print(sudoku)
    if (heuristic_algorithm_recursive(sudoku,dimension,0,0)):
        print("This is the solution:")
        print(sudoku)
    else:
        print("There aren't solutions")