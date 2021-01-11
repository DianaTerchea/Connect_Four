from copy import deepcopy
from random import randrange, shuffle

PLAYER_PIECE = 1


def create_board(rows, columns):
    """
    This function takes two integers and returns a matrix where each element
    is initialized by 0

    :param rows: integer value specifying the number of rows for the created
    matrix
    :param columns: integer value specifying the number of columns for the
    created matrix
    :return: matrix where each element is initialized it 0
    """
    res = [[0 for i in range(columns)] for j in range(rows)]
    return res


def print_board(board):
    '''
    This function takes a matrix and prints it to the screen

    :param board: The matrix that will pe showed on the screen
    :return: no returned value
    '''
    for i in range(len(board)):
        for j in range(len(board[0])):
            print(board[i][j], end=' ')
        print()


def is_valid_move(board, picked_column):
    """
    This function checks whether a column is valid as a next move
    :param board: matrix containing the current game state of the game table
    :param picked_column: integer between 0 and len(matrix[0]) specifying a
    column of our matrix
    :return: True, if we can put a piece on that column, False otherwise
    """
    if picked_column < 0 or picked_column >= len(board[0]):
        return False
    for row in range(len(board)):
        if board[row][picked_column] == 0:
            return True
    return False


def find_first_free_cell(board, picked_column):
    """
    This function takes a matrix and an integer and returns the row number
    for the first available cell
    :param board: matrix containing the current game state of the game table
    :param picked_column: integer between 0 and len(matrix[0]) specifying a
    column of our matrix
    :return: integer specifying the first available cell from that
    picked_column
    """
    for row in reversed(range(len(board))):
        if board[row][picked_column] == 0:
            return row


def make_move(board, picked_column, player):
    """
    This function takes a matrix, and two integers and returns the modified
    matrix after placing players piece on that column
    :param board: matrix containing the current game state of the game table
    :param picked_column: integer between 0 and len(matrix[0]) specifying a
    column of our matrix
    :param player: the value of the piece that will be placed
    :return: the modified matrix and the value of the row where the piece
    was placed
    """
    row = find_first_free_cell(board, picked_column)
    board[row][picked_column] = player
    return board, row


def is_four_in_row(board, row, column):
    """
    This functions checks if in the given matrix there are four equal
    elements in a row
    :param board: matrix containing the current game state of the game table
    :param row: integer between 0 and len(matrix) specifying a row of our
    matrix
    :param column: integer between 0 and len(matrix[0]) specifying a column
    of our matrix
    :return: True if we can find a four in a row, False otherwise
    """
    sequence = [board[row][column] for j in range(4)]
    if is_subset(sequence, board[row]):
        return True
    else:
        return False


def is_four_in_column(board, row, column):
    """
       This functions checks if in the given matrix there are four equal
       elements in a column
       :param board: matrix containing the current game state of the game table
       :param row: integer between 0 and len(matrix) specifying a row of our
       matrix
       :param column: integer between 0 and len(matrix[0]) specifying a
       column of our matrix
       :return: True if we can find a four in a row in our columns,
       False otherwise
       """
    sequence = [board[row][column] for j in range(4)]
    column = [board[i][column] for i in range(len(board))]
    if is_subset(sequence, column):
        return True
    else:
        return False


def is_four_in_diagonal(board, row, column):
    """
       This functions checks if in the given matrix there are four equal
       elements on the diagonals
       :param board: matrix containing the current game state of the game table
       :param row: integer between 0 and len(matrix) specifying a row of our
       matrix
       :param column: integer between 0 and len(matrix[0]) specifying a
       column of our matrix
       :return: True if we can find a four in a row in our diagonals,
       False otherwise
       """
    sequence = [board[row][column] for j in range(4)]
    diag1, diag2 = get_diagonals(board, row, column)
    if is_subset(sequence, diag1):
        return True
    elif is_subset(sequence, diag2):
        return True
    return False


