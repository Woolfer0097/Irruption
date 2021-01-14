from constants import *
from game_functions import *


class Slider(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        super().__init__(all_sprites)
        self.image = pygame.Surface((w, h))
        self.image.fill(pygame.Color(color))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

    def move_slider(self, x):
        self.rect.x = x


def test():
    slider_cursor = Slider(100, 100, 100, 50, "green")
    slider = Slider(100, 100, 10, 100, "red")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONUP:
                if slider_cursor.rect.collidepoint(event.pos):
                    slider.move_slider(event.pos[0])
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    test()
