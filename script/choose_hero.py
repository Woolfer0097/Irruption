from game_functions import *
from constants import *


# Класс, описывающий кнопку
class Button(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        super(Button, self).__init__(buttons)
        self.image = img
        self.standard_btn = img
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = (x, y)
        self.x, self.y = x, y

    # Функция увеличивает кнопку
    def highlight(self):
        self.image = pygame.transform.scale(self.standard_btn, (int(self.width * SCALE_COEFF),
                                                                int(self.height * SCALE_COEFF)))
        difference_width = (self.width - int(self.width * SCALE_COEFF)) // 2
        difference_height = (self.height - int(self.height * SCALE_COEFF)) // 2
        self.rect.x = self.x + difference_width
        self.rect.y = self.y + difference_height

    # Функция возвращает картинку кнопки в изначальную (после наведения)
    def set_default_image(self):
        self.image = self.standard_btn
        self.rect.x, self.rect.y = self.pos

    def on_hovered(self, pos):
        if self.rect.collidepoint(*pos):
            return True
        return False
