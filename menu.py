from menuButton import MenuButton
from graphics import *
from constants import *


def draw_title(display):
    menu_font = pygame.font.Font('freesansbold.ttf', 70)
    title = menu_font.render("CONNECT 4", True, WHITE, BLACK)
    titleRect = title.get_rect()
    titleRect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)
    display.blit(title, titleRect)


def render_main_menu(display):
    font = pygame.font.Font('freesansbold.ttf', 50)
    draw_title(display)
    startButton = MenuButton("START", START_BUTTON_COORD, display, font)

    while True:
        for event in pygame.event.get():
            display.fill(BLACK)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if startButton.rect[0] <= mouse[0] <= startButton.rect[0] + startButton.rect[2] and startButton.rect[
                    1] <= mouse[1] <= startButton.rect[1] + startButton.rect[3]:
                    display.fill(BLACK)
                    render_options_menu(display)
                    pygame.display.update()
            if startButton.rect.collidepoint(pygame.mouse.get_pos()):
                startButton.hovered = True
            else:
                startButton.hovered = False
            draw_title(display)
            startButton.draw()
            pygame.display.update()


def render_options_menu(display):
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
                    game_mode(display, table)
                elif buttons[1].rect.collidepoint(pygame.mouse.get_pos()):
                    game_mode(display, table)
                elif buttons[2].rect.collidepoint(pygame.mouse.get_pos()):
                    game_mode(display, table)
            for option in buttons:
                if option.rect.collidepoint(pygame.mouse.get_pos()):
                    option.hovered = True
                else:
                    option.hovered = False
                option.draw()
                pygame.display.update()


def game():
    pygame.init()
    screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
    pygame.mouse.set_cursor(*pygame.cursors.diamond)
    pygame.display.set_caption('CONNECT_4')
    render_main_menu(screen)


if __name__ == '__main__':
    table = [[0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0]]
    game()
