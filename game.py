import pygame
import os
from load_functions import *


SPEED = 20
FPS = 15


def game():
    hero = Hero(all_sprites, "wolf")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            screen.fill(pygame.Color("black"))
            hero.update(event)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)


class Hero(pygame.sprite.Sprite):
    def __init__(self, sprites, hero):
        super().__init__(sprites)
        self.animation_step = 0
        self.pos = self.x, self.y = (0, 800)
        if hero == "wolf":
            self.hero_sprites_stay = wolf_sprites
            self.hero_sprites_walk = wolf_walk_sprites
        else:
            self.hero_sprites_stay = cat_sprites
            self.hero_sprites_walk = cat_walk_sprites

    def update(self, *args):
        keys = pygame.key.get_pressed()
        if args and args[0].type == pygame.KEYDOWN:
            self.animation_step = 0
            if keys[pygame.K_LEFT]:
                self.animation_step += 1
                if self.x - SPEED > 0:
                    self.x -= SPEED
                screen.blit(pygame.transform.flip(
                    self.hero_sprites_walk[self.animation_step // 5],
                    True, False), (self.x - 20, self.y))
            elif keys[pygame.K_RIGHT]:
                self.animation_step += 1
                if self.x + SPEED < 1024:
                    self.x += SPEED
                screen.blit(self.hero_sprites_walk[self.animation_step // 5], self.pos)
            if self.animation_step >= 10:
                self.animation_step = 0
        else:
            if self.animation_step >= 50:
                self.animation_step = 0
            screen.fill(pygame.Color("black"))
            screen.blit(self.hero_sprites_stay[self.animation_step // 5], self.pos)
            self.animation_step += 1


if __name__ == '__main__':
    pygame.init()
    os.environ['SDL_VIDEO_TOP'] = '1'
    clock = pygame.time.Clock()
    size = width, height = 1024, 1024
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    my_spritesheet = LoadSprites("images/sprite_sheet_final#2.png")
    wolf_sprites = [my_spritesheet.get_sprite((i, 0)) for i in range(10)]
    wolf_walk_sprites = [my_spritesheet.get_sprite((i, 1)) for i in range(2)]
    cat_sprites = [my_spritesheet.get_sprite((i, 2)) for i in range(10)]
    cat_walk_sprites = [my_spritesheet.get_sprite((i, 3)) for i in range(2)]
    screen.fill(pygame.Color("black"))
    game()
