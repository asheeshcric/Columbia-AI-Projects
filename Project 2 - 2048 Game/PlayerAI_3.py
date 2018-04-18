import time
import math

from random import randint
from BaseAI_3 import BaseAI


class PlayerAI(BaseAI):
    def __init__(self):
        self.timeLimit = 0.2
        self.startTime = None

    def score(self, grid):
        smoothWeight = 0.1
        emptyWeight = 2.7
        maxWeight = 1.0
        monWeight = 1.0

        smoothValue = self.check_smoothness(grid)
        availableCells = len(grid.getAvailableCells())
        if availableCells > 0:
            emptyValue = math.log(availableCells)
        else:
            emptyValue = -100000
        maxValue = math.log(grid.getMaxTile(), 2)
        monValue = self.check_monaticity(grid)

        heuristicValue = smoothWeight * smoothValue + maxWeight * maxValue + emptyWeight * emptyValue + monWeight * monValue

        return heuristicValue

    def check_smoothness(self, grid):

        directionVectors = ((1, 0), (0, 1))
        smoothScore = 0.0
        for x in range(grid.size):
            for y in range(grid.size):
                if grid.map[x][y] != 0:
                    for vector in directionVectors:
                        for d in range(1, grid.size + 1):
                            x_n = x + vector[0] * d
                            y_n = y + vector[1] * d
                            if x_n < 0 or x_n >= grid.size or y_n < 0 or y_n >= grid.size:
                                break
                            if grid.map[x_n][y_n] != 0:
                                smoothScore -= abs(math.log(grid.map[x][y], 2) - math.log(grid.map[x_n][y_n], 2))
                                break
        return smoothScore

    def check_monaticity(self, grid):
        total = [0.0 for i in range(grid.size)]

        for x in range(grid.size):
            current = 0
            next = current + 1
            while next < 4:
                while next < 4 and grid.map[x][next] != 0:
                    next += 1
                if next >= 4: next -= 1
                if grid.map[x][current] != 0:
                    currentValue = math.log(grid.map[x][current], 2)
                else:
                    currentValue = 0

                if grid.map[x][next] != 0:
                    nextValue = math.log(grid.map[x][next], 2)
                else:
                    nextValue = 0

                if currentValue > nextValue:
                    total[0] += nextValue - currentValue
                elif nextValue > currentValue:
                    total[1] += currentValue - nextValue

                current = next
                next += 1

        # Left / Right direction
        for y in range(grid.size):
            current = 0
            next = current + 1
            while next < 4:
                while next < 4 and grid.map[next][y] != 0:
                    next += 1
                if next >= 4:
                    next -= 1
                if grid.map[current][y] != 0:
                    currentValue = math.log(grid.map[current][y], 2)
                else:
                    currentValue = 0

                if grid.map[next][y] != 0:
                    nextValue = math.log(grid.map[next][y], 2)
                else:
                    nextValue = 0

                if currentValue > nextValue:
                    total[2] += nextValue - currentValue
                elif nextValue > currentValue:
                    total[3] += currentValue - nextValue

                current = next
                next += 1

        return max(total[0], total[1]) + max(total[2], total[3])

    def predict_move(self, grid, n_move):
        gridCopy = grid.clone()
        gridCopy.move(n_move)
        return gridCopy

    def getMove(self, grid):
        # Start time for making a move
        self.startTime = time.clock()

        # Retrieving all the available moves from Grid
        moves = grid.getAvailableMoves()

        if not moves:  # Game ends here
            return None

        # Choosing a random move to begin with
        bestMove = moves[randint(0, len(moves) - 1)]
        bestScore = self.score(self.predict_move(grid, bestMove))

        try:
            depth = 1
            while True:
                score, move = self.alpha_beta(grid, depth)
                if score > bestScore:
                    bestMove = move
                    bestScore = score
                depth += 1

        except Exception:
            return bestMove

    def alpha_beta(self, grid, depth, alpha=float("-inf"), beta=float("inf"), maxPlayer=True):

        if time.clock() - self.startTime >= self.timeLimit:
            raise Exception

        if depth == 0:
            return self.score(grid), None

        # now we need to go over all the legal moves and find best
        bestScore = float("-inf") if maxPlayer else float("inf")
        bestMove = None

        if maxPlayer:
            # Estimating the maximizing move to play for us
            moves = grid.getAvailableMoves()
            if not moves:
                return self.score(grid), None

            for move in moves:
                nextGame = self.predict_move(grid, move)

                score, _ = self.alpha_beta(nextGame, depth - 1, alpha, beta, not maxPlayer)

                if score >= bestScore:
                    bestScore = score
                    bestMove = move

                if bestScore >= beta:
                    break

                alpha = max(alpha, bestScore)
        else:
            # Assuming that the Computer makes the most minimizing move for us
            availableCells = grid.getAvailableCells()
            if not availableCells:
                return self.score(grid), None
            for cell in availableCells:
                for tile_val in [2, 4]:
                    nextGame = grid.clone()
                    nextGame.setCellValue(cell, tile_val)
                    score, _ = self.alpha_beta(nextGame, depth - 1, alpha, beta, not maxPlayer)

                    if score <= bestScore:
                        bestScore = score
                        bestMove = None

                    if bestScore <= alpha:
                        break

                    beta = min(beta, bestScore)

        return bestScore, bestMove
