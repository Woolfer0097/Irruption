import pygame
import sys
import os


class LoadSprites:
    # создание поля
    def __init__(self, filename):
        self.filename = filename
        self.spritesheet = load_image(filename)
        self.left = 0
        self.top = 0
        self.cell_size = 128

    def get_sprite(self, cell):
        x, y = cell
        sprite = pygame.Surface((self.cell_size, self.cell_size))
        sprite.set_colorkey(pygame.Color("black"))
        sprite.blit(self.spritesheet, (0, 0), (x * self.cell_size, y * self.cell_size,
                                               self.cell_size, self.cell_size))
        return sprite


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1280, 1280
    screen = pygame.display.set_mode(size)
    my_spritesheet = LoadSprites("images/sprite_sheet_final#2.png")
    wolf_sprites = [my_spritesheet.get_sprite((i, 2)) for i in range(10)]
    print(wolf_sprites)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(wolf_sprites)):
                    screen.blit(wolf_sprites[i], (i * 128, 0))
        pygame.display.flip()