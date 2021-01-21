from constants import *
from choose_hero import Button


# Функция выключения
def terminate():
    pygame.quit()
    sys.exit()


# Функция загрузки изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('../data/images', name)
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


# Функция, вырезающая кадры со спрайт-листа
def cut_sheet(sheet, columns, rows):
    frames = []
    rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                       sheet.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            frames.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(
                frame_location, rect.size)), (256, 256)))
    return frames


# Затухание экрана
def fading(delay):
    for opacity in range(255, 0, -15):
        print(opacity)
        working_surface = pygame.Surface((1024, 768), pygame.SRCALPHA, 32)
        working_surface.fill((0, 0, 0, opacity))
        screen.blit(working_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(delay)


# Функция запуска начального экрана
def start_screen():
    bg = load_image("main_menu.png")
    start_btn = Button(load_image("start_btn.png"), 381, 326)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                if start_btn.on_hovered(event.pos):
                    start_btn.highlight()
                else:
                    start_btn.set_default_image()
            if event.type == pygame.MOUSEBUTTONUP:
                if start_btn.on_hovered(event.pos):
                    return
        screen.blit(bg, (0, 0))
        buttons.draw(screen)
        buttons.update()
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

