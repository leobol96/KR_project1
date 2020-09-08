import copy

def readSudoku():
    Sudoku = open("sudoku-example.txt", "r")
    for number in Sudoku:
        end_number = number.split()
        sudokunumbers.append(end_number[0])

def readRules():
    rules = open("sudoku-rules.txt", "r")
    for row in rules:
        if row[0] == "p":
            pass
        else:
            splitrow = row.split()
            splitrow.pop()
            sudokurules.append(splitrow)

def createDomain(domain):
    for rule in sudokurules:
        for literal in rule:
            if (literal not in domain):
                domain.append(literal)

def removeNumberInSudoku():
    for literal in sudokunumbers:
        removeClauses(literal)
        shortenClauses(literal)

def removeClauses(literal):
    
    global sudokurules
    rule_to_remove = []
    for rule in sudokurules:
        for number in rule:
            if (literal == number):
                rule_to_remove.append(rule)

    sudokurules = [x for x in sudokurules if x not in rule_to_remove]
    
def shortenClauses(literal):
    for rule in sudokurules:
        for number in rule:
            if literal[0] == '-':
                if (literal[1:]) == number:
                    rule.remove(number)
            else:
                if ('-' + literal == number):
                    rule.remove(number)  

def chekUnitliters():
    for rule in sudokurules:
        if len(rule) == 1 :
            # positive
            if rule[0][0] != '-':
                sudokunumbers.append(rule[0])
                if rule[0] in domain:
                    domain.remove(rule[0])
                    domain.remove('-' + rule[0])
            # negative
            elif rule[0] in domain:
                domain.remove(rule[0])
                domain.remove(rule[0][1:])

            literal_to_check.append(rule[0])

def checkPureLiters():
    return

def dpll_2(sudokurules,literal):
    
    back_list = copy.deepcopy(sudokurules)
    back_domain = copy.deepcopy(domain)
    back_sudoNumbers = copy.deepcopy(sudokunumbers)
    
    removeClauses(literal)
    shortenClauses(literal)

    if [] in sudokurules: return True
    if not sudokurules : return False

    chekUnitliters()
    checkPureLiters()

    if literal_to_check:
        # run dppl on literal 
        literal_to_use = literal_to_check.pop(0)
        dpll_2(sudokurules,literal_to_use)

if __name__=="__main__":
    sudokunumbers = []
    sudokurules = []
    domain = []
    readSudoku()
    readRules()
    createDomain(domain)

    literal_to_check = copy.deepcopy(sudokunumbers)

    if literal_to_check:
        # run dppl on literal 
        literal_to_use = literal_to_check[0]
        literal_to_check.pop()
        dpll_2(sudokurules,literal_to_use)


