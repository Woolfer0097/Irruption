from constants import *


# Класс, описывающий кнопку
class Button(pygame.sprite.Sprite):
    def __init__(self, frames, x, y, text="", icon=pygame.Surface((0, 0))):
        super(Button, self).__init__(buttons)
        self.frames = frames
        self.icon = icon
        self.image = frames[0]
        self.standard_btn = frames[0]
        self.current_frame = 0
        self.animation_fps = int(ANIMATION_FPS * 1.5)
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = (x, y)
        self.x, self.y = x, y
        self.text = text
        self.hovered = False

    # Функция, устанавливающая иконку
    def set_icon(self):
        screen.blit(self.icon, self.icon.get_rect(center=self.rect.center))

    # Функция увеличивает кнопку (выделяет/подсвечивает)
    def highlight(self):
        self.image = pygame.transform.scale(self.frames[self.current_frame // self.animation_fps],
                                            (int(self.width * SCALE_COEFF),
                                             int(self.height * SCALE_COEFF)))
        self.rect = self.image.get_rect()
        difference_width = (self.width - int(self.width * SCALE_COEFF)) // 2
        difference_height = (self.height - int(self.height * SCALE_COEFF)) // 2
        self.rect.x = self.x + difference_width
        self.rect.y = self.y + difference_height

    # Функция возвращает картинку кнопки в изначальную (после наведения)
    def set_default_image(self):
        self.rect = self.frames[self.current_frame // self.animation_fps].get_rect()
        self.rect.x, self.rect.y = self.pos
        self.hovered = False
        self.image = self.frames[self.current_frame // self.animation_fps]

    # Высчитывает текущий кадр
    def calculate_frame(self):
        self.current_frame += 1
        if self.current_frame < len(self.frames) * self.animation_fps:
            pass
        else:
            self.current_frame = 0

    # Проверяет наведён ли курсор на кнопку
    def on_hovered(self, pos):
        if self.rect.collidepoint(*pos):
            self.hovered = True
            return True
        return False

    # Функция, выполняющаяся каждый цикл (высчитывает текущий кадр, накладывает текст)
    def update(self):
        if self.text:
            set_text(self, self.text)
        if self.icon:
            self.set_icon()
        self.calculate_frame()
        if self.hovered:
            pass
        self.image = self.frames[self.current_frame // self.animation_fps]
