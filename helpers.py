def create_board(rows, columns):
    res = [[0 for i in range(columns)] for j in range(rows)]
    return res


def print_board(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            print(board[i][j], end=" ")
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
    diagonal_points = [(i, j) for i in range(len(board)) for j in range(len(board[0])) if
                       abs(row - i) == abs(column - j)]
    fdiagonal = [record for record in diagonal_points if
                 abs(diagonal_points[0][0] - record[0]) == abs(diagonal_points[0][1] - record[1])]
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
    if is_four_in_row(board, row, column) or is_four_in_column(board, row, column) or is_four_in_diagonal(board, row,
                                                                                                          column):
        return True
    return False


def is_board_full(board):
    return not any(0 in val for val in board)
