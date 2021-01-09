import pygame
import os
import sys
from PyQt5 import Qt

WIDTH, HEIGHT = SIZE = 1024, 1024
FPS = 30
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)
