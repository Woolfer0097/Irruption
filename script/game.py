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
                    self.rect.y += (self.jump_power ** 2) / 2
            self.jump_power -= GRAVITY  # Стадия прыжка уменьшается

    # Передвижение игрока в правую сторону
    def walk_right(self):
        if self.rect.x + STEP < SCREEN_WIDTH - self.width * 2:  # Проверяем не касается ли игрок стенок
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
        # Проверка на нажатие клавиш
        # for platform in platforms:
        #     if playerman.rect.colliderect(platform.rect):
        #         collide = True
        #         playerman.isJump = False
        #         if (platform.rect.collidepoint(playerman.rect.right, playerman.rect.bottom) or
        #                 platform.rect.collidepoint(playerman.rect.left, playerman.rect.bottom)):
        #             playerman.y = platform.rect.top - playerman.height + 1
        #             playerman.moveright = True
        #             playerman.moveleft = True
        #
        #         if (platform.rect.collidepoint(playerman.rect.right, playerman.rect.top) or
        #                 platform.rect.collidepoint(playerman.rect.right, playerman.rect.bottom - 10)):
        #             playerman.moveright = False
        #         elif (platform.rect.collidepoint(playerman.rect.left, playerman.rect.top) or
        #               platform.rect.collidepoint(playerman.rect.left, playerman.rect.bottom - 10)):
        #             playerman.moveleft = False
        #     else:
        #         playerman.moveright = True
        #         playerman.moveleft = True
        for platform in objects_group:
            if pygame.sprite.spritecollideany(self, objects_group):
                keys = pygame.key.get_pressed()
                if args and keys:
                    if keys[pygame.K_SPACE] and not self.is_jump:
                        self.is_jump = True
                    elif keys[pygame.K_LEFT]:
                        if not platform.rect.collidepoint(self.rect.centerx, self.rect.top) \
                                or not platform.rect.collidepoint(self.rect.centerx, self.rect.bottom - 10):
                            self.occupation = 2
                        else:
                            self.occupation = 0
                    elif keys[pygame.K_RIGHT]:
                        if not platform.rect.collidepoint(self.rect.centerx, self.rect.top) \
                                or not platform.rect.collidepoint(self.rect.centerx, self.rect.bottom - 10):
                            self.occupation = 1
                        else:
                            self.occupation = 0
                    else:
                        self.occupation = 0
            else:
                if not self.is_jump:
                    self.rect.y += (self.jump_power ** 2) // 2


# Класс, описывающий платформу
class Platform(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(objects_group)  # Добавляем платформу в группу объектов
        self.image = image  # Устанавливаем изображение для платформы
        self.rect = self.image.get_rect().move(pos_x, pos_y)  # Передвигаем платформу на переданные координаты
        self.abs_pos = (self.rect.x, self.rect.y)  # Устанавливаем позицию, независимую от движения камеры


class Level(object):
    def __init__(self, difficulty):
        self.level = []
        self.platform_width, self.platform_height = \
            platform_image.get_width(), platform_image.get_height()
        self.difficulty = DIFFICULTY[difficulty]

    def render(self):
        self.generate_level()
        # Перебираем массив и добавляем каждую платформу в группу спрайтов - platform_list
        for platform in self.level:
            x, y = platform
            block = Platform(platform_image, x, y)

    def generate_level(self):
        self.level = [[random.randint(self.platform_width * i,
                                      self.platform_width * i + random.randint(50, 150)),
                       random.randint(SCREEN_HEIGHT - 300, SCREEN_HEIGHT - 185)]
                      for i in range(1, self.difficulty)]
        self.level.insert(0, [0, 500])


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
def frame_generate(hero):
    if hero == "lynx":
        # hero_image = load_image("lynx_avatar.png")
        hero_name = "Рыська"
    else:
        # hero_image = load_image("wolf_avatar.png")
        hero_name = "Волчи"
    # player_frame.blit(hero_image, (0, 0))
    text = font.render(hero_name, True, WHITE)
    player_frame = load_image("player_frame.png")
    player_frame.blit(text, (200 - text.get_width() // 2, text.get_height() // 2))
    return player_frame


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
    paused = False
    buttons.empty()
    level = Level("tutorial")  # создаём объект уровня, передаём сложность
    level.render()
    camera.update(player)  # привязываем игрока к камере (позиционировать камеру на игрока)
    while True:
        if paused:
            buttons.empty()
            volume_on_btn = Button(short_light_button, 375, 471, "", icons["volume_up"])
            volume_off_btn = Button(short_light_button, 567, 471, "", icons["volume_down"])
            exit_btn = Button(long_light_button, 362, 342, "Выход")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONUP:
                    if volume_off_btn.on_hovered(event.pos):
                        transition()
                    if volume_on_btn.on_hovered(event.pos):
                        transition()
                    if exit_btn.on_hovered(event.pos):
                        update_db()
                        transition()
                        start_screen()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    paused = False
            mouse_pos = pygame.mouse.get_pos()
            for btn in buttons:
                if btn.on_hovered(mouse_pos):
                    btn.highlight()
                else:
                    btn.set_default_image()
            screen.blit(blured_bg, (0, 0))
            screen.blit(settings_window, (293, 43))
            text = font.render("Пауза", True, WHITE)
            screen.blit(text, (457, 189))
            buttons.draw(screen)
            buttons.update()
            pygame.display.flip()
            clock.tick(FPS)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE] and not player.is_jump:
                    paused = True
                player_group.update(event)
            # Рисуем задний фон
            screen.fill(WHITE)
            screen.blit(bg, (0, 0))
            player_frame = frame_generate(hero)
            screen.blit(player_frame, (10, 10))
            # Рисуем все платформы из группы спрайтов
            objects_group.draw(screen)
            objects_group.update()
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


pause_window = load_image("window.png")
platform_image = load_image("mini.png")
player_group = pygame.sprite.Group()
objects_group = pygame.sprite.Group()
death_count = 0
camera = Camera()  # создаём объект камеры
start = time.monotonic()
level_ = 1
# game(hero, level_)
# stop = time.monotonic()
# time_delta = stop - start
# update_db(name, hero, level_, time_delta, death_count)
