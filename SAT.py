import copy
import random

# Read the sudoku 
def readSudoku():
    Sudoku = open("sudoku-example_9_9_easy.txt", "r")
    for number in Sudoku:
        end_number = number.split()
        sudokunumbers.append(end_number[0])

# Read the rules in DIMACS format
def readRules():
    rules = open("sudoku-rules.txt", "r")
    for row in rules:
        if row[0] == "p":
            pass
        else:
            splitrow = row.split()
            splitrow.pop()
            sudokurules.append(splitrow)

# Negate the literal passed as a parameter
def negate(literal_to_negate):
    if (literal_to_negate[0] == '-'):
        return literal_to_negate[1:]
    else: 
        return '-' + literal_to_negate
        
# Create a domain
def createDomain(domain):
    for rule in sudokurules:
        for literal in rule:
            if (literal[0] == '-' and literal not in domain and literal[1:] not in sudokunumbers) or (literal[0] != '-' and literal not in domain and literal not in sudokunumbers):
                domain.append(literal)

# Remove clauses from the sudokurules using the literal passed as a parameter
def removeClauses(literal,sudokurules):
    
    #The symbol [:] it 's used to work with a copy of the original element. Deleting objects where you are working could cause problems
    for rule in sudokurules[:]:
        for number in rule[:]:
            if (literal == number):
                sudokurules.remove(rule)

# Shorten clauses from the sudokurules using the literal passed as a parameter
def shortenClauses(literal,sudokurules):
    
    #The symbol [:] it 's used to work with a copy of the original element. Deleting objects where you are working could cause problems
    for rule in sudokurules[:]:
        for number in rule[:]:
            if (number == negate(literal)):
                rule.remove(number) 

# Implementation of the DP algorithm
def dpll_2(sudokurules,literal,domain,sudokunumbers):

    removeClauses(literal,sudokurules)
    shortenClauses(literal,sudokurules)

    if not sudokurules: 
        sudokunumbers.sort()
        print(sudokunumbers)
        return True
    if [] in sudokurules: 
        return False

    # Remove from the domain P and -P
    literal_to_use = domain.pop(0)
    domain.remove(negate(literal_to_use))
    
    # The deep copies have to be executed after the pop from the domain
    back_list = copy.deepcopy(sudokurules)
    back_domain = copy.deepcopy(domain)
    back_number = copy.deepcopy(sudokunumbers)

    if dpll_2(sudokurules,literal_to_use,domain,sudokunumbers):
        # Check for -P
        return True
    else:
        # CHeck for P
        back_number.append(negate(literal_to_use)) 
        dpll_2(back_list,negate(literal_to_use),back_domain,back_number)


if __name__=="__main__":
    
    # Numbers used to solve the sudoku
    sudokunumbers = []
    # Rules used to solve the sudoku in Dimacs format 
    sudokurules = []
    # Domain where pop the numbers 
    domain = []
    
    readSudoku()
    readRules()
    createDomain(domain)

    # For all the number already in the sudoku 
    for literal in sudokunumbers:
        removeClauses(literal,sudokurules)
        shortenClauses(literal,sudokurules)

    back_list = copy.deepcopy(sudokurules)
    back_sudoNumbers = copy.deepcopy(sudokunumbers)

    domain.sort()
    literal_to_use = domain.pop(0)
    domain.remove(literal_to_use[1:])

    if not dpll_2(sudokurules,literal_to_use,domain,sudokunumbers):
        dpll_2(back_list,literal_to_use[1:],domain,back_sudoNumbers)