def is_subset(a, b):
    """
    This function checks if the first argument is subset of the second argument
    :param a: list of integers
    :param b: list of integers
    :return: True if a is subset of b, False otherwise
    """
    return any(map(lambda x: b[x:x + len(a)] == a, range(len(b) - len(a) + 1)))


def get_diagonal_points(board, row, column):
    """
           This function returns the coordinates of diagonal elements for a
           given position
           in the matrix
           :param board: matrix containing the current game state of the
           game table
           :param row: integer between 0 and len(matrix) specifying a row of
           our matrix
           :param column: integer between 0 and len(matrix[0]) specifying a
           column of our matrix
           :return: Two lists of tuples, the first one containing the
           coordinates of the points from the first diagonal parallel with
           the main diagonal, the second one
           containing the coordinates of the points from the diagonal
           parallel with the second diagonal
           """
    diagonal_points = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if abs(row - i) == abs(column - j):
                diagonal_points.append((i, j))
    diagonal_points = [(i, j) for i in range(len(board)) for j in
                       range(len(board[0])) if
                       abs(row - i) == abs(column - j)]
    fdiagonal = [record for record in diagonal_points if
                 abs(diagonal_points[0][0] - record[0]) == abs(
                     diagonal_points[0][1] - record[1])]
    bdiagonal = [i for i in diagonal_points if i not in fdiagonal]
    bdiagonal.append((row, column))
    return sort_list_of_tuples(fdiagonal), sort_list_of_tuples(bdiagonal)


def get_diagonals(board, row, column):
    """
    This function receives a matrix and two integers and returns two list of
    elements diagonally adjacent with our given element
    :param board: matrix containing the current game state of the
           game table
    :param row:  integer between 0 and len(matrix) specifying a row of
           our matrix
    :param column: integer between 0 and len(matrix[0]) specifying a
           column of our matrix
    :return: two list, first one containing elements diagonally adjacent,
    parallel with the main diagonal, the second one containing elements
    diagonally adjacent, parallel with second diagonal
    """
    fdiagonal, bdiagonal = get_diagonal_points(board, row, column)
    diag1 = [board[record[0]][record[1]] for record in fdiagonal]
    diag2 = [board[record[0]][record[1]] for record in bdiagonal]
    return diag1, diag2


def sort_list_of_tuples(list):
    """
    This function sorts a list of tuples by their first component
    :param list: list of tuples
    :return: the sorted list
    """
    list.sort(key=lambda x: x[0])
    return list


def is_final_state(board, row, column):
    """
    This function checks whether the given matrix is a final state for the
    game, if it has four in a row on row, on column or on diagonal
    :param board: matrix containing the current game state of the
           game table
    :param row: integer between 0 and len(matrix) specifying a row of
           our matrix
    :param column: integer between 0 and len(matrix[0]) specifying a
           column of our matrix
    :return: True if is a final state, false otherwise
    """
    if is_four_in_row(board, row, column) or is_four_in_column(board, row,
                                                               column) or \
        is_four_in_diagonal(
            board, row,
            column):
        return True
    return False


def is_board_full(board):
    """
    This functions check if there are any elements equal to 0 in our matrix
    :param board: matrix containing the current game state of the
           game table
    :return: True if there aren't any elements equal to 0, False otherwise
    """
    return not any(0 in val for val in board)


def is_terminal_node(board):
    """
    This functions checks whether the given matrix is full or is a final
    state for the game
    :param board: matrix containing the current game state of the
           game table
    :return: True, the row and column of the winning piece or False, -1, -1,
    or True, -1, -1 if the matrix is full
    """
    if is_board_full(board):
        return True, -1, -1
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != 0:
                if is_final_state(board, i, j):
                    return True, i, j
    return False, -1, -1


