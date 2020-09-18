import os 
import sys
import math

def createDir():
    path = os.getcwd() + "/sudoku_test"
    try: 
        os.mkdir(path)
    except: 
        print("Creation of the directory failed in path ",path)
    else: 
        print("Directory sudoku_test created")
    return path

def readFile_createSudoku(fileName,filesPath):  
    listSudokus = open(fileName, "r")    
    for idx,sudoku in enumerate(listSudokus):     
        sudoku = sudoku.rstrip("\n")
        max_row = int(math.sqrt(len(sudoku)))
        col = row = 1   
        fileToCreate = 'sudoku' + str(idx + 1)
        f= open(filesPath + '/' + fileToCreate + '.txt',"w")
        sukoku_onlyNumber = sudoku.replace('.', '')
        idx_number = 1

        for idx,char in enumerate(sudoku):
            if (char != '.'):
                if (idx_number == len(sukoku_onlyNumber)):
                    f.write((str(col) + str(row) + char + ' 0'))
                else:    
                    f.write((str(col) + str(row) + char + ' 0\n'))
                idx_number += 1

            if (row == max_row): 
                row = 1 
                col += 1
            else: row +=1
        f.close()
    listSudokus.close()

if __name__=="__main__":

    if (len(sys.argv)==1):
        print("Put the file with all the sudokus as a arg 1")
    else: 
        fileName = sys.argv[1]
        filesPath = createDir()
        readFile_createSudoku(fileName,filesPath)

