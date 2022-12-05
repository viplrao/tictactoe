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

    return X if num_xs > num_os else O


def actions(board: Board) -> set:
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    print(f"actions(board) called on {board}")
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
    print(f"result(board) called with {board}, {action}")
    if action is None:
        return board

    return_board = deepcopy(board)
    print("result: copy made")
    i = int(action[0])
    j = int(action[1])

    invalid_action = \
        i > 2 or \
        j > 2 or \
        board[i][j] != EMPTY or \
        winner(board) is not None

    if invalid_action:
        print(f"result: action {action} is invalid")
        raise Exception

    return_board[i][j] = player(board)
    print(f"result: returning f{return_board}")

    return return_board


def winner(board: Board) -> Optional[Player]:
    """
    Returns the winner of the game, if there is one.
    """
    if board == initial_state():
        return None

    for row in board:
        # Horizontal Check
        for _player in [X, O]:
            # If all the squares have the same player
            if filter(lambda x: x == _player, row) == row:
                return _player
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
    print(f"terminal(board) called on {board}")
    if winner(board):
        print("terminal: board has winner")
        return True

    for row in board:
        # At least one empty square? Game isn't over yet
        if len([square for square in row if square is EMPTY]) > 0:
            print(f"terminal: row {row} has empty square, returning false...")
            return False

    # Should be unreachable but just in case
    return True


def utility(board: Board) -> int:
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    print(f"utility(board) called on {board}")

    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board: Board) -> Optional[Action]:
    """
    Returns the optimal action for the current player on the board.
    """
    print(f"minimax called on board {board}")
    if terminal(board):
        return None

    _player = player(board)
    if _player == X:
        return minimax(result(board, max_value(board)[1]))
    else:
        return minimax(result(board, min_value(board)[1]))


def max_value(board: Board) -> Tuple[Numeric, Action]:
    print(f"max_value(board) called on {board}")
    # Base case
    if terminal(board):
        print(f"maxvalue: board {board} is terminal")
        return utility(board), (0, 0)

    v = -float("inf")
    best_action = (0, 0)

    for action in actions(board):
        # Try an action
        new_board = result(board, action)
        # Simulate min_player's move in response
        min_move = min_value(new_board)[0]
        print(f"max_value: found min_move = {min_move}")
        # Check if that's better
        if min_move > v:
            v = min_move
            best_action = action
            print(f"max_value: new best action is {best_action}")

    # Return the max_value and the action needed to achieve it
    return v, best_action


# Same thing but inverse
def min_value(board: Board) -> Tuple[Numeric, Action]:
    # Base case
    if terminal(board):
        return utility(board), (0, 0)

    v = float("inf")
    best_action = (0, 0)

    for action in actions(board):
        # Try an action
        new_board = result(board, action)
        # Simulate max_player's move in response
        min_move = max_value(new_board)[0]
        # Check if that's better
        if min_move < v:
            v = min_move
            best_action = action

    # Return the min_value and the action needed to achieve it
    return v, best_action
