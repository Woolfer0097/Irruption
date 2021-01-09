from game_functions import *
from constants import *


class AnimatedPlayer(pygame.sprite.Sprite):
    # Передаём спрайт-лист с анимацией игрока, количество рядов и колонок на спрайт-листе
    # И отступ от края холста
    def __init__(self, stay_frames, walk_frames):
        super().__init__(player_group)
        self.jump = False  # Флаг прыжка
        # self.direction = 0  # Направление игрока 0 - вправо, 1 - влево
        self.stay_frames = stay_frames  # Список, с анимацией бездействия игрока
        self.walk_frames = walk_frames  # Список, с анимацией ходьбы игрока
        self.current_frame = 0  # Текущий кадр - нулевой
        self.image = self.stay_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(0, 0)

    # Передвижение игрока в правую сторону
    def walk_right(self):
        self.rect = self.rect.move(0.5, 0)
        self.current_frame += 1
        if self.current_frame < len(self.walk_frames):
            pass
        else:
            self.current_frame = 0
        self.image = self.walk_frames[self.current_frame]

    # Передвижение игрока в левую сторону
    def walk_left(self):
        self.rect = self.rect.move(-0.5, 0)
        self.current_frame += 1
        if self.current_frame < len(self.walk_frames):
            pass
        else:
            self.current_frame = 0
        self.image = self.walk_frames[self.current_frame]
        self.flip()

    # Игрок бездействует
    def idle(self):
        self.current_frame += 1
        if self.current_frame < len(self.stay_frames):
            pass
        else:
            self.current_frame = 0
        self.image = self.stay_frames[self.current_frame]

    # Игрок прыгает
    def jumping(self):
        self.jump = True

    # Функция, обновляющая игрока (реализация анимации)
    def update(self, *args):
        if args and args[0].type == pygame.KEYDOWN:
            if not self.jump:
                if args[0].key == pygame.K_UP:
                    self.jumping()
                if args[0].key == pygame.K_LEFT:
                    self.walk_left()
                if args[0].key == pygame.K_RIGHT:
                    self.walk_right()

    # Функция, зеркально отражающая изображение игрока
    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)


class Platform(pygame.sprite.Sprite):
    def __init__(self, w, h, x, y):
        super().__init__(objects_group)
        self.image = pygame.Surface((w, h))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Функция запуска мини-игры
def game(hero):
    if hero == "lynx":
        player = AnimatedPlayer(
            [load_image(os.path.join("images", "lynx_stay.png")), 5, 2, 0, 0],
            [load_image(os.path.join("images", "walking_lynx.png")), 2, 1, 0, 0])
    else:
        player = AnimatedPlayer(
            [load_image(os.path.join("images", "wolf_stay.png")), 5, 2, 0, 0],
            [load_image(os.path.join("images", "walking_wolf.png")), 2, 1, 0, 0])
    animation = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill(pygame.Color("black"))
        player_group.draw(screen)
        objects_group.draw(screen)
        player_group.update()
        pygame.display.flip()
        clock.tick(FPS)


# Функция, вырезающая кадры со спрайт-листа
def cut_sheet(sheet, columns, rows):
    frames = []
    rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                       sheet.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            frames.append(sheet.subsurface(pygame.Rect(
                frame_location, rect.size)))
    return frames


player_group = pygame.sprite.Group()
objects_group = pygame.sprite.Group()
game("lynx")
