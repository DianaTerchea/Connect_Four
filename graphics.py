import pygame
import math
from helpers import *
from constants import *
import random
from menuButton import MenuButton


def draw_board(screen, rows, columns):
    CELL_WIDTH = WINDOW_WIDTH / columns
    CELL_HEIGHT = ((WINDOW_HEIGHT - 100) / rows)
    PIECE_RADIUS = (CELL_HEIGHT / 4)
    for c in range(columns):
        for r in range(rows):
            pygame.draw.rect(screen, GRAY,
                             pygame.Rect(c * CELL_WIDTH, r * CELL_HEIGHT + 100, CELL_WIDTH, CELL_HEIGHT), 1)
            pygame.draw.circle(screen, EMPTY_PIECE_COLOR,
                               (c * CELL_WIDTH + CELL_WIDTH / 2, r * CELL_HEIGHT + 100 + CELL_HEIGHT / 2), PIECE_RADIUS)


def draw_main_title(display):
    menu_font = pygame.font.Font('freesansbold.ttf', 70)
    title = menu_font.render("CONNECT 4", True, WHITE, BLACK)
    titleRect = title.get_rect()
    titleRect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)
    display.blit(title, titleRect)


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


def draw_winning_frame(display, text):
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


def render_main_frame(display):
    font = pygame.font.Font('freesansbold.ttf', 50)
    draw_main_title(display)
    startButton = MenuButton("START", START_BUTTON_COORD, display, font)
    return startButton


def render_options_frame(display, board, gaming_mode, first_player, rows, columns):
    menu_font = pygame.font.Font('freesansbold.ttf', 60)
    buttons = [MenuButton("EASY", EASY_BUTTON_COORD, display, menu_font),
               MenuButton("MEDIUM", MEDIUM_BUTTON_COORD, display, menu_font),
               MenuButton("HARD", HARD_BUTTON_COORD, display, menu_font)]
    while True:
        for event in pygame.event.get():
            display.fill(BLACK)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].rect.collidepoint(pygame.mouse.get_pos()):
                    render_computer_game_frame(display, board, gaming_mode, first_player, rows, columns)
                elif buttons[1].rect.collidepoint(pygame.mouse.get_pos()):
                    render_computer_game_frame(display, board, gaming_mode, first_player, rows, columns, 6)
                elif buttons[2].rect.collidepoint(pygame.mouse.get_pos()):
                    render_computer_game_frame(display, board, gaming_mode, first_player, rows, columns, 8)
            for option in buttons:
                if option.rect.collidepoint(pygame.mouse.get_pos()):
                    option.hovered = True
                else:
                    option.hovered = False
                option.draw()
                pygame.display.update()


def get_game_info_dict(gaming_mode):
    if gaming_mode == "computer":
        game_info = {
            "turn_captions": ["Player turn...", "Computer turn..."],
            "winning_captions": ["Player wins...", "Computer wins..."],
            "piece": ["P", "C"],
            "piece_color": [YELLOW, RED]
        }
    else:
        game_info = {
            "turn_captions": ["Player 1 turn...", "Player 2 turn..."],
            "winning_captions": ["Player 1 wins...", "Player 2 wins..."],
            "piece": ["P1", "P2"],
            "piece_color": [YELLOW, RED]
        }
    return game_info


def render_game_frame(screen, board, playing_mode, first_player=None, rows=4, columns=4):
    CELL_WIDTH = WINDOW_WIDTH / columns
    CELL_HEIGHT = ((WINDOW_HEIGHT - 100) / rows)
    PIECE_RADIUS = (CELL_HEIGHT / 4)
    if playing_mode == "human":
        game_info_dict = get_game_info_dict("player")
        turn = random.randint(0, 1)
    else:
        game_info_dict = get_game_info_dict("computer")
        if first_player == "human":
            turn = 0
        else:
            turn = 1

    draw_board(screen, rows, columns)
    draw_text_box(screen, game_info_dict["turn_captions"][turn], game_info_dict["piece_color"][turn])
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # draw when we have a full board
            if is_board_full(board):
                pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                draw_winning_frame(screen, "Draw")
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                posy = math.floor(event.pos[0] / CELL_WIDTH)
                if not is_valid_move(board, posy):
                    draw_text_box(screen, "Invalid column.Please choose another one...", GREEN)
                    continue
                else:
                    posx = find_first_free_cell(board, posy)

                pygame.draw.circle(screen, game_info_dict["piece_color"][turn],
                                   (posy * CELL_WIDTH + CELL_WIDTH / 2, posx * CELL_HEIGHT + 100 + CELL_HEIGHT / 2),
                                   PIECE_RADIUS)
                _, row = make_move(board, posy, game_info_dict["piece"][turn])
                if is_final_state(board, row, posy):
                    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                    draw_winning_frame(screen, game_info_dict["winning_captions"][turn])
                    break
                else:
                    draw_text_box(screen, game_info_dict["turn_captions"][(turn + 1) % 2],
                                  game_info_dict["piece_color"][(turn + 1) % 2])
                    turn = (turn + 1) % 2
        pygame.display.flip()
    quit()


