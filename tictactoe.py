"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy
from typing import List, Optional, Tuple, Union

X = "X"
O = "O"
EMPTY: None = None

# Yay Typing!!
Board = List[List]
Player = str
Numeric = Union[int, float]
Action = Tuple[int, int]


def initial_state() -> Board:
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board: Board) -> str:
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        return X

    num_xs = 0
    num_os = 0
    for row in board:
        for square in row:
            if square == X:
                num_xs += 1
            elif square == O:
                num_os += 1

    return O if num_xs > num_os else X


def actions(board: Board) -> set:
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    # Add all empty squares to set
    for i, _ in enumerate(board):
        for j, _ in enumerate(board[i]):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board: Board, action: Action) -> Board:
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action is None:
        return board

    return_board = deepcopy(board)
    i = int(action[0])
    j = int(action[1])

    invalid_action = \
        i > 2 or \
        j > 2 or \
        board[i][j] != EMPTY or \
        winner(board) is not None

    if invalid_action:
        raise Exception

    return_board[i][j] = player(board)

    return return_board


def winner(board: Board) -> Optional[Player]:
    """
    Returns the winner of the game, if there is one.
    """
    if board == initial_state():
        return None

    for row in board:
        # Horizontal Check
        if all(x == row[0] for x in row):
            return row[0]

    for j, _ in enumerate(board[0]):
        first_square = board[0][j]
        all_same = True
        for i, _ in enumerate(board):
            if board[i][j] != first_square:
                all_same = False
        if all_same:
            return first_square

    # Manual Diagonal Check because only two options
    fst_diag = board[0][0] == board[1][1] == board[2][2]
    snd_diag = board[2][0] == board[1][1] == board[0][2]

    if fst_diag or snd_diag:
        return board[1][1]

    return None


def terminal(board: Board) -> bool:
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True

    for row in board:
        # At least one empty square? Game isn't over yet
        if any(square == EMPTY for square in row):
            return False

    # Should be unreachable but just in case
    return True


def utility(board: Board) -> int:
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if terminal(board) and winner(board) == X:
        return 1
    elif terminal(board) and winner(board) == O:
        return -1
    else:
        return 0


def minimax(board: Board) -> Optional[Action]:
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        return max_value(board)[1]
    else:
        return min_value(board)[1]


def max_value(board: Board) -> Tuple[Numeric, Action]:
    # Base case
    best_action = (0, 0)
    if terminal(board):
        return utility(board), best_action

    v = -float("inf")

    for action in actions(board):
        # Try an action
        new_board = result(board, action)
        # Simulate min_player's move in response
        min_move = min_value(new_board)[0]
        # Check if that's better
        if min_move > v:
            v = min_move
            best_action = action
            if v == 1:  # If you've found a winning board, no point continuing
                return v, best_action

    # Return the max_value and the action needed to achieve it
    return v, best_action


# Same thing but inverse
def min_value(board: Board) -> Tuple[Numeric, Action]:
    # Base case
    best_action = (0, 0)
    if terminal(board):
        return utility(board), best_action

    v = float("inf")

    for action in actions(board):
        # Try an action
        new_board = result(board, action)
        # Simulate max_player's move in response
        min_move = max_value(new_board)[0]
        # Check if that's better
        if min_move < v:
            v = min_move
            best_action = action
            if v == -1:  # If you've found a winning board, no point continuing
                return v, best_action

    # Return the min_value and the action needed to achieve it
    return v, best_action
