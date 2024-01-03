"""
Tic Tac Toe Player
"""

import math

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
    If inital_state() (game has just started), then returns X.
    """

    # if the board is empty, return X
    if board == initial_state(): 
        return X

    # initialize counts for X and O
    X_count = 0
    O_count = 0

    # loop through the rows and columns in the board and add to X and O count
    for row in board:
        for col in row:
            if col == X:
                X_count+=1
            elif col == O:
                O_count+=1
    
    # if X is more, return O; else return X
    if X_count > O_count:
        return O
    else: 
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # create set of moves
    moves = set()

    # loop through rows and columns using enumerate to keep track of the index,
    # if the column is empty, add the index into the moves set.
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if col == EMPTY:
                moves.add((i, j))
    
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action] != EMPTY:
        raise Exception('Invalid Move!')
    new_board = board.deepcopy()




def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
