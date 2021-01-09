from game_functions import *
from constants import *


# Класс, описывающий кнопку
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super(Button, self).__init__(all_sprites)
        self.standard_color = pygame.Color('#008000')
        self.image = pygame.Surface((w, h))
        self.image.fill(self.standard_color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = (x, y)

    # Функция подсвечивает кнопку
    def highlight(self):
        highlighted_color = screen.get_at(self.pos)
        hsv = highlighted_color.hsva
        if hsv[2] + 30 < 100:
            highlighted_color.hsva = (hsv[0], hsv[1], hsv[2] + 30, hsv[3])
        self.image.fill(highlighted_color)

    # Функция возвращает цвет кнопки в изначальный (после наведения)
    def set_default_color(self):
        self.image.fill(self.standard_color)
