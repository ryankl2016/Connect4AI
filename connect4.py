import random
import sys

BOARD_HEIGHT = 6
BOARD_WIDTH = 7

class Game():
    def __init__(self):
        self.board = Board()

    # returns new grid after dropping chip or False if not possible
    def drop(self, col, chip, grid):

        # asserts col in bound and chip is only 'X' or 'O'
        valid_move = col < BOARD_WIDTH and col >= 0 and (chip == 'X' or chip == 'O')
        assert valid_move

        # can't move in this column
        if grid[0][col] != '_':
            return False

        # drop chip
        row = BOARD_HEIGHT - 1
        while row > -1 and grid[row][col] != '_':
            row -= 1
        new_grid = copyGrid(grid)
        new_grid[row][col] = chip
        return new_grid

    # sets game board to new grid after move
    def move(self, col, chip, grid):
        new_grid = self.drop(col, chip, grid)
        if new_grid:
            self.board.grid = new_grid

    # returns player and opponent
    def getPlayer(self, chip):
        if chip == 'X':
            other = 'O'
        else:
            other = 'X'
        return chip, other

    # returns highest heuristic score steps ahead
    def getBestScore(self, chip, grid, steps, minmaxVal = None):

        player, opponent = self.getPlayer(chip) # keeps player and opponent consistent per turn
        turn = [[player, max, -50, -1], [opponent, min, 50, 1]][steps % 2] # players turn if steps even, opponent o.w.
        _, lastMover = self.getPlayer(turn[0]) # lastMover == player who last moved

        if isWinner(lastMover, grid): # if last move caused win, return max or min rewards
            if lastMover == player:
                return 100
            else:
                return -100

        if steps == 5: # return heuristic value
            return almostFours(player, grid) - almostFours(opponent, grid)

        bestScore = turn[2]
        comparator = turn[1]
        temp = None
        mode = turn[3]

        for i in range(0, BOARD_WIDTH):

            newGrid = self.drop(i, turn[0], grid)

            if newGrid: # if move succeeded

                newScore = self.getBestScore(player, newGrid, steps + 1, temp)
                #print(steps, turn[0], i+1, newScore)
                # minimax prune
                if minmaxVal != None and (newScore + mode) == comparator(newScore + mode, minmaxVal):
                    # print(steps, turn[0], i+1, newScore)
                    return newScore
                # if (newScore == 100 and comparator == max) or (newScore == -100 and comparator == min):
                #     return newScore
                # set new running best score
                if newScore == comparator(newScore, bestScore):
                    bestScore = newScore
                    temp = newScore

        return bestScore

    # computer player moves always maximizing player score and minimizing opponent
    def CP_move(self, chip, grid):

        bestMoves = [] # list of best moves
        bestScore = -100 # running max score
        temp = None # temp value for alpha-beta pruning

        for i in range(0, BOARD_WIDTH):
        # for i in range(3, 4):
            newGrid = self.drop(i, chip, grid)

            if newGrid: # if dropping chip in col i succeeded

                newScore = self.getBestScore(chip, newGrid, 1, temp)
                # print(i + 1, newScore)
                if newScore == bestScore: # if new move is equally good as best moves
                    bestMoves.append(i)

                elif newScore > bestScore: # if new move is a best move
                    bestScore = newScore
                    bestMoves = [i]
                    temp = newScore

        if len(bestMoves) == 0:
            print("Game Over")
            return

        # if numerous best moves, choose random best move
        move = bestMoves[random.randint(0, len(bestMoves) - 1)]
        print('CP plays ' + str(move + 1))
        self.move(move, chip, grid)
        return

# contains grid of current game
class Board():
    def __init__(self):
        self.grid = []
        for i in range(0, BOARD_HEIGHT):
            self.grid.append(['_'] * BOARD_WIDTH)

# returns number of potential winning rows for player playing chip
def almostFours(chip, grid):

    # returns True if potential four in a row exists in positions
    def three_exist(chip, positions):
        cnt = 0
        blanks = 0
        for pos in positions:
            if chip == pos:
                cnt += 1
            elif pos == '_':
                blanks += 1
        return cnt == 3 and blanks == 1

    # returns True if potential four in a row exists starting at r, c
    def three_in_row(r, c, grid):

        if r + 3 < BOARD_HEIGHT: # checks if row is in bound
            if three_exist(chip, [grid[r][c], grid[r + 1][c], grid[r + 2][c], grid[r + 3][c]]):
                return True
            if c >= 3:
                if three_exist(chip, [grid[r][c], grid[r + 1][c - 1], grid[r + 2][c - 2], grid[r + 3][c - 3]]):
                    return True
            if c + 3 < BOARD_WIDTH:
                if three_exist(chip, [grid[r][c], grid[r + 1][c + 1], grid[r + 2][c + 2], grid[r + 3][c + 3]]):
                    return True

        if c + 3 < BOARD_WIDTH: # checks if col is in bound
            if three_exist(chip, [grid[r][c], grid[r][c + 1], grid[r][c + 2], grid[r][c + 3]]):
                return True

        return False

    threes = 0
    for r in range(0, BOARD_HEIGHT):
        for c in range(0, BOARD_WIDTH):
            if three_in_row(r, c, grid):
                threes += 1

    return threes

