"""
Tic Tac Toe Player
"""

import math
import copy

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
    
    # if game just started, it is X's turn
    if board == initial_state():
        return X
    
    # variables to track the # of X's and O's on the board
    x = 0
    o = 0

    # loop through rows and columns, count the X's and O's
    for row in board:
        for column in row:
            if column == X: x += 1
            elif column == O: o += 1
    
    return O if o < x else X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    # variable to track possible actions
    actions_ = set()

    # loop through rows and columns and add 
    for i, row in enumerate(board):
        for j, column in enumerate(row):
            if column == EMPTY: actions_.add((i, j))
    
    return actions_


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    # deep copy of board, to not change the original and making action a list to be able to access the row and column #s
    board_ = copy.deepcopy(board)
    action_ = list(action)

    # if action is not valid, raise exception
    if board_[action_[0]][action_[1]] != EMPTY or (action[0] > 2 or action[0] < 0) or (action[1] > 2 or action[1] < 0):
        raise Exception("Invalid Action")
    
    # change the spot on the board to the player whose turn it is
    board_[action_[0]][action_[1]] = player(board)

    return board_


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    for i in range(3):

        # checking rows
        if board[i] == [X, X, X]:
            return X
        if board[i] == [O, O, O]:
            return O
        
        # checking columns
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return X if board[0][i] == X else O
        
    # checking diagnols
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return X if board[0][0] == X else O
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return X if board[0][2] == X else O
        

    # if no winner, return None
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board): 
        return True

    # loop throw rows and columns, if there is an empty spot return false
    for row in board:
        for column in row:
            if column == EMPTY: 
                return False
    
    return True



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    winner_ = winner(board)

    return 1 if winner_ == X else -1 if winner_== O else 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    # if game is already over return None
    if terminal(board):
        return None
    
    if player(board) == X:

        alpha = -math.inf

        # looping through every possible action
        for action in actions(board):

            # getting the optimal move for the other player given the resulting board from the current action
            v = min_value(result(board, action), alpha)

            # if that move has a higher value than alpha, set alpha to that value and store the action
            if v > alpha:
                alpha = v
                best_action = action

        return best_action   

    else:

        beta = math.inf

        # looping through every possible action
        for action in actions(board):

            # getting the optimal move for the other player given the resulting board from the current action
            v = max_value(result(board, action), beta)

            # if that move has a lower value than beta, set beta to that value and store the action
            if v < beta:
                beta = v
                best_action = action
            
        return best_action


def max_value(board, beta):
    """
        Returns the max utility outcome of the given board state. Takes in a variable beta to incorporate alpha-beta pruning.
    """

    # if game is over return the utility of the winner
    if terminal(board):
        return utility(board)
    
    alpha = -math.inf

    # loop through every possible action
    for action in actions(board):

        # setting alpha to the max of alpha and the result of the optimal move of the other player
        alpha = max(alpha, min_value(result(board, action), alpha))

        # if alpha >= beta, then we can prune because this is would mean the optimal move of the maximizing player is going to be higher than the beta, that we are trying to minimize, we have already found
        if alpha >= beta:
            break
    
    return alpha


def min_value(board, alpha):
    """
        Returns the minimum utility outcome of the given board state. Takes in a variable alpha to incorporate alpha-beta pruning.
    """

    # if game is over return the utility of the winner
    if terminal(board):
        return utility(board)

    beta = math.inf

    # loop through every possible action
    for action in actions(board):

        # set beta to the minimum of beta and the result of the optimal move of the other player
        beta = min(beta, max_value(result(board, action), beta))

        # if beta <= alpha, then we can prune because this would mean the optimal move of the minimizing player is lower than the alpha, that we are trying to maximize, that we have already found
        if beta <= alpha:
            break
    
    return beta