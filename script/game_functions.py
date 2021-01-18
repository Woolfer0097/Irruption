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


# Функция запуска начального экрана
def start_screen():
    bg = load_image("images/main_menu.png")
    start_btn = Button(300, 100, 100, 100)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEMOTION:
                if start_btn.on_hovered(event.pos):
                    print("Наведено")
            elif event.type == pygame.MOUSEBUTTONUP:
                if start_btn.on_hovered(event.pos):
                    return
        screen.blit(bg, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
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

