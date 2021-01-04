from copy import deepcopy
from random import randrange, shuffle

PLAYER_PIECE = 1


def create_board(rows, columns):
    res = [[0 for i in range(columns)] for j in range(rows)]
    return res


def print_board(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            print(board[i][j], end=' ')
        print()


def is_valid_move(board, picked_column):
    if picked_column < 0 or picked_column >= len(board[0]):
        return False
    for row in range(len(board)):
        if board[row][picked_column] == 0:
            return True
    return False


def find_first_free_cell(board, picked_column):
    for row in reversed(range(len(board))):
        if board[row][picked_column] == 0:
            return row


def make_move(board, picked_column, player):
    row = find_first_free_cell(board, picked_column)
    board[row][picked_column] = player
    return board, row


def is_four_in_row(board, row, column):
    sequence = [board[row][column] for j in range(4)]
    if is_subset(sequence, board[row]):
        return True
    else:
        return False


def is_four_in_column(board, row, column):
    sequence = [board[row][column] for j in range(4)]
    column = [board[i][column] for i in range(len(board))]
    if is_subset(sequence, column):
        return True
    else:
        return False


def is_four_in_diagonal(board, row, column):
    sequence = [board[row][column] for j in range(4)]
    diag1, diag2 = get_diagonals(board, row, column)
    if is_subset(sequence, diag1):
        return True
    elif is_subset(sequence, diag2):
        return True
    return False


def is_subset(a, b):
    return any(map(lambda x: b[x:x + len(a)] == a, range(len(b) - len(a) + 1)))


def get_diagonal_points(board, row, column):
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
    fdiagonal, bdiagonal = get_diagonal_points(board, row, column)
    diag1 = [board[record[0]][record[1]] for record in fdiagonal]
    diag2 = [board[record[0]][record[1]] for record in bdiagonal]
    return diag1, diag2


def sort_list_of_tuples(list):
    list.sort(key=lambda x: x[0])
    return list


def is_final_state(board, row, column):
    if is_four_in_row(board, row, column) or is_four_in_column(board, row,
                                                               column) or \
        is_four_in_diagonal(
        board, row,
        column):
        return True
    return False


def is_board_full(board):
    return not any(0 in val for val in board)


def is_terminal_node(board):
    if is_board_full(board):
        return True, -1, -1
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != 0:
                if is_final_state(board, i, j):
                    return True, i, j
    return False, -1, -1


def compute_score(window, player_piece):
    score = 0
    if window.count(player_piece) == 4:
        score += 100
    elif window.count(player_piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(player_piece) == 2 and window.count(0) == 2:
        score += 2
    if window.count(1) == 2 and window.count(0) == 2:
        score -= 1
    if window.count(1) == 3 and window.count(0) == 1:
        score -= 100
    return score


def get_move_score(board, player_piece):
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
            _, new_score = minimax(board_copy, depth - 1, alpha, beta, False)
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
            _, new_score = minimax(board_copy, depth - 1, alpha, beta, True)
            if new_score <= value:
                value = new_score
                col = column
            beta = min(beta, value)
            if beta <= alpha:
                break
        return col, value
