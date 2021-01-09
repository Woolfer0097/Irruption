from constants import *
from choose_hero import Button


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('../data', name)
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


def get_size_of_desktop():
    desktop = Qt.QApplication(sys.argv).desktop()
    return desktop.width(), desktop.height()


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


# Функция запускающая экран выбора персонажей
def choose_hero():
    all_sprites.empty()
    screen.fill(pygame.Color("black"))
    button_wolf = Button(50, 250, 200, 50)
    button_lynx = Button(700, 250, 200, 50)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONUP:
                for button in all_sprites:
                    if button.rect.collidepoint(event.pos):
                        return
            elif event.type == pygame.MOUSEMOTION:
                for button in all_sprites:
                    if button.rect.collidepoint(event.pos):
                        button.highlight()
                    else:
                        button.set_default_color()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

