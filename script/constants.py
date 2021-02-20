# Библиотеки и константы для игры


import pygame  # Основная библиотека (Движок игры)
import sqlite3  # Библиотека для работы с БД
import pytmx  # Библиотека загрузки карт для уровней
import os  # Библиотека для работы с операционной системой
import sys  # Библиотека для работы с файлами
import time  # Библиотека для работы со временем
import random  # Библиотека для работы со случайными значениями

SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE = 1024, 683
STEP = 10
JUMP_STRENGTH = 10
ANIMATION_FPS = 15
FPS = 30
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
GRAVITY = 0.8
SCALE_COEFF = 1.2
FONT_SIZE = 72
DIFFICULTY = {"hard": 15, "medium": 12, "easy": 10, "tutorial": 8}
all_sprites = pygame.sprite.Group()
buttons = pygame.sprite.Group()
font = pygame.font.Font("../data/fonts/thintel.ttf", FONT_SIZE)
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("Irruption")
