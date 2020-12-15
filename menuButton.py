from constants import *


class MenuButton:
    hovered = False

    def __init__(self, text, pos, screen, font):
        self.text = text
        self.pos = pos
        self.screen = screen
        self.menu_font = font
        self.draw()

    def draw(self):
        self.rend = self.menu_font.render(self.text, True, self.get_button_color())
        self.rect = self.rend.get_rect()
        self.rect.center = self.pos
        self.screen.blit(self.rend, self.rect)

    def get_button_color(self):
        if self.hovered:
            return GRAY
        else:
            return WHITE
