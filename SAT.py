import copy
import random

# Read the sudoku 
def readSudoku():
    Sudoku = open("sudoku-example.txt", "r")
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

def check_delete_UnitLiterals(sudokurules,domain,sudokunumbers):
    
    for rule in sudokurules[:]:
        if len(rule) == 1:
            if rule in domain:domain.remove(rule[0])
            if negate(rule[0]) in domain:domain.remove(negate(rule[0]))
            if rule[0][0] != '-':
                sudokunumbers.append(rule[0])
            removeClauses(rule[0],sudokurules)
            shortenClauses(rule[0],sudokurules)
    
    for rule in sudokurules:
        if len(rule) == 1:
            check_delete_UnitLiterals(sudokurules,domain,sudokunumbers)

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

    check_delete_UnitLiterals(sudokurules,domain,sudokunumbers)

    # Remove from the domain P and -P
    literal_to_use = domain.pop(0)
    if negate(literal_to_use) in domain : domain.remove(negate(literal_to_use))
    
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

    # First check for unitLiterals 
    check_delete_UnitLiterals(sudokurules,domain,sudokunumbers)

    if not sudokurules:
        print(sudokunumbers)
    else:
        back_list = copy.deepcopy(sudokurules)
        back_sudoNumbers = copy.deepcopy(sudokunumbers)

        domain.sort()
        literal_to_use = domain.pop(0)
        if negate(literal_to_use) in domain :domain.remove(negate(literal_to_use))

        if not dpll_2(sudokurules,literal_to_use,domain,sudokunumbers):
            dpll_2(back_list,negate(literal_to_use),domain,back_sudoNumbers)


