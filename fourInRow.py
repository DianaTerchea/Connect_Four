import sys


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


def player_vs_computer_game(board):
    turn = 0
    while True:
        if turn == 0:
            print("Player 1 turn...")
        else:
            print("Player 2 turn...")

        while True:
            selected_column = int(input("Give column: "))
            if not is_valid_move(board, selected_column):
                selected_column = int(input("Give a valid column: "))
                if is_valid_move(board, selected_column):
                    break
            else:
                break
        if turn == 0:
            _, row = make_move(board, selected_column, "P1")
            print_board(board)
            if is_final_state(board, row, selected_column):
                print("Player1 wins.......")
                break
            turn = 1
        else:
            _, row = make_move(board, selected_column, "P2")
            print_board(board)
            if is_final_state(board, row, selected_column):
                print("Player2 wins.....")
                break
            turn = 0


def player_vs_player_game(board):
    turn = 0
    while True:
        if turn == 0:
            print("Player 1 turn...")
        else:
            print("Player 2 turn...")

        while True:
            selected_column = int(input("Give column: "))
            if not is_valid_move(board, selected_column):
                selected_column = int(input("Give a valid column: "))
                if is_valid_move(board, selected_column):
                    break
            else:
                break
        if turn == 0:
            _, row = make_move(board, selected_column, "P1")
            print_board(board)
            if is_final_state(board, row, selected_column):
                print("Player1 wins.......")
                break
            turn = 1
        else:
            _, row = make_move(board, selected_column, "P2")
            print_board(board)
            if is_final_state(board, row, selected_column):
                print("Player2 wins.....")
                break
            turn = 0


if __name__ == '__main__':
    playerType = str(sys.argv[1])
    rows = int(sys.argv[3])
    columns = int(sys.argv[2])
    while True:
        if rows < 4:
            rows = int(input(
                "The number of rows should be at least 4. Please give a valid number of columns/rows... "))
        elif columns < 4:
            columns = int(input(
                "The number of columns should be at least 4. Please give a valid number of columns... "))
        else:
            break
    if len(sys.argv) < 5:
        firstPlayer = "human"
    else:
        firstPlayer = str(sys.argv[4])

    matrix = create_board(rows, columns)
    if playerType == "human":
        player_vs_player_game(matrix)
    else:
        player_vs_computer_game(matrix)
