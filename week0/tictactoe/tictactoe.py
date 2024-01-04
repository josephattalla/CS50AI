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

    # return moves 
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # if the action is placing a move on a spot that is not empty, raise Excpetion
    if board[action[0], action[1]] != EMPTY:
        raise Exception('Invalid Move!')
    
    # make deepcopy of board
    new_board = deepcopy(board)

    # get whose turn it is
    user = player(board)

    # place user (player) in action (empty index on board)
    new_board[action[0], action[1]] = user

    # return new_board
    return new_board




def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check rows and columns for a winner
    for i in range(3):
        # Check rows
        if board[i] == [X, X, X]:
            return X
        elif board[i] == [O, O, O]:
            return O

        # Check columns
        if board[0][i] == board[1][i] == board[2][i] == X:
            return X
        elif board[0][i] == board[1][i] == board[2][i] == O:
            return O

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == X or board[0][2] == board[1][1] == board[2][0] == X:
        return X
    elif board[0][0] == board[1][1] == board[2][2] == O or board[0][2] == board[1][1] == board[2][0] == O:
        return O

    # If no winner, return None
    return None
    

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # if there is a winner, return True
    if winner(board):
        return True
    
    # if all spots are not empty, return True, else return False
    return all(col != EMPTY for row in board for col in row)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    # check who won and return their respective number
    user = winner(board)
    if user:
        if user == X:
            return 1
        else:
            return -1
    
    # if no one won, return 0
    return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    # get player
    user = player(board)

    # if player is X, call max_function; else call min_function
    if user == X:
        return max_function(board)[1]
    else:
        return min_function(board)[1]


def max_function(board):
        """
        Returns the maximized action and utility value for the current player.
        """
        
        # if game is over, return None for action and the utility
        if terminal(board):
            return None, utility(board)
        
        # set starting value to maximize against and empty best action
        v = -math.inf
        best_action = None

        # loop through the possible actions
        moves = actions(board)
        for move in moves:

            # create new board based on current move
            new_board = result(board, move)
            # get value of optimal move of other player using min_function
            _, value = min_function(new_board)
            
            # if value is greater than v, set v = value and best_action = move
            if value > v:
                v = value
                best_action = move
        
        # return the best_action and value of best_action (the value is used for the min_function)
        return best_action, v

            

def min_function(board):
    """
    Returns the minimized action and utility value for current player.
    """

    # if game is over, return None for action and the utility
    if terminal(board):
        return None, utility(board)
    
    # set starting value to maximize against and empty best action
    v = math.inf
    best_action = None

    # loop through the possible actions
    moves = actions(board)
    for move in moves:

        # create new board based on current move
        new_board = result(board, move)
        # get value of optimal move of other player using max_function
        _, value = max_function(new_board)
        
        # if value is less than v, set v = value and best_action = move
        if value < v:
            v = value
            best_action = move
    
    # return the best_action and value of best_action (the value is used for the max_function)
    return best_action, v
    