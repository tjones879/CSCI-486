from collections import namedtuple
from copy import deepcopy
import random

MARK_O = -100
MARK_NONE = 0
MARK_X = 100

MAX_SIZE = 3

Move = namedtuple('Move', ['row', 'col', 'mark'])
State = namedtuple('State', ['board', 'turns'])


def initState(size):
    board = list()
    for r in range(size):
        board.append([MARK_NONE for x in range(size)])
    return State(board, 0)


def getMoves(board):
    board = board[0]
    rows = len(board)
    cols = len(board[0])
    moves = list()
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == MARK_NONE:
                moves.append((row, col, MARK_NONE))
    return moves


def winIndices(size):
    for r in range(size):
        yield [(r, c) for c in range(size)]
    for c in range(size):
        yield [(r, c) for r in range(size)]
    yield [(i, i) for i in range(size)]
    yield [(i, size - 1 - i) for i in range(size)]


def endScore(board) -> (int, bool):
    turns = board[1]
    board = board[0]
    cols = len(board)

    for indexes in winIndices(cols):
        first = board[indexes[0][0]][indexes[0][1]]
        if all(board[r][c] == first for r, c in indexes):
            if first is not MARK_NONE:
                return (first, True)

    if turns == 9:
        return (MARK_NONE, True)

    return (MARK_NONE, False)


def nextState(state: State, move: Move) -> State:
    board = deepcopy(state[0])
    if move[0] < 0 or move[0] >= MAX_SIZE:
        print("ROW < 0")
        'return error'
    if move[1] < 0 or move[1] >= MAX_SIZE:
        print("COL < 0")
        'return error'
    if board[move[0]][move[1]] != MARK_NONE:
        print("MARK != NONE")
        'return error'
    board[move[0]][move[1]] = move[2]
    return (board, state[1] + 1)


def heuristic(game, player):
    # Only check lines that are winnable by either player
    size = len(game)
    options = list()
    for indexes in winIndices(size):
        line = [(game[r][c], (r, c)) for r, c in indexes]
        if len(set(line[0])) < 3:
            options.append(line)

    # Create a set of possible places
    # For each possible place check the following:
    # --> Assign max value if it causes win & return
    # --> Assign half max value if blocks immediate win
    # --> Add score according to how much it strengthens all included lines
    # --> --> (Cannot add more than 1/2 max, each line is 1/6 of max)


def minimax(game, depth, player):
    if depth is 0:
        return heuristic(game, player)
    end = endScore(game)
    if end[1]:
        return MARK_NONE, end[0]

    if player is MARK_X:
        bestScore = -5000
        for move in getMoves(game):
            clone = nextState(game, Move(move[0], move[1], player))
            _, value = minimax(clone, 1, player * -1)
            # Break out early if we've found a best case
            if value == MARK_X:
                bestMove = move
                bestScore = value
                break
            if value > bestScore:
                bestMove = move
                bestScore = value
    else:
        bestScore = 5000
        for move in getMoves(game):
            clone = nextState(game, Move(move[0], move[1], player))
            _, value = minimax(clone, 1, player * -1)
            # Break out early if we've found a best case
            if value == MARK_O:
                bestMove = move
                bestScore = value
                break
            if value < bestScore:
                bestMove = move
                bestScore = value
    bestMove = (bestMove[0], bestMove[1], player)
    return bestMove, bestScore


def randomAgent(game, player):
    moves = getMoves(game)
    move = random.choice(moves)
    move = Move(move[0], move[1], player)
    return move


def playGame():
    game = initState(MAX_SIZE)
    player = MARK_X
    while True:
        move, score = minimax(game, 1, player)

        player *= -1
        print(move)
        game = nextState(game, move)
        print(game)
        if endScore(game)[1]:
            print("GAME OVER (SCORE):", endScore(game)[0])
            break


playGame()
