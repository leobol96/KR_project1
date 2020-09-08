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
            if (literal not in sudokunumbers and literal not in domain):
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

def chekUnitliter():
    for rule in sudokurules:
        if len(rule) == 1 and rule[0][0] != '-':
            sudokunumbers.append(rule[0])
            domain.remove(rule[0])
            domain.remove('-' + rule[0])
            removeClauses(rule[0])
            shortenClauses(rule[0])

def dpll_2(sudokurules,literal):
    
    back_list = copy.deepcopy(sudokurules)
    back_domain = copy.deepcopy(domain)
    
    removeClauses(literal)
    shortenClauses(literal)

    if [] in sudokurules: return True
    if not sudokurules : return False

    chekUnitliter()



if __name__=="__main__":
    sudokunumbers = []
    sudokurules = []
    domain = []
    readSudoku()
    readRules()
    createDomain(domain)
    #removeNumberInSudoku()
    #removeClauses('-111')
    shortenClauses('-111')


