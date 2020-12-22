import sys
from graphics import play_game
from helpers import create_board

if __name__ == '__main__':
    game_mode = str(sys.argv[1])
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
    play_game(matrix, game_mode, firstPlayer, rows, columns)
