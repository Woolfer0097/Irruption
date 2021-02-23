from constants import *


class Player(pygame.sprite.Sprite):
    # Передаём спрайт-лист с анимацией игрока, количество рядов и колонок на спрайт-листе
    # И отступ от края холста
    def __init__(self, stay_frames, walk_frames, pos):
        super().__init__(player_group)
        self.is_jump = False  # Флаг прыжка
        self.camera_stop = False
        self.occupation = 0  # Переменная - отвечает за действия игрока
        # 0 - бездействие, 1 - ходьба вправо,
        # 2 - ходьба влево, 3 - прыжок.
        self.deaths = 0
        self.jump_power = JUMP_STRENGTH  # Сила прыжка в определенный момент времени
        self.stay_frames = stay_frames  # Список, с анимацией бездействия игрока
        self.walk_frames = walk_frames  # Список, с анимацией ходьбы игрока
        self.current_frame = 0  # Текущий кадр - нулевой
        self.image = self.stay_frames[self.current_frame]
        self.rect = pygame.Rect(*pos, 184, 240)  # Получаем прямоугольную область игрока
        self.width = self.rect.width  # Ширина игрока
        self.height = self.rect.height  # Высота игрока
        self.x, self.y = pos
        self.pos = pos
        self.rect = self.rect.move(*self.pos)  # Передвигаем игрока на заданную позицию

    # Прыжок игрока
    def jump(self):
        if self.is_jump:  # Проверка на то, не вернулся ли в изначальное положение игрок
            if self.jump_power > 2:
                self.rect.y -= (self.jump_power ** 2) / 2  # Поднимаем игрока
            else:
                if pygame.sprite.spritecollideany(self, objects_group):
                    self.is_jump = False
                    self.jump_power = JUMP_STRENGTH
                else:
                    self.rect.y += (self.jump_power ** 2) / 2
            self.jump_power -= GRAVITY  # Стадия прыжка уменьшается

    # Передвижение игрока в правую сторону
    def walk_right(self):
        if self.camera_stop:
            self.rect.x += STEP
        self.calculate_frame(1)  # Вычисляем кадр анимации
        self.image = self.walk_frames[self.current_frame // ANIMATION_FPS]
        # self.camera_apply()  # Применяем камеру ко всем объектам,
        # чтобы они сместились на расстояние, которое прошёл игрок

    # Передвижение игрока в левую сторону
    def walk_left(self):
        if self.camera_stop:
            self.rect.x -= STEP
        self.calculate_frame(1)  # Вычисляем кадр анимации
        self.image = self.walk_frames[self.current_frame // ANIMATION_FPS]
        self.flip()  # Переворачиваем изображение игрока, т.к. движется влево
        # self.camera_apply()  # Применяем камеру ко всем объектам,
        # чтобы они сместились на расстояние, которое прошёл игрок

    # Вычисление текущего кадра (передаётся действие игрока 0 - бездействие, 1 - ходьба)
    def calculate_frame(self, action):
        frames = self.walk_frames if action == 1 else self.stay_frames  # Определяем список кадров
        self.current_frame += 1  # Увеличиваем счётчик кадров на 1
        # Проверка на выход из списка кадров (Если выходит, то обнуляем счётчик)
        if self.current_frame < len(frames) * ANIMATION_FPS:
            pass
        else:
            self.current_frame = 0  # Обнуляем счётчик

    # Игрок бездействует
    def idle(self):
        self.calculate_frame(0)  # Вычисляем кадр анимации
        self.image = self.stay_frames[self.current_frame // ANIMATION_FPS]

    # Функция, зеркально отражающая изображение игрока
    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)

    # Функция, обновляющая игрока (реализация анимации)
    def update(self, *args):
        # pygame.draw.rect(screen, WHITE, self.rect, 1)
        for platform in objects_group:
            # pygame.draw.rect(screen, WHITE, platform.rect, 1)i
            if pygame.sprite.spritecollideany(self, objects_group):
                keys = pygame.key.get_pressed()
                if args and keys:
                    if keys[pygame.K_SPACE] and not self.is_jump:
                        self.is_jump = True
                    elif keys[pygame.K_LEFT]:
                        if not pygame.sprite.collide_mask(self, platform):
                            self.occupation = 2
                    elif keys[pygame.K_RIGHT]:
                        if not pygame.sprite.collide_mask(self, platform):
                            self.occupation = 1
                    else:
                        self.occupation = 0
            else:
                if not self.is_jump:
                    self.occupation = 0
                    self.rect.y += (self.jump_power ** 2) // 2


# Класс, описывающий платформу
class Platform(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(objects_group)  # Добавляем платформу в группу объектов
        self.image = image  # Устанавливаем изображение для платформы
        self.rect = self.image.get_rect().move(pos_x, pos_y)  # Передвигаем платформу на переданные координаты
        self.abs_pos = (pos_x, pos_y)  # Устанавливаем позицию, независимую от движения камеры
        self.mask = pygame.mask.from_surface(self.image)


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Level(object):
    def __init__(self, difficulty):
        self.level = []
        self.platform_width, self.platform_height = \
            platform_image.get_width(), platform_image.get_height()
        self.difficulty = DIFFICULTY[difficulty]
        self.level_start = 0
        self.level_length = 0

    def render(self):
        self.generate_level()
        # Перебираем массив и добавляем каждую платформу в группу спрайтов - platform_list
        for platform in self.level:
            x, y = platform
            Platform(platform_image, x, y)
        Platform(npc_platform_image,
                 self.platform_width * self.difficulty + 200, 400)

    def generate_level(self):
        self.level = [[random.randint(self.platform_width * i + 150,
                                      self.platform_width * i + 160),
                       random.randint(SCREEN_HEIGHT - 300, SCREEN_HEIGHT - 186)]
                      for i in range(1, self.difficulty)]
        self.level_length = self.platform_width * (self.difficulty - 1)
        self.level.insert(0, [0, 500])


# Класс, описывающий камеру
class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x = obj.abs_pos[0] + self.dx

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = 0
