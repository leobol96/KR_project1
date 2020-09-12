import copy
import sys
import time


# Read the sudoku
def read_sudoku(sudokuname):
    Sudoku = open(sudokuname, "r")
    for number in Sudoku:
        end_number = number.split()
        sudokunumbers.append(end_number[0])


# Read the rules in DIMACS format
def read_rules(rulename):
    rules = open(rulename, "r")
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


# Create a domain
def create_domain(domain):
    for rule in sudokurules:
        for literal in rule:
            if (literal[0] == '-' and literal not in domain and negate(literal) not in sudokunumbers) or (
                    literal[0] != '-' and literal not in domain and literal not in sudokunumbers):
                domain.append(literal)


# Write the file in 'Name of the file in input' + '.out' + 'txt'
def writefile(sudokuname, result):
    output = open(sudokuname.replace('.txt', '') + '.out.txt', 'w')
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
def give_literal(domain, sudokurules):
    if version == '-S2':
        literal_to_use = dlis_heuristic(sudokurules)
    elif version == '-S3':
        literal_to_use = cul_heuristic(sudokurules)
    else:
        literal_to_use = domain[0]

    # Removing P and -P from the domain
    if literal_to_use in domain: domain.remove(literal_to_use)
    if negate(literal_to_use) in domain: domain.remove(negate(literal_to_use))
    return literal_to_use


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


def check_delete_unit_literals(sudokurules, domain, sudokunumbers):
    number_unit_literals = 0
    literal_list = []
    for rule in sudokurules[:]:
        if len(rule) == 1:
            number_unit_literals += 1
            if rule in domain: domain.remove(rule[0])
            if negate(rule[0]) in domain: domain.remove(negate(rule[0]))
            if rule[0][0] != '-':
                if rule[0] not in sudokunumbers: sudokunumbers.append(rule[0])
            if rule[0] not in literal_list: literal_list.append(rule[0])

    if literal_list:
        remove_clauses(literal_list, sudokurules)
        shorten_clauses(literal_list, sudokurules)

    if number_unit_literals > 1:
        check_delete_unit_literals(sudokurules, domain, sudokunumbers)


# Implementation of the DP algorithm
def dpll_2(sudokurules, literal, domain, sudokunumbers):
    remove_clauses(literal, sudokurules)
    shorten_clauses(literal, sudokurules)
    # The ceck unit literal has to be here, because could creates the
    check_delete_unit_literals(sudokurules, domain, sudokunumbers)

    if not sudokurules:
        global result
        sudokunumbers.sort()
        result = sudokunumbers[:]
        return True
    if [] in sudokurules:
        return False

    literal_to_use = give_literal(domain, sudokurules)

    back_sudoku_rules = copy.copy(sudokurules)
    back_domain = copy.copy(domain)
    back_sudoku_number = copy.copy(sudokunumbers)

    if literal_to_use[0] != '-' and literal_to_use not in sudokunumbers:
        sudokunumbers.append(literal_to_use)

    if dpll_2(sudokurules, literal_to_use, domain, sudokunumbers):
        return True
    else:
        if literal_to_use[0] != '-' and literal_to_use not in sudokunumbers:
            sudokunumbers.append(literal_to_use)
        dpll_2(back_sudoku_rules, negate(literal_to_use), back_domain, back_sudoku_number)


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
        # Domain where pop the numbers
        domain = []
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
        print("4.0: Creating the domain")
        create_domain(domain)

        print("5.0: Starting solving")
        print("5.1: Iterating on given numbers")
        remove_clauses(sudokunumbers, sudokurules)
        shorten_clauses(sudokunumbers, sudokurules)
        check_delete_unit_literals(sudokurules, domain, sudokunumbers)

        if not sudokurules:
            result = sudokunumbers[:]
            result.sort()
        else:
            print("5.2: Starting the dpll core")

            literal_to_use = give_literal(domain, sudokurules)
            back_list = copy.copy(sudokurules)
            back_sudoNumbers = copy.copy(sudokunumbers)

            if literal_to_use[0] != '-' and literal_to_use not in sudokunumbers:
                sudokunumbers.append(literal_to_use)

            if not dpll_2(sudokurules, literal_to_use, domain, sudokunumbers):
                if literal_to_use[0] != '-' and literal_to_use not in sudokunumbers:
                    sudokunumbers.append(literal_to_use)
                dpll_2(back_list, negate(literal_to_use), domain, back_sudoNumbers)

        print("6.0: Finish")
        print("Total time in Seconds :" + format(time.time() - start_time, '.2f'))

        print("7.0: Writing the result")
        writefile(sudokuname, result)
