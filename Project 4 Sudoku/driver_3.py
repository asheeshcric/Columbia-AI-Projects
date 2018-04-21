import copy
import itertools
import queue
import sys


def select_unassigned_variable(sudoku_assign, sudoku_domain):
    # Random large number
    large_random_number = 100
    for row in 'ABCDEFGHI':
        for col in '123456789':
            if sudoku_assign[row + col] == 0:  # Consider only unassigned variables
                value = sudoku_domain[row + col]
                if len(value) < large_random_number:
                    large_random_number = len(value)
                    chosen_key = row + col
    return chosen_key


def check_consistency(sudoku_assign, chosen_key, val):
    global sudoku_constraint

    constraint_list = sudoku_constraint[chosen_key]
    for constraint in constraint_list:
        if val == sudoku_assign[constraint[1]]:
            return False
    return True


def check_inference(sudoku_assign, sudoku_domain, chosenKey, value):
    # Forward checking implemented using this function

    global sudoku_constraint

    constraintList = sudoku_constraint[chosenKey]
    for constraint in constraintList:
        checkKey = constraint[1]
        # Only check for assigned variables
        if sudoku_assign[checkKey] == 0:
            if value in sudoku_domain[checkKey]:
                sudoku_domain[checkKey].remove(value)
            if not sudoku_domain[checkKey]:
                return (False, sudoku_assign, sudoku_domain)
    return (True, sudoku_assign, sudoku_domain)


def back_track_search(sudoku_assign, sudoku_domain):
    if all(value > 0 for key, value in sudoku_assign.items()):
        return (True, sudoku_assign, sudoku_domain)
    chosen_key = select_unassigned_variable(sudoku_assign, sudoku_domain)
    for value in sudoku_domain[chosen_key]:
        if check_consistency(sudoku_assign, chosen_key, value):
            sudoku_assign_new = copy.deepcopy(sudoku_assign)
            sudoku_domain_new = copy.deepcopy(sudoku_domain)
            sudoku_assign_new[chosen_key] = value
            sudoku_domain_new[chosen_key] = [value]
            result_inference = check_inference(sudoku_assign_new, sudoku_domain_new, chosen_key, value)
            if result_inference[0] == True:
                result_bts = back_track_search(result_inference[1], result_inference[2])
                if result_bts[0] == True:
                    return result_bts
    return (False, sudoku_assign, sudoku_domain)


def make_assign(sudoku_assign, sudoku_domain):
    for key, value in sudoku_domain.items():
        if len(value) == 1:
            sudoku_assign[key] = value[0]
    return sudoku_assign


def get_neighbors(Xi):
    global sudoku_constraint
    neighbours = [Xk for Xi, Xk in sudoku_constraint[Xi]]
    return neighbours


def revert(sudoku_domain, Xi, Xj):
    reverted = False
    for x in sudoku_domain[Xi]:
        if not any(y != x for y in sudoku_domain[Xj]):
            sudoku_domain[Xi].remove(x)
            reverted = True
    return reverted


def AC3(sudoku_assign, sudoku_domain, constraint_list):
    temp_queue = queue.Queue()
    for constraint in constraint_list:
        temp_queue.put(constraint)
    while not temp_queue.empty():
        Xi, Xj = temp_queue.get()
        if revert(sudoku_domain, Xi, Xj):
            if not sudoku_domain[Xi]:
                return (False, sudoku_assign, sudoku_domain)
            for Xk in get_neighbors(Xi):
                temp_queue.put((Xk, Xi))
    sudoku_assign = make_assign(sudoku_assign, sudoku_domain)
    return (True, sudoku_assign, sudoku_domain)


def initialize_sudoku_csp():
    global sudoku_constraint

    # Create domain values
    domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # Create sudoku board containing all the variables
    sudoku_board = [['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'],['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9'],
                    ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9'],
                    ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9'],['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9'],
                    ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9'],['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9'],
                    ['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9']]
    sudoku_domain = {key: list(domain) for row in sudoku_board for key in row}
    sudoku_assign = {key: 0 for key in sudoku_domain}

    constraint_list = []
    for row in sudoku_board:
        constraint_list = constraint_list + list(itertools.permutations(row, 2))
    sudokuBoardT = list(map(list, zip(*sudoku_board)))

    for col in sudokuBoardT:
        constraint_list = constraint_list + list(itertools.permutations(col, 2))

    for row in [0, 3, 6]:
        for col in [0, 3, 6]:
            box = [val for row in sudoku_board[row:row + 3] for val in row[col:col + 3]]
            constraint_list = constraint_list + list(itertools.permutations(box, 2))
    constraint_list = list(set(constraint_list))
    sudoku_constraint = {key: list([]) for key in sudoku_domain}

    for value in constraint_list:
        sudoku_constraint[value[0]].append(value)

    return sudoku_assign, sudoku_domain, constraint_list


def solve_sudoku(initial_sudoku):
    sudoku_assign, sudoku_domain, constraint_list = initialize_sudoku_csp()

    pos = -1
    for j in 'ABCDEFGHI':
        for i in '123456789':
            key = j + i
            pos = pos + 1
            sudoku_assign[key] = int(initial_sudoku[pos])
            if int(initial_sudoku[pos]) != 0:
                sudoku_domain[key] = [int(initial_sudoku[pos])]

    # Try to solve the board with AC3 Algorithm first
    status, sudoku_assign_new, sudoku_domain_new = AC3(copy.deepcopy(sudoku_assign), copy.deepcopy(sudoku_domain),
                                                     copy.deepcopy(constraint_list))
    method_name = 'AC3'
    if status == True:
        sudoku_assign = sudoku_assign_new
        sudoku_domain = sudoku_domain_new
    if all(value > 0 for key, value in sudoku_assign_new.items()):
        # Solved using AC3 Algorithm
        pass
    else:
        # AC3 failed. So, we have to use BTS to solve the board
        status, sudoku_assign, sudoku_domain = back_track_search(copy.deepcopy(sudoku_assign),
                                                              copy.deepcopy(sudoku_domain))
        method_name = 'BTS'

    # Make final sudoku string on completion of the game
    final_sudoku_string = ''
    for m in 'ABCDEFGHI':
        for n in '123456789':
            k = m + n
            final_sudoku_string = final_sudoku_string + str(sudoku_assign[k])

    # Print the output of the game to a file named 'output.txt'
    print(final_sudoku_string + ' ' + method_name)
    file = open('output.txt', 'w')
    file.write(final_sudoku_string + ' ' + method_name)
    file.close()


if __name__ == '__main__':
    solve_sudoku(sys.argv[1])
