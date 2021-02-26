# Библиотеки, константы для игры, глобальные функции и переменные


import pygame  # Основная библиотека (Движок игры)
import sqlite3  # Библиотека для работы с БД
import pytmx  # Библиотека загрузки карт для уровней
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


def play_scene(filename):
    scene = VideoFileClip(filename)
    scene.volumex(0.4)
    scene.preview()
    return


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


def name_window():
    pass


def update_db():  # name, hero, level, time_delta, deaths
    pass
    # connection = sqlite3.connect("data/databases/score.sqlite")
    # cursor = connection.cursor()
    # score = (time_delta // deaths) * 100  # Вычисляем текущий счёт игрока
    # sql_requests = [f"UPDATE PROGRESS SET {level} WHERE NAME = {name}",
    #                 f"UPDATE SCORE SET {score} WHERE NAME = {name}"]
    # for sql_request in sql_requests:
    #     cursor.execute(sql_request)


SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE = 1024, 683
STEP = 5
MAX_MOVE_COUNT = 9
JUMP_STRENGTH = 10
ANIMATION_FPS = 20
FPS = 60
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
GRAVITY = 0.8
SCALE_COEFF = 1.2
FONT_SIZE = 72
DIFFICULTY = {"hard": 15, "medium": 12, "easy": 10, "tutorial": 8}
LEVELS = {0: "tutorial", 1: "easy", 2: "medium", 3: "hard"}
all_sprites = pygame.sprite.Group()
buttons = pygame.sprite.Group()
font = pygame.font.Font("../data/fonts/thintel.ttf", FONT_SIZE)
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("Irruption")
player_group = pygame.sprite.Group()
objects_group = pygame.sprite.Group()
borders = pygame.sprite.Group()
tic_tae_toe = pygame.sprite.Group()
death_count = 0
pause_window, settings_window = load_image("window.png"), load_image("window.png")
platform_image = load_image("mini.png")
npc_platform_image = load_image("irbis_platform.png")
dialog_total_frame = load_image("dialog_total_frame.png")
choose_screen = load_image("choose_hero_window.png")
i_s = cut_sheet(load_image("icons.png"), 5, 2, 74, 71)  # icon_sheet
# (i_s - сокращено для удобной записи в словаре)
icons = {"settings": i_s[0], "pause": i_s[1], "reset": i_s[2], "star": i_s[3],
         "cross": i_s[4], "hp": i_s[5], "cup": i_s[6], "volume_down": i_s[7],
         "volume_up": i_s[8]}
texts = [[{"hero": "Привет, кто ты?"}, {"bars": "Привет, я Ирбис и это моя территория!"},
         {"hero": "Ох, извини, я не хочу тревожить тебя..."}, {"bars": "Ну что ж... Просто так я тебя не отпущу!"},
         {"bars": "Знаешь ли, в этих краях очень скучно"}, {"bars": "Придётся тебе поиграть со мной!"}]]
bg_frames = cut_sheet(load_image("start_screen.png"), 2, 1, 1024, 683)
long_button_frames = cut_sheet(load_image("buttons.png"), 1, 7, 256, 64)
short_button_frames = cut_sheet(load_image("short_btn.png"), 3, 1, 96, 78)
short_light_button = [load_image("short_light_button.png")]
long_light_button = [load_image("long_light_button.png")]
control_window = load_image("control_window.png")
info_screen = load_image("about_authors_screen.png")
bg = load_image("bg.png")
blured_bg = load_image("blured_bg.png")
pygame.mixer.music.set_volume(0.2)
