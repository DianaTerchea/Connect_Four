import pygame
import math
from fourInRow import *
from constants import *


def draw_board(screen):
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE,
                             pygame.Rect(c * CELL_WIDTH, r * CELL_HEIGHT + 100, CELL_WIDTH, CELL_HEIGHT), 1)
            pygame.draw.circle(screen, PIECE_COLOR,
                               (c * CELL_WIDTH + CELL_WIDTH / 2, r * CELL_HEIGHT + 100 + CELL_HEIGHT / 2), PIECE_RADIUS)


def draw_text_box(screen, text, box_color):
    pygame.display.update()
    menu_font = pygame.font.Font('freesansbold.ttf', 30)
    title = menu_font.render(text, True, box_color, BLACK)
    titleRect = title.get_rect()
    titleRect.topleft = (0, 0)
    titleRect.width = WINDOW_WIDTH
    titleRect.height = 50
    pygame.draw.rect(screen, BLACK, titleRect)
    screen.blit(title, titleRect)
    pygame.display.update()


def draw_winning_screen(display, text):
    draw_text_box(display, "", BLACK)
    menu_font = pygame.font.Font('freesansbold.ttf', 60)
    title = menu_font.render(text, True, WHITE, BLACK)
    titleRect = title.get_rect()
    titleRect.center = (WINDOW_WIDTH // 2, 50)
    display.blit(title, titleRect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


def game_mode(screen, board):
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
                    draw_text_box(screen, "Invalid column.Please choose another one...", GREEN)
                    # turn = (turn + 1) % 2
                    continue
                else:
                    posx = find_first_free_cell(board, posy)

                if turn == 0:
                    pygame.draw.circle(screen, YELLOW,
                                       (posy * CELL_WIDTH + CELL_WIDTH / 2, posx * CELL_HEIGHT + 100 + CELL_HEIGHT / 2),
                                       PIECE_RADIUS)
                    _, row = make_move(board, posy, "P1")
                    if is_final_state(board, row, posy):
                        draw_text_box(screen, "Player 1 wins...", GREEN)
                        pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                        draw_winning_screen(screen, "Player 1 wins...")
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
                        draw_text_box(screen, "Player 2 wins...", GREEN)
                        pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                        draw_winning_screen(screen, "Player 2 wins...")
                        break
                    else:
                        draw_text_box(screen, "Player 1 turn...", YELLOW)
                        turn = 0

        pygame.display.flip()