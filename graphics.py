import pygame
import math
from helpers import *
from constants import *
import random
from menuButton import MenuButton


def draw_board(screen, rows, columns):
    """
    This function draws a game board of rows X column dimension on the given
    screen
    :param screen: pygame.display
    :param rows: integer specifying the number of rows of the board
    :param columns: integer specifying the number of rows of the board
    :return: no return value
    """
    cell_width = WINDOW_WIDTH / columns
    cell_height = ((WINDOW_HEIGHT - 100) / rows)
    piece_radius = (CELL_HEIGHT / 4)
    for c in range(columns):
        for r in range(rows):
            pygame.draw.rect(screen, GRAY,
                             pygame.Rect(c * cell_width, r * cell_height + 100,
                                         cell_width, cell_height), 1)
            pygame.draw.circle(screen, EMPTY_PIECE_COLOR,
                               (c * cell_width + cell_width / 2,
                                r * cell_height + 100 + cell_height / 2),
                               piece_radius)


def draw_main_title(display):
    """
    This function draws text at a given position
    :param display: pygame.display
    :return: no return value
    """
    menu_font = pygame.font.Font('freesansbold.ttf', 70)
    title = menu_font.render('CONNECT 4', True, WHITE, BLACK)
    titleRect = title.get_rect()
    titleRect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)
    display.blit(title, titleRect)


def draw_text_box(screen, text, box_color):
    """
    This function draws a text a defined position on the screen
    :param screen: pygame.display
    :param text: the string that will be rendered
    :param box_color: the color of the background box where the text will be
    written
    :return: no return value
    """
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
    """
    This function draws a text a defined position on the screen, the winner
    of the game
    :param display: pygame.display
    :param text: string that will be rendered
    :return: no return value
    """
    draw_text_box(display, '', BLACK)
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
    """
    This function renders the main frame of the game, containing a title and
    a start button
    :param display: pygame.display
    :return: returns the initialized start button
    """
    font = pygame.font.Font('freesansbold.ttf', 50)
    draw_main_title(display)
    startButton = MenuButton('START', START_BUTTON_COORD, display, font)
    return startButton


def render_options_frame(display, board, gaming_mode, first_player, rows,
                         columns):
    """
    This function renders the options frame of the game, containing 3
    buttons: Easy, Medium, Hard. Each button on click will trigger a
    specifiv game mode.
    :param display: pygame.display
    :param board: matrix containing the current state of the game
    :param gaming_mode: equal to "computer" if the set game mode is "player
    vs computer" or equal to "human" is mode is "player vs player"
    :param first_player: states which player will move first
    :param rows: the number of rows of the board
    :param columns: the number of columns of the board
    :return: no return value
    """
    menu_font = pygame.font.Font('freesansbold.ttf', 60)
    buttons = [MenuButton('EASY', EASY_BUTTON_COORD, display, menu_font),
               MenuButton('MEDIUM', MEDIUM_BUTTON_COORD, display, menu_font),
               MenuButton('HARD', HARD_BUTTON_COORD, display, menu_font)]
    while True:
        for event in pygame.event.get():
            display.fill(BLACK)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].rect.collidepoint(pygame.mouse.get_pos()):
                    render_computer_game_frame(display, board, gaming_mode,
                                               first_player, rows, columns, 1)
                elif buttons[1].rect.collidepoint(pygame.mouse.get_pos()):
                    render_computer_game_frame(display, board, gaming_mode,
                                               first_player, rows, columns, 4)
                elif buttons[2].rect.collidepoint(pygame.mouse.get_pos()):
                    render_computer_game_frame(display, board, gaming_mode,
                                               first_player, rows, columns, 5)
            for option in buttons:
                if option.rect.collidepoint(pygame.mouse.get_pos()):
                    option.hovered = True
                else:
                    option.hovered = False
                option.draw()
                pygame.display.update()


def get_game_info_dict(gaming_mode):
    """
    This function returns a dictionary adapted to the given game mode
    :param gaming_mode: "human" for "player vs player" or "computer" for
    "computer vs player"
    :return: selected dictionary
    """
    if gaming_mode == 'computer':
        game_info = {
            'turn_captions': ['Player turn...', 'Computer turn...'],
            'winning_captions': ['Player wins...', 'Computer wins...'],
            'piece': [1, 2],
            'piece_color': [YELLOW, RED]
        }
    else:
        game_info = {
            'turn_captions': ['Player 1 turn...', 'Player 2 turn...'],
            'winning_captions': ['Player 1 wins...', 'Player 2 wins...'],
            'piece': [1, 2],
            'piece_color': [YELLOW, RED]
        }
    return game_info