def render_computer_game_frame(screen, board, playing_mode, first_player=None, rows=4, columns=4, difficulty=4):
    CELL_WIDTH = WINDOW_WIDTH / columns
    CELL_HEIGHT = ((WINDOW_HEIGHT - 100) / rows)
    PIECE_RADIUS = (CELL_HEIGHT / 4)
    if playing_mode == "human":
        game_info_dict = get_game_info_dict("player")
        turn = random.randint(0, 1)
    else:
        game_info_dict = get_game_info_dict("computer")
        if first_player == "human":
            turn = 0
        else:
            turn = 1

    draw_board(screen, rows, columns)
    draw_text_box(screen, game_info_dict["turn_captions"][turn], game_info_dict["piece_color"][turn])
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # draw when we have a full board
            if is_board_full(board):
                pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                draw_winning_frame(screen, "Draw")
                break
            if turn == 0:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posy = math.floor(event.pos[0] / CELL_WIDTH)
                    if not is_valid_move(board, posy):
                        draw_text_box(screen, "Invalid column.Please choose another one...", GREEN)
                        continue
                    else:
                        posx = find_first_free_cell(board, posy)

                    pygame.draw.circle(screen, game_info_dict["piece_color"][turn],
                                       (posy * CELL_WIDTH + CELL_WIDTH / 2, posx * CELL_HEIGHT + 100 + CELL_HEIGHT / 2),
                                       PIECE_RADIUS)
                    _, row = make_move(board, posy, game_info_dict["piece"][turn])
                    if is_final_state(board, row, posy):
                        pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                        draw_winning_frame(screen, game_info_dict["winning_captions"][turn])
                        break
                    else:
                        draw_text_box(screen, game_info_dict["turn_captions"][(turn + 1) % 2],
                                      game_info_dict["piece_color"][(turn + 1) % 2])
                        turn = (turn + 1) % 2
            elif turn == 1:
                posy, _ = minimax(board, difficulty, float('-inf'), float('inf'), True)
                posx = find_first_free_cell(board, posy)

                pygame.draw.circle(screen, game_info_dict["piece_color"][turn],
                                   (posy * CELL_WIDTH + CELL_WIDTH / 2, posx * CELL_HEIGHT + 100 + CELL_HEIGHT / 2),
                                   PIECE_RADIUS)
                _, row = make_move(board, posy, game_info_dict["piece"][turn])
                if is_final_state(board, row, posy):
                    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                    draw_winning_frame(screen, game_info_dict["winning_captions"][turn])
                    break
                else:
                    draw_text_box(screen, game_info_dict["turn_captions"][(turn + 1) % 2],
                                  game_info_dict["piece_color"][(turn + 1) % 2])
                    turn = (turn + 1) % 2
        pygame.display.flip()
    quit()


def play_game(board, mode, first_player, rows, columns):
    pygame.init()
    screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
    pygame.mouse.set_cursor(*pygame.cursors.diamond)
    pygame.display.set_caption('CONNECT_4')
    startButton = render_main_frame(screen)
    while True:
        for event in pygame.event.get():
            screen.fill(BLACK)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if startButton.rect[0] <= mouse[0] <= startButton.rect[0] + startButton.rect[2] and startButton.rect[
                    1] <= mouse[1] <= startButton.rect[1] + startButton.rect[3]:
                    if mode == "computer":
                        screen.fill(BLACK)
                        render_options_frame(screen, board, mode, first_player, rows, columns)
                        pygame.display.update()
                    else:
                        screen.fill(BLACK)
                        render_game_frame(screen, board, mode, first_player, rows, columns)
                        pygame.display.update()
            if startButton.rect.collidepoint(pygame.mouse.get_pos()):
                startButton.hovered = True
            else:
                startButton.hovered = False
            draw_main_title(screen)
            startButton.draw()
            pygame.display.update()
