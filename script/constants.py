import pygame
import pygame_gui
import os
import sys
import time
from PyQt5 import Qt

WIDTH, HEIGHT = SIZE = 1024, 768
STEP = 10
JUMP_STRENGTH = 10
ANIMATION_FPS = 15
FPS = 30
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
GRAVITY = 1
SCALE_COEFF = 1.2
all_sprites = pygame.sprite.Group()
buttons = pygame.sprite.Group()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("Irruption")
