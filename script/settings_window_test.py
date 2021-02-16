import pygame

FPS = 30


def settings_window():
    pass


if __name__ == '__main__':
    screen = pygame.display.set_mode((1024, 683))
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(pygame.Color("white"))
        settings_window()
        pygame.display.flip()
        clock.tick(FPS)
