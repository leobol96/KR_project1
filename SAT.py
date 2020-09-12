import copy
import sys
import time


# Read the sudoku
def read_sudoku(sudoku_filename):
    sudoku = open(sudoku_filename, "r")
    for number in sudoku:
        end_number = number.split()
        sudokunumbers.append(end_number[0])


# Read the rules in DIMACS format
def read_rules(rules_filename):
    rules = open(rules_filename, "r")
    for row in rules:
        if row[0] == "p":
            pass
        else:
            splitrow = row.split()
            splitrow.pop()
            sudokurules.append(splitrow)


# Negate the literal passed as a parameter
def negate(literal_to_negate):
    if literal_to_negate[0] == '-':
        return literal_to_negate[1:]
    else:
        return '-' + literal_to_negate


# Write the file in 'Name of the file in input' + '.out' + 'txt'
def writefile(sudoku_out_name, result):
    output = open(sudoku_out_name.replace('.txt', '') + '.out.txt', 'w')
    if result:
        for idx, number in enumerate(result):
            output.write(number + ' 0\n')
    output.close()


# Remove clauses from the sudokurules using the literal passed as a parameter
def remove_clauses(literal, sudokurules):
    # The symbol [:] it 's used to work with a copy of the original element. Deleting objects where you are working
    # could cause problems
    for rule in sudokurules[:]:
        for number in rule[:]:
            if isinstance(literal, list):
                if number in literal:
                    sudokurules.remove(rule)
                    break
            else:
                # For the strings (397 in -397) is true, this behaviour is not valid for lists
                if number == literal:
                    sudokurules.remove(rule)
                    break


# Shorten clauses from the sudokurules using the literal passed as a parameter
def shorten_clauses(literal, sudokurules):
    # The symbol [:] it 's used to work with a copy of the original element. Deleting objects where you are working
    # could cause problems
    for rule in sudokurules[:]:
        for number in rule[:]:
            if isinstance(literal, list):
                if negate(number) in literal:
                    rule.remove(number)
            else:
                # For the strings (397 in -397) is true, this behaviour is not valid for lists
                if negate(number) == literal:
                    rule.remove(number)


# Give the literal using the version passed as a parameter
def give_literal(sudokurules):
    if version == '-S2':
        return dlis_heuristic(sudokurules)
    elif version == '-S3':
        return cul_heuristic(sudokurules)
    else:
        return sudokurules[0][0]


# Create unit literals heuristic algorithm
def cul_heuristic(sudokurules):
    idx_len_clauses = 2
    while True:
        for rule in sudokurules:
            if len(rule) == idx_len_clauses:
                return rule[0]
        idx_len_clauses += 1


#Doesn't work
def dlis_heuristic(sudokurules):
    hashmap = {}
    for rule in sudokurules:
        for literal in rule:
            hashmap[literal] = hashmap.get(literal, 0) + 1

    n_time = 0
    for key in hashmap:
        if hashmap.get(key) > n_time:
            to_return = key
            n_time = hashmap.get(key)

    return to_return


def check_delete_unit_literals(sudokurules, sudokunumbers):
    number_unit_literals = 0
    literal_list = []
    for rule in sudokurules[:]:
        if len(rule) == 1:
            #print('Rule:', rule)
            #print(sudokurules)
            #print('________________')
            number_unit_literals += 1
            if rule[0][0] != '-':
                if rule[0] not in sudokunumbers: sudokunumbers.append(rule[0])
            if rule[0] not in literal_list: literal_list.append(rule[0])

    if literal_list :
        remove_clauses(literal_list, sudokurules)
        shorten_clauses(literal_list, sudokurules)

    if number_unit_literals > 1 and [] not in sudokurules:
        check_delete_unit_literals(sudokurules, sudokunumbers)


# Implementation of the DP algorithm
def dpll_2(sudokurules, literal, sudokunumbers):

    remove_clauses(literal, sudokurules)
    shorten_clauses(literal, sudokurules)
    check_delete_unit_literals(sudokurules, sudokunumbers)

    if not sudokurules:

        if literal[0] != '-' and literal not in sudokunumbers:
            sudokunumbers.append(literal)

        global result
        sudokunumbers.sort()
        result = sudokunumbers[:]
        return True
    if [] in sudokurules:
        return False

    literal_to_use = give_literal(sudokurules)

    back_sudoku_rules = copy.deepcopy(sudokurules)
    back_sudoku_number = copy.deepcopy(sudokunumbers)

    if literal_to_use[0] != '-' and literal_to_use not in sudokunumbers:
        sudokunumbers.append(literal_to_use)

    if dpll_2(sudokurules, literal_to_use, sudokunumbers):
        return True
    else:
        if (negate(literal_to_use))[0] != '-' and negate(literal_to_use) not in sudokunumbers:
            back_sudoku_number.append(negate(literal_to_use))
        dpll_2(back_sudoku_rules, negate(literal_to_use), back_sudoku_number)


if __name__ == "__main__":

    if len(sys.argv) < 4:
        print("Please insert:\narg1: Name of the sudoku file\narg2: Name of the rules file")
    else:
        start_time = time.time()
        print("1.0: Start")
        # Numbers used to solve the sudoku
        sudokunumbers = []
        # Rules used to solve the sudoku in Dimacs format
        sudokurules = []
        # Result
        result = []
        # Version of the algorithm
        version = sys.argv[1]

        print("2.0: Reading the sudoku")
        sudokuname = sys.argv[2]
        read_sudoku(sudokuname)
        print("3.0: Reading the rules")
        rulename = sys.argv[3]
        read_rules(rulename)

        print("5.0: Starting solving")
        print("5.1: Iterating on given numbers")
        remove_clauses(sudokunumbers, sudokurules)
        shorten_clauses(sudokunumbers, sudokurules)
        check_delete_unit_literals(sudokurules, sudokunumbers)

        if not sudokurules:
            result = sudokunumbers[:]
            result.sort()
        else:
            print("5.2: Starting the dpll core")

            literal_to_use = give_literal(sudokurules)
            back_list = copy.deepcopy(sudokurules)
            back_sudoNumbers = copy.deepcopy(sudokunumbers)

            if literal_to_use[0] != '-' and literal_to_use not in sudokunumbers:
                sudokunumbers.append(literal_to_use)

            if not dpll_2(sudokurules, literal_to_use, sudokunumbers):
                if (negate(literal_to_use))[0] != '-' and negate(literal_to_use) not in sudokunumbers:
                    back_sudoNumbers.append(negate(literal_to_use))
                dpll_2(back_list, negate(literal_to_use), back_sudoNumbers)

        print("6.0: Finish")
        print("Total time in Seconds :" + format(time.time() - start_time, '.2f'))

        print("7.0: Writing the result")
        writefile(sudokuname, result)
