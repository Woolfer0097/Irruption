from constants import *
from button import Button


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
def cut_sheet(sheet, columns, rows, obj_width, obj_height):
    frames = []
    rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                       sheet.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            frames.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(
                frame_location, rect.size)), (obj_width, obj_height)))
    return frames


def calculate_frame(current_frame, frames):
    current_frame += 1
    if current_frame < len(frames) * ANIMATION_FPS:
        pass
    else:
        current_frame = 0
    return current_frame


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
    current_frame = 0
    bg_frames = cut_sheet(load_image("start_screen.png"), 2, 1, 1024, 683)
    button_frames = cut_sheet(load_image("buttons.png"), 1, 7, 256, 64)
    start_btn = Button(button_frames, 381, 320, "Играть")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONUP:
                if start_btn.on_hovered(event.pos):
                    return
        mouse_pos = pygame.mouse.get_pos()
        for btn in buttons:
            if btn.on_hovered(mouse_pos):
                btn.highlight()
            else:
                btn.set_default_image()
        screen.blit(bg_frames[current_frame // ANIMATION_FPS], (0, 0))
        current_frame = calculate_frame(current_frame, bg_frames)
        buttons.draw(screen)
        buttons.update()
        pygame.display.flip()
        clock.tick(FPS)


# Функция запускающая экран выбора персонажей
def choose_hero():
    all_sprites.empty()
    screen.fill(pygame.Color("black"))
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

