from game_functions import *

FPS = 60


class Player(pygame.sprite.Sprite):
    # Передаём спрайт-лист с анимацией игрока, количество рядов и колонок на спрайт-листе
    # И отступ от края холста
    def __init__(self, stay_frames, walk_frames, pos):
        super().__init__(player_group)
        self.is_jump = False  # Флаг прыжка
        self.occupation = 0  # Переменная - отвечает за действия игрока
        # 0 - бездействие, 1 - ходьба вправо,
        # 2 - ходьба влево, 3 - прыжок.
        self.deaths = 0
        self.jump_power = JUMP_STRENGTH  # Сила прыжка в определенный момент времени
        self.stay_frames = stay_frames  # Список, с анимацией бездействия игрока
        self.walk_frames = walk_frames  # Список, с анимацией ходьбы игрока
        self.current_frame = 0  # Текущий кадр - нулевой
        self.image = self.stay_frames[self.current_frame]
        self.width = self.image.get_width() // 4  # Ширина игрока
        self.height = self.image.get_height()  # Высота игрока
        self.rect = self.image.get_rect()  # Получаем прямоугольную область игрока
        self.dx = 0
        self.default_x, self.default_y = pos  # Начальные координаты игрока
        self.rect = self.rect.move(*pos)  # Передвигаем игрока на заданную позицию
        self.dx, self.dy = pos  # Переменная позиции игрока

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
                    self.rect.y += (self.jump_power ** 2) // 2
            self.jump_power -= GRAVITY  # Стадия прыжка уменьшается

    # Передвижение игрока в правую сторону
    def walk_right(self):
        if self.rect.x + STEP < WIDTH - self.width * 2:  # Проверяем не касается ли игрок стенок
            self.rect = self.rect.move(STEP, 0)  # Передвигаем игрока вправо на "шаг"
        self.calculate_frame(1)  # Вычисляем кадр анимации
        self.image = self.walk_frames[self.current_frame // ANIMATION_FPS]
        # self.camera_apply()  # Применяем камеру ко всем объектам,
        # чтобы они сместились на расстояние, которое прошёл игрок

    # Передвижение игрока в левую сторону
    def walk_left(self):
        if self.rect.x - STEP > 0:
            self.rect = self.rect.move(-STEP, 0)
        self.calculate_frame(1)  # Вычисляем кадр анимации
        self.image = self.walk_frames[self.current_frame // ANIMATION_FPS]
        self.flip()  # Переворачиваем изображение игрока, т.к. движется влево
        # self.camera_apply()  # Применяем камеру ко всем объектам,
        # чтобы они сместились на расстояние, которое прошёл игрок

    # Перемещает камеру
    def camera_apply(self):
        # Находим смещение игрока
        self.dx += self.dx - self.rect.x
        self.dy += self.dy - self.rect.y
        # Применяем смещение камеры ко всем объектам
        for sprite in objects_group:
            camera.apply(sprite)

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
        if self.rect.y == 0:
            self.deaths += 1
            return
        # Проверка на соприкосновение игрока и объектов (Если коллизий нет, то опускаем игрока)
        if not pygame.sprite.spritecollideany(self, objects_group) and not self.is_jump:
            self.rect.y += (self.jump_power ** 2) // 2  # Опускаем игрока
        # Проверка на нажатие клавиш
        keys = pygame.key.get_pressed()
        if args and keys:
            if keys[pygame.K_SPACE] and not self.is_jump:
                self.is_jump = True
            elif keys[pygame.K_LEFT]:
                self.occupation = 2
            elif keys[pygame.K_RIGHT]:
                self.occupation = 1
            else:
                self.occupation = 0


# Класс, описывающий платформу
class Platform(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y, tile_size):
        super().__init__(objects_group)  # Добавляем платформу в группу объектов
        self.image = image  # Устанавливаем изображение для платформы
        self.rect = self.image.get_rect().move(  # Передвигаем платформу на переданные координаты
            pos_x * tile_size,
            pos_y * tile_size)
        self.abs_pos = (self.rect.x, self.rect.y)  # Устанавливаем позицию, независимую от движения камеры


# Класс, описывающий генерацию уровня
class Level:
    def __init__(self, filename):
        self.map = pytmx.load_pygame(os.path.join('../data/maps', filename))  # Загружаем карту
        self.height, self.width = self.map.height, self.map.width  # Высота и ширина карты
        self.tile_size = self.map.tilewidth  # Размер тайла (квадрата)

    def render(self, screen):  # Передаётся экран, на который отрисовываются объекты
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)  # Изображение тайла
                if image:
                    platform = Platform(image, x, y, self.tile_size)  # Создаём объект платформы

    def get_tile_id(self, position):  # Функция для получения ID тайла
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, 0)]


# Класс, описывающий камеру
class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x = obj.abs_pos[0] + self.dx

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = 0
        self.dy = 0


# Функция запуска мини-игры
def game(hero, lvl):
    stay_parameters = [5, 2, 256, 256]  # Параметры для создания спрайт-листа бездействия игрока
    walk_parameters = [2, 1, 256, 256]  # Параметры для создания спрайт-листа ходьбы игрока
    # Установка игрока
    if hero == "lynx":
        player = Player(
            cut_sheet(load_image("lynx_stay.png"), *stay_parameters),
            cut_sheet(load_image("walking_lynx.png"), *walk_parameters), (0, 1))
    else:
        player = Player(
            cut_sheet(load_image("wolf_stay.png"), *stay_parameters),
            cut_sheet(load_image("walking_wolf.png"), *walk_parameters), (135, 100))
    level = Level(LEVELS[lvl])  # создаём объект уровня
    level.render(screen)
    camera.update(player)  # привязываем игрока к камере (позиционировать камеру на игрока)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            player_group.update(event)
        screen.fill(WHITE)  # Отрисовываем фон каждый цикл
        screen.blit(load_image("background.png"), (0, 0))
        for sprite in objects_group:
            screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))
        player_group.draw(screen)  # Отрисовываем игрока
        player_group.update()  # Обновляем игрока каждый цикл
        # death_count = player.deaths
        # Проверка на то, чем занят игрок
        if player.occupation == 0:
            player.idle()
        if player.occupation == 1:
            player.walk_right()
        if player.occupation == 2:
            player.walk_left()
        if player.is_jump:
            player.jump()
        pygame.display.flip()
        clock.tick(FPS)


player_group = pygame.sprite.Group()
objects_group = pygame.sprite.Group()
death_count = 0
camera = Camera()  # создаём объект камеры
start = time.monotonic()
hero = "wolf"
level_ = 1
# game(hero, level_)
# stop = time.monotonic()
# time_delta = stop - start
# update_db(name, hero, level_, time_delta, death_count)
