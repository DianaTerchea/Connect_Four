import pygame
import math
from fourInRow import *
import time

COLUMNS = 7
ROWS = 6

WINDOW_HEIGHT = 850
WINDOW_WIDTH = 850
CELL_WIDTH = WINDOW_WIDTH / COLUMNS
CELL_HEIGHT = ((WINDOW_HEIGHT - 100) / ROWS)
PIECE_RADIUS = (CELL_HEIGHT / 4)

PIECE_COLOR = (140, 140, 140)
BLUE = (40, 34, 100)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def draw_board(screen):
    print("Drawing initial table...")
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE,
                             pygame.Rect(c * CELL_WIDTH, r * CELL_HEIGHT + 100, CELL_WIDTH, CELL_HEIGHT), 1)
            pygame.draw.circle(screen, PIECE_COLOR,
                               (c * CELL_WIDTH + CELL_WIDTH / 2, r * CELL_HEIGHT + 100 + CELL_HEIGHT / 2), PIECE_RADIUS)


def draw_text_box(screen, text, box_color):
    pygame.draw.rect(screen, box_color,
                     pygame.Rect(0, 0, 200, 35))
    pygame.display.update()
    font = pygame.font.SysFont('Arial', 25)
    screen.blit(font.render(text, True, WHITE), (0, 0))
    pygame.display.update()


def draw_winning_screen(screen, text):
    pygame.draw.rect(screen, BLACK,
                     pygame.Rect(WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 - 100, 500, 500))
    pygame.display.update()
    font = pygame.font.SysFont('Arial', 25)
    screen.blit(font.render(text, True, WHITE), (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
    pygame.display.update()


def graphic_game(board):
    pygame.init()
    screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
    pygame.mouse.set_cursor(*pygame.cursors.diamond)
    pygame.display.set_caption('CONNECT_4')
    draw_board(screen)
    draw_text_box(screen, "Player 1 turn...", YELLOW)

    running = True
    turn = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                posy = math.floor(event.pos[0] / CELL_WIDTH)
                if not is_valid_move(board, posy):
                    draw_text_box(screen, "Invalid column...", RED)
                    turn = (turn + 1) % 2
                else:
                    posx = find_first_free_cell(board, posy)

                if turn == 0:
                    pygame.draw.circle(screen, YELLOW,
                                       (posy * CELL_WIDTH + CELL_WIDTH / 2, posx * CELL_HEIGHT + 100 + CELL_HEIGHT / 2),
                                       PIECE_RADIUS)
                    _, row = make_move(board, posy, "P1")
                    if is_final_state(board, row, posy):
                        draw_winning_screen(screen, "Player 1 wins...")
                        time.sleep(3)
                        break
                    else:
                        draw_text_box(screen, "Player 2 turn...", RED)
                        turn = 1
                else:
                    pygame.draw.circle(screen, RED,
                                       (posy * CELL_WIDTH + CELL_WIDTH / 2, posx * CELL_HEIGHT + 100 + CELL_HEIGHT / 2),
                                       PIECE_RADIUS)
                    _, row = make_move(board, posy, "P2")
                    if is_final_state(board, row, posy):
                        draw_winning_screen(screen, "Player 2 wins...")
                        time.sleep(3)
                        running = False
                    else:
                        draw_text_box(screen, "Player 1 turn...", YELLOW)
                        turn = 0

        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    table = [[0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0]]
    graphic_game(table)
