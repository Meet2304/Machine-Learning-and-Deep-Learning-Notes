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
    Returns the starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    countX = sum(row.count(X) for row in board)
    countO = sum(row.count(O) for row in board)
    
    return O if countX > countO else X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(row, col) for row in range(3) for col in range(3) if board[row][col] == EMPTY}

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY:
        raise ValueError("Invalid action")
    
    result_board = copy.deepcopy(board)
    result_board[action[0]][action[1]] = player(board)
    return result_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows, columns, and diagonals
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != EMPTY:
            return board[row][0]
    
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != EMPTY:
            return board[0][col]
    
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(cell != EMPTY for row in board for cell in row)

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0 

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def MAX_VALUE(board):
        if terminal(board):
            return utility(board), None
        value = -math.inf
        best_action = None
        for action in actions(board):
            move_value, _ = MIN_VALUE(result(board, action))
            if move_value > value:
                value = move_value
                best_action = action
        return value, best_action
    
    def MIN_VALUE(board):
        if terminal(board):
            return utility(board), None
        value = math.inf
        best_action = None
        for action in actions(board):
            move_value, _ = MAX_VALUE(result(board, action))
            if move_value < value:
                value = move_value
                best_action = action
        return value, best_action

    # AI makes the first move if user is O
    if player(board) == O and len(actions(board)) == 9:
        return actions(board).pop()  # Choose any first move for O
    
    # Normal minimax behavior
    return MAX_VALUE(board)[1] if player(board) == X else MIN_VALUE(board)[1]
