"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    Xc = 0
    Oc = 0
    for row in board:
        Xc += row.count(X)
        Oc += row.count(O)
    if Xc <= Oc:
        return X
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    result_a = set()
    for row_index, row in enumerate(board):
        for column_index, item in enumerate(row):
            if item == EMPTY:
                result_a.add((row_index, column_index))
    return result_a


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception
    else:
        c_board = deepcopy(board)
        i, j = action
        playing = player(board)
        c_board[i][j] = playing
        return c_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == X and board[0][1] == X and board[0][2] == X:
        return X
    if board[1][0] == X and board[1][1] == X and board[1][2] == X:
        return X
    if board[2][0] == X and board[2][1] == X and board[2][2] == X:
        return X
    if board[0][0] == X and board[1][0] == X and board[2][0] == X:
        return X
    if board[0][1] == X and board[1][1] == X and board[2][1] == X:
        return X
    if board[0][2] == X and board[1][2] == X and board[2][2] == X:
        return X
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X
    if board[2][0] == X and board[1][1] == X and board[0][2] == X:
        return X
    if board[0][0] == O and board[0][1] == O and board[0][2] == O:
        return O
    if board[1][0] == O and board[1][1] == O and board[1][2] == O:
        return O
    if board[2][0] == O and board[2][1] == O and board[2][2] == O:
        return O
    if board[0][0] == O and board[1][0] == O and board[2][0] == O:
        return O
    if board[0][1] == O and board[1][1] == O and board[2][1] == O:
        return O
    if board[0][2] == O and board[1][2] == O and board[2][2] == O:
        return O
    if board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O
    if board[2][0] == O and board[1][1] == O and board[0][2] == O:
        return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    for row in board:
        for each in row:
            if each == EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def X_value(board):
    result_X = ()
    if terminal(board):
        return utility(board), result_X
    a = -math.inf
    for action in actions(board):
        b = max(a, O_value(result(board, action))[0])
        if b > a:
            a = b
            result_X = action
    return a, result_X

def O_value(board):
    result_O = ()
    if terminal(board):
        return utility(board), result_O
    a = math.inf
    for action in actions(board):
        b = min(a, X_value(result(board, action))[0])
        if b < a:
            a = b
            result_O = action
    return a, result_O

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        if player(board) == X:
            action = X_value(board)[1]
            return action
        else:
            action = O_value(board)[1]
            return action

