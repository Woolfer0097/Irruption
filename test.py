from moviepy.editor import *
import pygame

pygame.display.set_caption('Видео')

clip = VideoFileClip(r"data/katstsena1.mp4")
clip.preview()

pygame.quit()

#
class LoadSprites:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.spritesheet = load_image("images/sprite_sheet_final#2.png")
        self.left = 0
        self.top = 0
        self.cell_size = 128

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, (255, 255, 255), (self.cell_size * x + self.left,
                                                           self.top + self.cell_size * y,
                                                           self.cell_size, self.cell_size),
                                 1)
        screen.blit(self.spritesheet, (1, 10))

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        return ((mouse_pos[0] - self.left) // self.cell_size,
                (mouse_pos[1] - self.top) // self.cell_size)

    def on_click(self, cell_coords):
        if self.width > cell_coords[0] >= 0 and self.height > cell_coords[1] >= 0:
            self.get_sprite(cell_coords)
        else:
            pass

    def get_sprite(self, cell):
        x, y = cell
        sprite = pygame.Surface((self.cell_size, self.cell_size))
        sprite.set_colorkey(pygame.Color("black"))
        sprite.blit(self.spritesheet, (0, 0), (x, y, self.cell_size, self.cell_size))
        return sprite
