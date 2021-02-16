# Библиотеки и константы для игры


import pygame  # Основная библиотека (Движок игры)
import sqlite3  # Библиотека для работы с БД
import pytmx  # Библиотека загрузки карт для уровней
import os  # Библиотека для работы с операционной системой
import sys  # Библиотека для работы с файлами
import time  # Библиотека для работы со временем

WIDTH, HEIGHT = SIZE = 1024, 683
STEP = 10
JUMP_STRENGTH = 10
ANIMATION_FPS = 15
FPS = 30
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
GRAVITY = 0.8
SCALE_COEFF = 1.2
FONT_SIZE = 72
LEVELS = {1: "безымянный.tmx", 2: "level_2.tmx", 3: "level_3.tmx"}
all_sprites = pygame.sprite.Group()
buttons = pygame.sprite.Group()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("Irruption")