def compute_score(window, computer_piece):
    """
    This function checks if there are 2,3 or 4 in a row in the given window
    and adds a score according to some rules. This heuristic function was
    inspired by https://www.youtube.com/watch?v=3R1Cx6uGjMw.
    :param window: sequence of pieces
    :param computer_piece: the value of the computer piece
    :return: the computed score
    """
    score = 0
    if window.count(computer_piece) == 4:
        score += 100
    elif window.count(computer_piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(computer_piece) == 2 and window.count(0) == 2:
        score += 2
    if window.count(PLAYER_PIECE) == 2 and window.count(0) == 2:
        score -= 1
    if window.count(PLAYER_PIECE) == 3 and window.count(0) == 1:
        score -= 100
    return score


def get_move_score(board, player_piece):
    """
    This function computes the score for a player horizontally, vertically
    and diagonally. This function was inspired by
    https://www.youtube.com/watch?v=MMLtza3CZFM.
    :param board:  matrix containing the current game state of the
           game table
    :param player_piece: integer value, 0 or 1 equal to our player piece value
    :return: the computed score
    """
    # compute score horizontal
    score = 0
    center_elements = [board[i][len(board[0]) // 2] for i in range(len(board))]
    score += center_elements.count(player_piece) * 3

    for row in board:
        for column_count in range(len(board[0]) - 3):
            window = row[column_count: column_count + 4]
            score += compute_score(window, player_piece)

    # compute score vertical
    for column_index in range(len(board[0])):
        column_elements = [board[i][column_index] for i in range(len(board))]
        for row_count in range(len(board) - 3):
            window = column_elements[row_count: row_count + 4]
            score += compute_score(window, player_piece)

    # compute score on diagonals
    for row_index in range(len(board) - 3):
        for column_index in range(len(board[0]) - 3):
            window = [board[row_index + i][column_index + i] for i in range(4)]
            score += compute_score(window, player_piece)

    for row_index in range(len(board) - 3):
        for column_index in range(len(board[0]) - 3):
            window = [board[row_index + 3 - i][column_index + i] for i in
                      range(4)]
            score += compute_score(window, player_piece)

    return score


def minimax_alpha_beta(board, depth, alpha, beta, maximizing_player):
    """
    The minimax algorithm with alpha, beta pruning as explained at
    https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Pseudocode.
    :param board: matrix containing the current game state of the
           game table
    :param depth: the current depth of search
    :param alpha: alpha coefficient
    :param beta: beta coefficient
    :param maximizing_player: boolean value, True if we are on the maximizing lever, False otherwise
    :return: (None, value of the heuristic function) or (the computed column value, value of the heuristic function)
    """
    available_moves = [column for column in range(len(board[0])) if
                       is_valid_move(board, column)]
    shuffle(available_moves)
    is_terminal, row, column = is_terminal_node(board)
    if depth == 0 or is_terminal is True:
        if is_terminal is True:
            if board[row][column] == 2:
                # computer wins
                return None, float('inf')
            elif board[row][column] == 1:
                # player wins
                return None, float('-inf')
            else:  # draw
                return None, 0
        else:
            # depth == 0
            return None, get_move_score(board, 2)

    if maximizing_player:  # computer
        value = float('-inf')
        col = randrange(len(board[0]))
        for column in available_moves:
            board_copy = deepcopy(board)
            board_copy, _ = make_move(board_copy, column, 2)
            _, new_score = minimax_alpha_beta(board_copy, depth - 1, alpha,
                                              beta, False)
            if new_score > value:
                value = new_score
                col = column
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return col, value
    else:  # player
        value = float('inf')
        col = randrange(len(board[0]))
        for column in available_moves:
            board_copy = deepcopy(board)
            board_copy, _ = make_move(board_copy, column, 1)
            _, new_score = minimax_alpha_beta(board_copy, depth - 1, alpha,
                                              beta, True)
            if new_score <= value:
                value = new_score
                col = column
            beta = min(beta, value)
            if beta <= alpha:
                break
        return col, value
