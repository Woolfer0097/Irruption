import pygame
import os
import sys
from PyQt5 import Qt

WIDTH, HEIGHT = SIZE = 1024, 768
FPS = 30
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
GRAVITY = 1
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)
