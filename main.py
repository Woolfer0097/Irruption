from moviepy.editor import *
import os
import pygame
from load_functions import *

WIDTH, HEIGHT = 1024, 1024
FPS = 30


# class StartButton(pygame.sprite.Sprite):
#     def __init__(self, all_sprites):
#         super.__init__(all_sprites)


def start_screen():
    bg = load_image("images/start_screen.png")
    screen.blit(bg, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def play_scene(filename):
    clip = VideoFileClip(filename)
    clip.preview()
    return


if __name__ == '__main__':
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color("black"))
    start_screen()
    # play_scene("data/katstsena1.mp4")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(wolf_sprites)):
                    screen.blit(cat_sprites[i], (i * 128, 0))
        pygame.display.flip()
