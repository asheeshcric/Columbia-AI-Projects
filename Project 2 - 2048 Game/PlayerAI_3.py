from BaseAI_3 import BaseAI

import time
import numpy as np
import itertools

player_allowance = 0.02
player_time_limit = 0.2 - player_allowance
player_prev_time = 0
player_alarm = False
tile_values = [2, 4]
max_depth = 4


class PlayerAI(BaseAI):
    def getMove(self, grid):
        global player_time_limit
        global player_prev_time
        global player_alarm
        player_alarm = False
        player_prev_time = time.clock()
        grid.depth = 0
        (child, _) = max_play(grid, -np.inf, np.inf)
        return child


def max_play(grid, alpha, beta):
    global player_time_limit
    global player_prev_time
    global player_alarm
    if terminal_test(grid):
        return (None, evaluate_utility(grid))

    (_, max_utility) = (None, -np.inf)

    moves = grid.getAvailableMoves()

    for move in moves:
        child_grid = grid.clone()
        child_grid.depth = grid.depth + 1  # Increment the depth of node
        child_grid.move(move)
        (_, utility) = min_play(child_grid, alpha, beta)

        if utility > max_utility:
            (max_move, max_utility) = (move, utility)

        if max_utility >= beta:
            break

        if max_utility > alpha:
            alpha = max_utility

        if player_alarm or player_update_alarm():
            break

    return max_move, max_utility


def min_play(grid, alpha, beta):
    global player_time_limit
    global player_prev_time
    global player_alarm
    if terminal_test(grid):
        return (None, evaluate_utility(grid))

    (_, min_utility) = (None, np.inf)

    cells = grid.getAvailableCells()

    for cell_value in tile_values:
        for cell in cells:
            child_grid = grid.clone()
            child_grid.depth = grid.depth + 1  # Increment the depth of node
            child_grid.insertTile(cell, cell_value)
            (_, utility) = max_play(child_grid, alpha, beta)

            if utility < min_utility:
                (min_move, min_utility) = (cell, utility)

            if min_utility <= alpha:
                break

            if min_utility < beta:
                beta = min_utility

            if player_alarm or player_update_alarm():
                break

        if player_alarm or player_update_alarm():
            break

    return min_move, min_utility


def player_update_alarm():
    global player_time_limit
    global player_prev_time
    global player_alarm
    if (time.clock() - player_prev_time) >= player_time_limit:
        player_alarm = True
    else:
        player_alarm = False
    return player_alarm


def terminal_test(grid):
    if grid.depth >= max_depth or (not grid.canMove()):
        return True
    else:
        return False


def abs_diff(x, y):
    return abs(x - y)


def evaluate_utility(grid):
    tot_cells = len(grid.getAvailableCells())
    k1 = tot_cells / (grid.size * grid.size)

    tot_diff = 0
    for i in range(grid.size - 1):
        tot_diff += sum(list(map(abs_diff, grid.map[i], grid.map[i + 1])))
    for i in range(grid.size):
        tot_diff += sum(list(map(abs_diff, grid.map[i][:-1], grid.map[i][1:])))

    tot_cells = sum(itertools.chain.from_iterable(grid.map))
    k2 = tot_diff / (2 * tot_cells)

    return k1 - k2
