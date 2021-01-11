from constants import *


class MenuButton:
    """This class methods were inspired by
    https://gist.github.com/ohsqueezy/2802185"""
    hovered = False

    def __init__(self, text, pos, screen, font):
        """
        This method initialize class members
        :param text: string
        :param pos: position of center button
        :param screen: pygame.display
        :param font: font of the writen text
        """
        self.text = text
        self.pos = pos
        self.screen = screen
        self.menu_font = font
        self.draw()

    def draw(self):
        """
        This method draws the button on the screen
        :return: no returned value
        """
        self.rend = self.menu_font.render(self.text, True,
                                          self.get_button_color())
        self.rect = self.rend.get_rect()
        self.rect.center = self.pos
        self.screen.blit(self.rend, self.rect)

    def get_button_color(self):
        """
        This method returns the color of the button influenced by hover
        :return: color, RGB triple = (r, g,b)
        """
        if self.hovered:
            return GRAY
        else:
            return WHITE
