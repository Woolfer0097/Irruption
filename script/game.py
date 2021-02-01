from game_functions import *
from constants import *


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
        self.jump_power = JUMP_STRENGTH  # Сила прыжка в определенный момент времени
        self.stay_frames = stay_frames  # Список, с анимацией бездействия игрока
        self.walk_frames = walk_frames  # Список, с анимацией ходьбы игрока
        self.current_frame = 0  # Текущий кадр - нулевой
        self.image = self.stay_frames[self.current_frame]
        self.width = self.image.get_width() // 4  # Ширина игрока
        self.height = self.image.get_height()  # Высота игрока
        self.rect = self.image.get_rect()
        x, y = pos
        self.default_x, self.default_y = x, y  # Начальные координаты игрока
        self.rect = self.rect.move(x, y)
        self.pos = pos

    # Прыжок игрока
    def jump(self):
        if self.jump_power >= -10:  # Проверка на то, не вернулся ли в изначальное положение игрок
            if self.jump_power < 0:  # Проверка на то, достиг ли игрок точки невесомости
                if not pygame.sprite.spritecollideany(self, objects_group):
                    self.rect.y += (self.jump_power ** 2) // 2  # Опускаем игрока
            else:
                if not pygame.sprite.spritecollideany(self, objects_group):
                    self.rect.y -= (self.jump_power ** 2) // 2  # Поднимаем игрока
            self.jump_power -= GRAVITY  # Стадия прыжка уменьшается
        else:
            self.is_jump = False
            self.jump_power = JUMP_STRENGTH

    # Передвижение игрока в правую сторону
    def walk_right(self):
        if self.rect.x + STEP < WIDTH - self.width * 2:
            self.rect = self.rect.move(STEP, 0)
        self.calculate_frame(1)
        self.image = self.walk_frames[self.current_frame // ANIMATION_FPS]
        # self.camera_apply()

    # Передвижение игрока в левую сторону
    def walk_left(self):
        if self.rect.x - STEP > 0:
            self.rect = self.rect.move(-STEP, 0)
        self.calculate_frame(1)
        self.image = self.walk_frames[self.current_frame // ANIMATION_FPS]
        self.flip()
        # self.camera_apply()

    # Перемещает камеру
    def camera_apply(self):
        self.pos = (self.rect.x, self.rect.y)
        for sprite in objects_group:
            camera.apply(sprite)

    # Вычисление текущего кадра (передаётся действие игрока 0 - бездействие, 1 - ходьба)
    def calculate_frame(self, action):
        frames = self.walk_frames if action == 1 else self.stay_frames
        self.current_frame += 1
        if self.current_frame < len(frames) * ANIMATION_FPS:
            pass
        else:
            self.current_frame = 0

    # Игрок бездействует
    def idle(self):
        self.calculate_frame(0)
        self.image = self.stay_frames[self.current_frame // ANIMATION_FPS]

    # Функция, зеркально отражающая изображение игрока
    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)

    # Функция, обновляющая игрока (реализация анимации)
    def update(self, *args):
        self.camera_apply()
        keys = pygame.key.get_pressed()
        if args and keys:
            if keys[pygame.K_SPACE]:
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
        super().__init__(objects_group)
        self.image = image
        self.rect = self.image.get_rect().move(
            pos_x * tile_size, pos_y * tile_size)
        self.abs_pos = (self.rect.x, self.rect.y)


# Класс, описывающий генерацию уровня
class Level:
    def __init__(self, filename):
        self.map = pytmx.load_pygame(os.path.join('../data/maps', filename))
        self.height, self.width = self.map.height, self.map.width
        self.tile_size = self.map.tilewidth

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                image = image = self.map.get_tile_image(x, y, 0)
                if image:
                    platform = Platform(image, x, y, self.tile_size)
                    screen.blit(image, (x * self.tile_size, y * self.tile_size))

    def get_tile_id(self, position):
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, 0)]


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


# Функция запуска мини-игры
def game(hero):
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
            cut_sheet(load_image("walking_wolf.png"), *walk_parameters), (30, 365))
    level = Level("тест.tmx")  # создаём объект уровня
    camera.update(player)  # привязываем игрока к камере (позиционировать камеру на игрока)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            player_group.update(event)
        screen.fill(WHITE)  # Отрисовываем фон каждый цикл
        objects_group.empty()
        objects_group.draw(screen)  # Отрисовываем все объекты
        player_group.draw(screen)  # Отрисовываем игрока
        level.render(screen)
        if player.occupation == 0:
            if not player.is_jump:
                player.idle()
        if player.occupation == 1:
            player.walk_right()
        if player.occupation == 2:
            player.walk_left()
        if player.is_jump:
            player.jump()
        pygame.display.flip()
        clock.tick(FPS)


screen = pygame.display.set_mode(SIZE)
player_group = pygame.sprite.Group()
objects_group = pygame.sprite.Group()
camera = Camera()  # создаём объект камеры
game("wolf")