def render_game_frame(screen, board, playing_mode, first_player=None, rows=4,
                      columns=4):
    """
    This function renders the player vs player game
    :param screen: pygame.display
    :param board:  matrix containing the current state of the game
    :param playing_mode: equal to "computer" if the set game mode is "player
    vs computer" or equal to "human" is mode is "player vs player"
    :param first_player: the player who moves first
    :param rows: number of rows of the board
    :param columns: number of columns of the board
    :return: no returned value
    """
    cell_width = WINDOW_WIDTH / columns
    cell_height = ((WINDOW_HEIGHT - 100) / rows)
    piece_radius = (CELL_HEIGHT / 4)
    if playing_mode == 'human':
        game_info_dict = get_game_info_dict('player')
        turn = random.randint(0, 1)
    else:
        game_info_dict = get_game_info_dict('computer')
        if first_player == 'human':
            turn = 0
        else:
            turn = 1

    draw_board(screen, rows, columns)
    draw_text_box(screen, game_info_dict['turn_captions'][turn],
                  game_info_dict['piece_color'][turn])
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # draw when we have a full board
            if is_board_full(board):
                pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                draw_winning_frame(screen, 'Draw')
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                posy = math.floor(event.pos[0] / cell_width)
                if not is_valid_move(board, posy):
                    draw_text_box(screen,
                                  'Invalid column.Please choose another '
                                  'one...',
                                  GREEN)
                    continue
                else:
                    posx = find_first_free_cell(board, posy)

                pygame.draw.circle(screen, game_info_dict['piece_color'][turn],
                                   (posy * cell_width + cell_width / 2,
                                    posx * cell_height + 100 + cell_height /
                                    2),
                                   PIECE_RADIUS)
                _, row = make_move(board, posy, game_info_dict['piece'][turn])
                if is_final_state(board, row, posy):
                    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                    draw_winning_frame(screen,
                                       game_info_dict['winning_captions'][
                                           turn])
                    break
                else:
                    draw_text_box(screen, game_info_dict['turn_captions'][
                        (turn + 1) % 2],
                                  game_info_dict['piece_color'][
                                      (turn + 1) % 2])
                    turn = (turn + 1) % 2
        pygame.display.flip()
    quit()


def render_computer_game_frame(screen, board, playing_mode, first_player=None,
                               rows=4, columns=4, difficulty=4):
    """
    This function render the computer vs player game
    :param screen: pygame.display
    :param board:  matrix containing the current state of the game
    :param playing_mode: equal to "computer" if the set game mode is "player
    vs computer" or equal to "human" is mode is "player vs player"
    :param first_player: the player who moves first
    :param rows: number of rows of the board
    :param columns: number of columns of the board
    :param difficulty: the initial depth of the minimax algorithm,
    the greater the depth, the smarter the AI algorithm
    :return: no returned value
    """
    cell_width = WINDOW_WIDTH / columns
    cell_height = ((WINDOW_HEIGHT - 100) / rows)
    piece_radius = (CELL_HEIGHT / 4)
    if playing_mode == 'human':
        game_info_dict = get_game_info_dict('player')
        turn = random.randint(0, 1)
    else:
        game_info_dict = get_game_info_dict('computer')
        if first_player == 'human':
            turn = 0
        else:
            turn = 1

    draw_board(screen, rows, columns)
    draw_text_box(screen, game_info_dict['turn_captions'][turn],
                  game_info_dict['piece_color'][turn])
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # draw when we have a full board
            if is_board_full(board):
                pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                draw_winning_frame(screen, 'Draw')
                break
            if turn == 0:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posy = math.floor(event.pos[0] / cell_width)
                    if not is_valid_move(board, posy):
                        draw_text_box(screen,
                                      'Invalid column.Please choose another '
                                      'one...',
                                      GREEN)
                        continue
                    else:
                        posx = find_first_free_cell(board, posy)

                    pygame.draw.circle(screen,
                                       game_info_dict['piece_color'][turn],
                                       (posy * cell_width + cell_width / 2,
                                        posx * cell_height + 100 +
                                        cell_height / 2),
                                       piece_radius)
                    _, row = make_move(board, posy,
                                       game_info_dict['piece'][turn])
                    if is_final_state(board, row, posy):
                        pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                        draw_winning_frame(screen,
                                           game_info_dict['winning_captions'][
                                               turn])
                        break
                    else:
                        draw_text_box(screen, game_info_dict['turn_captions'][
                            (turn + 1) % 2],
                                      game_info_dict['piece_color'][
                                          (turn + 1) % 2])
                        turn = (turn + 1) % 2
            elif turn == 1:
                posy, _ = minimax_alpha_beta(board, difficulty, float('-inf'),
                                             float('inf'), True)
                if posy is None:
                    # end of the game draw, the minimax algoritm could not
                    # find a valid column
                    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                    draw_winning_frame(screen, "Draw")
                    break
                posx = find_first_free_cell(board, posy)

                pygame.draw.circle(screen, game_info_dict['piece_color'][turn],
                                   (posy * cell_width + cell_width / 2,
                                    posx * cell_height + 100 + cell_height /
                                    2),
                                   piece_radius)
                _, row = make_move(board, posy, game_info_dict['piece'][turn])
                if is_final_state(board, row, posy):
                    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                    draw_winning_frame(screen,
                                       game_info_dict['winning_captions'][
                                           turn])
                    break
                else:
                    draw_text_box(screen, game_info_dict['turn_captions'][
                        (turn + 1) % 2],
                                  game_info_dict['piece_color'][
                                      (turn + 1) % 2])
                    turn = (turn + 1) % 2
        pygame.display.flip()
    quit()


def play_game(board, mode, first_player, rows, columns):
    """
    This functions renders the graphic of connect four game.
    :param board:  matrix containing the current state of the game
    :param mode: equal to "computer" if the set game mode is "player
    vs computer" or equal to "human" is mode is "player vs player"
    :param first_player: the player who moves first
    :param rows: number of rows of the board
    :param columns: number of columns of the board
    :return: no returned value
    """
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
                if startButton.rect[0] <= mouse[0] <= startButton.rect[0] + \
                    startButton.rect[2] and startButton.rect[1] \
                    <= mouse[1] <= startButton.rect[1] + startButton.rect[3]:
                    if mode == 'computer':
                        screen.fill(BLACK)
                        render_options_frame(screen, board, mode, first_player,
                                             rows, columns)
                        pygame.display.update()
                    else:
                        screen.fill(BLACK)
                        render_game_frame(screen, board, mode, first_player,
                                          rows, columns)
                        pygame.display.update()
            if startButton.rect.collidepoint(pygame.mouse.get_pos()):
                startButton.hovered = True
            else:
                startButton.hovered = False
            draw_main_title(screen)
            startButton.draw()
            pygame.display.update()
