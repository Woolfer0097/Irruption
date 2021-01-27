from game_functions import *
from constants import *


# Класс, описывающий кнопку
class Button(pygame.sprite.Sprite):
    def __init__(self, frames, x, y, text=""):
        super(Button, self).__init__(buttons)
        self.frames = frames
        self.image = frames[0]
        self.standard_btn = frames[0]
        self.current_frame = 0
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = (x, y)
        self.x, self.y = x, y
        self.text = text
        self.hovered = False

    # Функция устанавливающая надпись на кнопке
    def set_text(self):
        font = pygame.font.Font("../data/fonts/thintel.ttf", FONT_SIZE)
        text = font.render(self.text, True, WHITE)
        screen.blit(text, text.get_rect(center=self.rect.center))

    # Функция увеличивает кнопку (выделяет/подсвечивает)
    def highlight(self):
        self.image = pygame.transform.scale(self.frames[self.current_frame // ANIMATION_FPS],
                                            (int(self.width * SCALE_COEFF),
                                             int(self.height * SCALE_COEFF)))
        difference_width = (self.width - int(self.width * SCALE_COEFF)) // 2
        difference_height = (self.height - int(self.height * SCALE_COEFF)) // 2
        self.rect.x = self.x + difference_width
        self.rect.y = self.y + difference_height

    # Функция возвращает картинку кнопки в изначальную (после наведения)
    def set_default_image(self):
        self.rect.x, self.rect.y = self.pos
        self.hovered = False
        self.image = self.frames[self.current_frame // ANIMATION_FPS]

    def calculate_frame(self):
        self.current_frame += 1
        if self.current_frame < len(self.frames) * ANIMATION_FPS:
            pass
        else:
            self.current_frame = 0

    def on_hovered(self, pos):
        if self.rect.collidepoint(*pos):
            self.hovered = True
            return True
        return False

    def update(self):
        self.set_text()
        self.calculate_frame()
        if self.hovered:
            pass
        else:
            self.image = self.frames[self.current_frame // ANIMATION_FPS]