# checks if player who plays chip has won
def isWinner(chip, grid):

    # checks if four in a row exists in southwest, southeast, east, or south direction
    def four_in_row(r, c, grid):
        if r + 3 < BOARD_HEIGHT:
            if grid[r][c] == grid[r + 1][c] == grid[r + 2][c] == grid[r + 3][c]:
                return True
            if c >= 3:
                if grid[r][c] == grid[r + 1][c - 1] == grid[r + 2][c - 2] == grid[r + 3][c - 3]:
                    return True
            if c + 3 < BOARD_WIDTH:
                if grid[r][c] == grid[r + 1][c + 1] == grid[r + 2][c + 2] == grid[r + 3][c + 3]:
                    return True
        if c + 3 < BOARD_WIDTH:
            if grid[r][c] == grid[r][c + 1] == grid[r][c + 2] == grid[r][c + 3]:
                return True
        return False

    # iterate through all positions
    for r in range(0, BOARD_HEIGHT):
        for c in range(0, BOARD_WIDTH):
            if grid[r][c] == chip:
                if four_in_row(r, c, grid):
                    return True

    return False

# creates deep copy of grid
def copyGrid(grid):
    new_grid = [row[:] for row in grid]
    return new_grid

# prints game board
def printBoard(board):
    print([str(col) for col in range(1, BOARD_WIDTH + 1)])
    for row in board.grid:
        print(row)

# creates a random Board of chips
def createRandomBoard():
    board = Board()
    grid = []
    for i in range(0, BOARD_HEIGHT):
        grid.append(['X' if random.randint(1, 2) == 1 else 'O' for j in range(0, BOARD_WIDTH)])
    board.grid = grid
    return board

# tests createRandomBoard, printBoard, and isWinner
def test():
    for i in range(0, 5):
        board = createRandomBoard()
        printBoard(board)
        game = Game()
        print(isWinner('X', board.grid))
        print(isWinner('O', board.grid))

# outputs game played by random moves
def test1():
    game = Game()
    players = ['X', 'O']
    for i in range(0, 26):
        col = random.randint(0, 6)
        chip = players[i % 2]
        grid = game.board.grid
        game.move(col, chip, grid)
    printBoard(game.board)

# test outputs mock game played by two computers
def test2():
    game = Game()
    i = BOARD_WIDTH * BOARD_HEIGHT + 1
    players = ['X', 'O']
    while i > 0:
        game.CP_move(players[i % 2], game.board.grid)
        printBoard(game.board)
        print('\n')
        if isWinner(players[i % 2], game.board.grid):
            print(players[i % 2] + ' wins!')
            if i % 2 == 0:
                return [1, 0]
            else:
                return [0, 1]
            break
        i -= 1
    return [0, 0]

# test allows user to play against computer in terminal
def test3():
    game = Game()
    i = BOARD_WIDTH * BOARD_HEIGHT + 1
    players = ['O', 'X']
    player = input('Player 0 or Player 1? [0/1]')
    possible_moves = [move for move in range(1, BOARD_WIDTH + 1)]

    while player != 1 and player != 0:
        player = input('Player 0 or Player 1? [0/1]')

    while i > 0:
        printBoard(game.board)
        if i % 2 == player:
            game.CP_move(players[i % 2], game.board.grid)
        else:
            col = input('Drop in column:')
            while col not in possible_moves:
                col = input('Drop in column:')

            game.move(col - 1, players[i % 2], game.board.grid)
        print('\n')
        if isWinner(players[i % 2], game.board.grid):
            printBoard(game.board)
            print(players[i % 2] + ' wins!')
            break
        i -= 1

    y = 'y'
    n = 'n'
    rematch = input('Play again? [y/n]')
    while rematch != 'y' and rematch != 'n':
        rematch = input('Play again? [y/n]')
    if rematch == 'y':
        test3()
    else:
        return



def test4():
    game = Game()
    game.board.grid = [ ['_', '_', '_', '_', '_', '_', '_'],
                        ['_', '_', '_', '_', '_', '_', '_'],
                        ['_', '_', 'X', '_', '_', '_', '_'],
                        ['_', '_', 'O', '_', '_', '_', '_'],
                        ['O', 'X', 'O', 'O', 'X', '_', 'X'],
                        ['X', 'O', 'O', 'X', 'O', 'X', 'X'] ]
    i = 30
    players = ['O', 'X']
    player = 0
    possible_moves = [move for move in range(1, BOARD_WIDTH + 1)]
    while i > 0:
        printBoard(game.board)
        if i % 2 == player:
            game.CP_move(players[i % 2], game.board.grid)
        else:
            col = input('Drop in column:')
            while col not in possible_moves:
                col = input('Drop in column:')

            game.move(col - 1, players[i % 2], game.board.grid)
        print('\n')
        if isWinner(players[i % 2], game.board.grid):
            printBoard(game.board)
            print(players[i % 2] + ' wins!')
            break
        i -= 1

    y = 'y'
    n = 'n'
    rematch = input('Play again? [y/n]')
    while rematch != 'y' and rematch != 'n':
        rematch = input('Play again? [y/n]')
    if rematch == 'y':
        test3()
    else:
        return


def test5():
    scoreX, scoreO = 0, 0
    rounds = 50
    for i in range(0, rounds):
        game = test2()
        scoreX += game[0]
        scoreO += game[1]
        print(scoreX, scoreO)


test3()
