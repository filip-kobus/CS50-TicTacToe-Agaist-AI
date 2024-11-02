"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy
from operator import index

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
    x_moves, o_moves = count_moves_on_board(board)

    return X if x_moves == o_moves else O

def count_moves_on_board(board):
    x_counter = 0
    o_counter = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                x_counter += 1
            elif board[i][j] == O:
                o_counter += 1

    return x_counter, o_counter

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                action = i, j
                possible_actions.add(action)

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    current_player = player(board)
    i, j = action
    board_after_action = deepcopy(board)
    board_after_action[i][j] = current_player

    return board_after_action


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    previous_player = O if player(board) == X else X

    # Check if there is horizontal, vertical or diagonal winner
    for i in range(3):
        vertical_streak = 0
        horizontal_streak = 0
        for j in range(3):
            if board[i][j] == previous_player:
                horizontal_streak += 1
            if board[j][i] == previous_player:
                vertical_streak += 1
        if vertical_streak == 3 or horizontal_streak == 3:
            return previous_player

    # Check if there is diagonal winner
    left_diagonal_streak = 0
    right_diagonal_streak = 0
    for i in range(3):
        if board[i][i] == previous_player:
            left_diagonal_streak += 1
        if board[i][2-i] == previous_player:
            right_diagonal_streak += 1

    if right_diagonal_streak == 3 or left_diagonal_streak == 3:
        return previous_player

    return EMPTY


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True

    return not any(EMPTY in row for row in board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if win := winner(board):
        return 1 if win == X else -1
    return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def get_min(board):
        if terminal(board):
            return utility(board)

        possible_actions = actions(board)
        min_value = 2
        for action in possible_actions:
            board_after_action = result(board, action)
            next_value = get_max(board_after_action)
            if next_value == -1:
                return -1
            if next_value < min_value:
                min_value = next_value

        return min_value


    def get_max(board):
        if terminal(board):
            return utility(board)

        possible_actions = actions(board)
        max_value = -2
        for action in possible_actions:
            board_after_action = result(board, action)
            next_value = get_min(board_after_action)
            if next_value == 1:
                return 1
            if next_value > max_value:
                max_value = next_value

        return max_value

    current_player = player(board)
    best_action = None
    possible_actions = actions(board)

    if terminal(board):
        return None

    if current_player == X:
        max_val = -2
        for action in possible_actions:
            value = get_min(result(board, action))
            if value > max_val:
                max_val = value
                best_action = action
    else:
        min_val = 2
        for action in possible_actions:
            value = get_max(result(board, action))
            if value < min_val:
                min_val = value
                best_action = action

    return best_action