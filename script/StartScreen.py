from load_functions import *


FPS = 30


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


if __name__ == '__main__':
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    clock = pygame.time.Clock()
    size = width, height = 1024, 768
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    screen.fill(pygame.Color("black"))
    start_screen()
