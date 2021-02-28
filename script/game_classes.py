from constants import *


class Player(pygame.sprite.Sprite):
    # Передаём спрайт-лист с анимацией игрока, количество рядов и колонок на спрайт-листе
    # И отступ от края холста
    def __init__(self, stay_frames, walk_frames, pos, npc=False):
        super().__init__(player_group)
        self.is_jump = False  # Флаг прыжка
        self.camera_stop = False
        self.npc = npc
        self.occupation = 0  # Переменная - отвечает за действия игрока
        # 0 - бездействие, 1 - ходьба вправо,
        # 2 - ходьба влево, 3 - прыжок.
        self.deaths = 0
        self.jump_power = JUMP_STRENGTH  # Сила прыжка в определенный момент времени
        self.stay_frames = stay_frames  # Список, с анимацией бездействия игрока
        if walk_frames:
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
        if self.npc:
            self.idle()
        else:
            # pygame.draw.rect(screen, WHITE, self.rect, 1) - Хитбокс игрока
            for platform in objects_group:
                # pygame.draw.rect(screen, WHITE, platform.rect, 1) - Хитбокс платформ
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
                        self.rect.y += 2


# Класс, описывающий платформу
class Platform(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(objects_group)  # Добавляем платформу в группу объектов
        self.image = image  # Устанавливаем изображение для платформы
        self.rect = self.image.get_rect().move(pos_x, pos_y)  # Передвигаем платформу на переданные координаты
        self.abs_pos = (pos_x, pos_y)  # Устанавливаем позицию, независимую от движения камеры
        self.mask = pygame.mask.from_surface(self.image)


# Класс, описывающий границу экрана
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


# Класс, описывающий объект уровня
class Level(object):
    def __init__(self, difficulty):
        self.level = []
        self.platform_width, self.platform_height = \
            platform_image.get_width(), platform_image.get_height()
        self.difficulty = DIFFICULTY[difficulty]
        self.level_start = 0
        self.level_length = 0

    # Отрисовка уровня
    def render(self):
        self.generate_level()
        # Перебираем массив и добавляем каждую платформу в группу спрайтов - platform_list
        for platform in self.level:
            x, y = platform
            Platform(platform_image, x, y)
        Platform(npc_platform_image,
                 self.level_length + 450, 400)

    # Генерация уровня
    def generate_level(self):
        self.level = [[random.randint(self.platform_width * 1.5 * i,
                                      self.platform_width * 1.5 * i + PLATFORM_DIFFERENT),
                       random.randint(SCREEN_HEIGHT - 300, SCREEN_HEIGHT - 186)]
                      for i in range(1, self.difficulty)]
        self.level_length = self.level[-1][0]
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


# Класс доски для игры в крестики-нолики
class Board(pygame.sprite.Sprite):
    def __init__(self, width, height, left, top):
        super().__init__(tic_tae_toe)
        self.width = width
        self.height = height
        self.board = [[" "] * width for _ in range(height)]
        self.step = 0
        self.cell_size = 124
        self.left = left
        self.top = top
        self.cross_image = load_image("player_symbol.png")
        self.zero_image = load_image("irbis_symbol.png")
        self.screen = load_image("mini_game_frame.png")
        self.coord_ratio = {(0, 0): 0, (0, 1): 1, (0, 2): 2,
                            (1, 0): 3, (1, 1): 4, (1, 2): 5,
                            (2, 0): 6, (2, 1): 7, (2, 2): 8}
        self.win_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                 (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                 (0, 4, 8), (2, 4, 6)]

    # Отрисовка
    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                # pygame.draw.rect(self.screen, WHITE, (self.cell_size * x + 33,           |
                #                                       self.cell_size * y + 119,          |Отрисовка границ
                #                                       self.cell_size, self.cell_size), 2)|
                if self.board[y][x] == "X":
                    x_figure, y_figure = self.cell_size * x + 33, 119 + self.cell_size * y
                    self.screen.blit(self.cross_image, (x_figure, y_figure))
                elif self.board[y][x] == "O":
                    x_figure, y_figure = self.cell_size * x + 33, 119 + self.cell_size * y
                    self.screen.blit(self.zero_image, (x_figure, y_figure))

    # Обработка клика
    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        return self.on_click(cell)

    # Получаем клетку
    def get_cell(self, mouse_pos):
        return ((mouse_pos[0] - (self.left + 33)) // self.cell_size,
                (mouse_pos[1] - (self.top + 119)) // self.cell_size)

    # Проверка клика
    def on_click(self, cell_coordinates):
        if self.width > cell_coordinates[0] >= 0 and self.height > cell_coordinates[1] >= 0:
            return cell_coordinates
        else:
            pass

    # Ход игрока
    def player_step(self, cell_coords):
        coordinates = self.get_click(cell_coords)
        if coordinates:
            x, y = coordinates
            for j in range(self.width):
                for i in range(self.height):
                    if j == x and i == y:
                        if self.board[i][j] != "X" and self.board[i][j] != "O":
                            self.board[i][j] = "X"
                            self.step += 1
                            return True
                        else:
                            return False
        else:
            pass

    # Проверка выигрыша
    def check_win(self):
        for x in range(self.width):
            for i, coord in enumerate(self.win_combinations):
                y1, x1 = self.get_key(coord[0])
                y2, x2 = self.get_key(coord[1])
                y3, x3 = self.get_key(coord[2])
                if self.board[x1][y1] == self.board[x2][y2] == self.board[x3][y3]:
                    return self.board[x1][y1]
        if self.step == 9:
            return "draw"
        return False

    # Ход компьютера
    def ai_step(self):  # artificial intellect`s step
        x, y = self.get_key(random.randint(0, 8))
        if self.board[x][y] != "X" and self.board[x][y] != "O":
            self.board[x][y] = "O"
            self.step += 1
        else:
            self.ai_step()

    # Взятие ключа словаря по значению
    def get_key(self, value_need):
        for key, value in self.coord_ratio.items():
            if value == value_need:
                return key


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
                                            (int(self.width * SCALE_COEFFICIENT),
                                             int(self.height * SCALE_COEFFICIENT)))
        self.rect = self.image.get_rect()
        difference_width = (self.width - int(self.width * SCALE_COEFFICIENT)) // 2
        difference_height = (self.height - int(self.height * SCALE_COEFFICIENT)) // 2
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
        self.calculate_frame()
        self.image = self.frames[self.current_frame // self.animation_fps]
        if self.text:
            set_text(self, self.text)
        if self.icon:
            self.set_icon()


# Класс, описывающий Поле для ввода текста
class TextBox(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super(TextBox, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.set_position()

    def set_position(self):
        self.rect.x = self.x
        self.rect.y = self.y


class InfoLabel(pygame.sprite.Sprite):
    def __init__(self, image, x):
        super(InfoLabel, self).__init__(info_labels)
        self.image = image
        self.default_image = image
        self.data = get_info()
        self.hero_avatar = None
        self.name = ""
        self.hero = ""
        self.level = 0
        self.rect = self.image.get_rect()
        self.dy = 0
        self.x = x
        self.length = 0
        self.set_position()

    def set_position(self):
        self.rect.x = self.x

    def scroll_down(self):
        self.dy += 20

    def scroll_up(self):
        self.dy -= 20

    def render(self):
        for i in range(len(self.data)):
            self.image.fill(BLACK)
            self.hero = self.data[i][1]
            self.name = self.data[i][2]
            self.level = self.data[i][3]
            if self.hero == "wolf":
                self.hero_avatar = load_image("wolf_avatar.png")
            elif self.hero == "lynx":
                self.hero_avatar = load_image("lynx_avatar.png")
            avatar_frame = load_image("avatar_frame.png")
            avatar_frame.blit(self.hero_avatar, (-6, -6))
            self.image.blit(pygame.transform.scale(avatar_frame, (68, 68)), (10, 10))
            font_text = pygame.font.Font("../data/fonts/thintel.ttf", 48)
            text = font_text.render(self.name, True, WHITE)
            self.image.blit(text, (120, 10))
            text = font_text.render(str(self.level), True, WHITE)
            self.image.blit(text, (500, 10))
            screen.blit(self.image, (self.rect.x, ((self.image.get_height() + 20) * i + 100) + self.dy))
        self.length = -((self.image.get_height() + 20) * len(self.data))
