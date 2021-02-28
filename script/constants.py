# Библиотеки, константы для игры, глобальные функции и переменные


import pygame  # Основная библиотека (Движок игры)
import sqlite3  # Библиотека для работы с БД
import os  # Библиотека для работы с операционной системой
import sys  # Библиотека для работы с файлами
import time  # Библиотека для работы со временем
import random  # Библиотека для работы со случайными значениями
from moviepy.editor import *


# Функция выключения
def terminate():
    pygame.quit()
    sys.exit()


# Функция загрузки изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('../data/images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Функция, вырезающая кадры со спрайт-листа
def cut_sheet(sheet, columns, rows, obj_width, obj_height):
    frames = []
    rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                       sheet.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            image = pygame.transform.scale(sheet.subsurface(pygame.Rect(
                frame_location, rect.size)), (obj_width, obj_height))
            image = image.convert_alpha()
            frames.append(image)
    return frames


# Функция устанавливающая надпись на кнопке
def set_text(surface, text, font_size=72):
    font_text = pygame.font.Font("../data/fonts/thintel.ttf", font_size)
    text_result = font_text.render(text, True, WHITE)
    screen.blit(text_result, text_result.get_rect(center=surface.rect.center))


# Функция проигрывающая видео в окне, в моём случае видео - это кат-сцены
def play_scene(filename):
    scene = VideoFileClip(filename)
    scene.volumex(0.4)
    scene.preview()
    return


# Функция высчитывающая кадр анимации объекта
def calculate_frame(current_frame, frames):
    current_frame += 1
    if current_frame < len(frames) * ANIMATION_FPS:
        pass
    else:
        current_frame = 0
    return current_frame


# Затухание экрана (Передаётся задержка)
def transition(delay=15):
    for size in range(40):
        black_rect = pygame.Surface((1024, 20 * size))  # - переход сверху - вниз
        black_rect.fill(BLACK)
        screen.blit(black_rect, (black_rect.get_rect(center=screen.get_rect().center)))
        pygame.display.flip()
        pygame.time.delay(delay)


# Функция создания нового профиля для сохранения прогресса
def create_account(identifier, name=None):
    sql_request = "SELECT NAME FROM saves"
    name_list = [str(*i) for i in cursor.execute(sql_request)]
    level = 0
    if name not in name_list:
        sql_request = f"INSERT INTO saves(ID,HERO,NAME,PROGRESS) VALUES({identifier},'None','{name}',{level})"
    else:
        return "unique_error"
    cursor.execute(sql_request)
    return True


# Функция обновления базы данных (сохранение прогресса)
def update_db(identifier, hero=None, level=None):
    sql_requests = [f"UPDATE saves SET HERO = '{hero}' WHERE ID = {identifier}",
                    f"UPDATE saves SET PROGRESS = {level} WHERE ID = {identifier}"]
    for sql_request in sql_requests:
        cursor.execute(sql_request)
    connection.commit()


# Константы для игры:
ACCEPTED_SYMBOLS = "abcdefghijklmnopqrstuvwxyz" \
                   "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
                   "абвгдеёжзийклмнопрстуфхцчшщъыьэюя" \
                   "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ" \
                   "0123456789 _"  # Символы которые игрок может вписывать в поле ввода имени
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE = 1024, 683  # Размеры экрана
STEP = 5  # Количество пикселей на которое передвигается игрок при ходьбе
MAX_MOVE_COUNT = 9  # Макс. кол-во ходов в мини-игре крестики-нолики
MAX_TEXT_LENGTH = 12  # Макс. длина вводимого имени
JUMP_STRENGTH = 10  # Сила прыжка игрока
ANIMATION_FPS = 25  # Кадры анимации в секунду
FPS = 60  # Кадры в секунду (Frame Per Second)
WHITE = pygame.Color("white")  # Белый цвет
BLACK = pygame.Color("black")  # Чёрный цвет
GRAVITY = 0.8  # Сила гравитации
SCALE_COEFFICIENT = 1.2  # Коэффициент увеличения объектов (у меня кнопок)
DIFFICULTY = {"hard": 15, "medium": 12, "easy": 10, "tutorial": 8}  # Соотношение сложности уровня
# и кол-ва платформ на нём
LEVELS = {0: "tutorial", 1: "easy", 2: "medium", 3: "hard"}  # Соотношение номера уровня и сложности на нём
connection = sqlite3.connect("../data/databases/saves.sqlite")  # Подключение к базе данных с сохранёнными играми
cursor = connection.cursor()  # Курсор подключения для работы с БД
all_sprites = pygame.sprite.Group()  # Группа всех спрайтов
buttons = pygame.sprite.Group()  # Группа спрайтов кнопок
player_group = pygame.sprite.Group()  # Группа спрайтов игрока
objects_group = pygame.sprite.Group()  # Группа спрайтов платформ
borders = pygame.sprite.Group()  # Группа спрайтов границ окна
tic_tae_toe = pygame.sprite.Group()  # Группа спрайтов крестиков и ноликов
screen = pygame.display.set_mode(SCREEN_SIZE)  # Объект экрана
clock = pygame.time.Clock()  # Объект часов для отрисовки кадров
pygame.display.set_caption("Irruption")  # Название окна
# Загрузка изображений:
pause_window, settings_window = load_image("window.png"), load_image("window.png")
platform_image = load_image("mini.png")
npc_platform_image = load_image("irbis_platform.png")
dialog_total_frame = load_image("dialog_total_frame.png")
choose_screen = load_image("choose_hero_window.png")
input_box = load_image("input_box.png")
control_window = load_image("control_window.png")
info_screen = load_image("about_authors_screen.png")
bg = load_image("bg.png")
blurred_bg = load_image("blured_bg.png")
# Загрузка спрайт-листов:
bg_frames = cut_sheet(load_image("start_screen.png"), 2, 1, 1024, 683)
long_button_frames = cut_sheet(load_image("buttons.png"), 1, 7, 256, 64)
short_button_frames = cut_sheet(load_image("short_btn.png"), 3, 1, 96, 78)
short_light_button = [load_image("short_light_button.png")]
long_light_button = [load_image("long_light_button.png")]
i_s = cut_sheet(load_image("icons.png"), 5, 2, 74, 71)  # icon_sheet
# (i_s - сокращено для удобной записи в словаре)
icons = {"settings": i_s[0], "pause": i_s[1], "reset": i_s[2], "star": i_s[3],
         "cross": i_s[4], "hp": i_s[5], "cup": i_s[6], "volume_down": i_s[7],
         "volume_up": i_s[8]}
# Игровые диалоги
dialog_texts = [[{"hero": "Привет, кто ты?"},
                 {"bars": "Привет, я Ирбис и это моя территория!"},
                 {"hero": "Ох, извини, я не хочу тревожить тебя..."},
                 {"bars": "Ну что ж... Просто так я тебя не отпущу!"},
                 {"bars": "Знаешь ли, в этих краях очень скучно"},
                 {"bars": "Придётся тебе поиграть со мной!"}]]
pygame.mixer.music.set_volume(0.2)  # Устанавливаем громкость звука
