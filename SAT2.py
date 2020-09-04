def ReadSudoku():
    Sudoku = open("sudoku-example.txt", "r")
    for number in Sudoku:
        end_number = number.split()
        Sudokunumbers.append(end_number[0])

def ReadRules():
    rules = open("sudoku-rules.txt", "r")
    for row in rules:
        if row[0] == "p":
            pass
        else:
            splitrow = row.split()
            splitrow.pop()
            sudokurules.append(splitrow)


if __name__=="__main__":
    Sudokunumbers = []
    sudokurules = []
    ReadSudoku()
    print(Sudokunumbers)
    ReadRules()
    print(sudokurules)
