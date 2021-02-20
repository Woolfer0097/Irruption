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


# Затухание экрана (Передаётся задержка)
def transition(delay=15):
    for size in range(40):
        black_rect = pygame.Surface((1024, 20 * size))  # - переход сверху - вниз
        black_rect.fill(BLACK)
        screen.blit(black_rect, (black_rect.get_rect(center=screen.get_rect().center)))
        pygame.display.flip()
        pygame.time.delay(delay)


def name_window():
    pass


def update_db():  # name, hero, level, time_delta, deaths
    pass
    # connection = sqlite3.connect("data/databases/score.sqlite")
    # cursor = connection.cursor()
    # score = (time_delta // deaths) * 100  # Вычисляем текущий счёт игрока
    # sql_requests = [f"UPDATE PROGRESS SET {level} WHERE NAME = {name}",
    #                 f"UPDATE SCORE SET {score} WHERE NAME = {name}"]
    # for sql_request in sql_requests:
    #     cursor.execute(sql_request)


# Функция запуска начального экрана
def start_screen():
    current_frame = 0
    settings_flag = False
    control_flag = False
    buttons.empty()
    while True:
        if settings_flag:
            buttons.empty()
            volume_on_btn = Button(short_light_button, 375, 471, "", icons["volume_up"])
            volume_off_btn = Button(short_light_button, 567, 471, "", icons["volume_down"])
            control = Button(long_light_button, 362, 342, "Управление")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONUP:
                    if volume_off_btn.on_hovered(event.pos):
                        transition()
                    if volume_on_btn.on_hovered(event.pos):
                        transition()
                    if control.on_hovered(event.pos):
                        control_flag = True
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    if control_flag:
                        control_flag = False
                    else:
                        settings_flag = False
                        control_flag = False
            mouse_pos = pygame.mouse.get_pos()
            for btn in buttons:
                if btn.on_hovered(mouse_pos):
                    btn.highlight()
                else:
                    btn.set_default_image()
            screen.blit(blured_bg, (0, 0))
            if control_flag:
                screen.blit(control_window, (0, 0))
            else:
                screen.blit(settings_window, (293, 43))
                text = font.render("Настройки", True, WHITE)
                screen.blit(text, (416, 189))
                buttons.draw(screen)
                buttons.update()
            pygame.display.flip()
            clock.tick(FPS)
        else:
            buttons.empty()
            start_btn = Button(long_button_frames, 384, 310, "Играть")
            info_btn = Button(long_button_frames, 384, 406, "Об авторах")
            exit_btn = Button(long_button_frames, 384, 502, "Выход")
            settings_btn = Button(short_button_frames, 910, 584, "", icons["settings"])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONUP:
                    if start_btn.on_hovered(event.pos):
                        transition()
                        return 0
                    if info_btn.on_hovered(event.pos):
                        transition()
                        return 1
                    if exit_btn.on_hovered(event.pos):
                        transition()
                        terminate()
                    if settings_btn.on_hovered(event.pos):
                        settings_flag = True
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


i_s = cut_sheet(load_image("icons.png"), 5, 2, 74, 71)  # icon_sheet
# (i_s - сокращено для удобной записи в словаре)
icons = {"settings": i_s[0], "pause": i_s[1], "reset": i_s[2], "star": i_s[3],
         "cross": i_s[4], "hp": i_s[5], "cup": i_s[6], "volume_down": i_s[7],
         "volume_up": i_s[8]}
bg_frames = cut_sheet(load_image("start_screen.png"), 2, 1, 1024, 683)
long_button_frames = cut_sheet(load_image("buttons.png"), 1, 7, 256, 64)
short_button_frames = cut_sheet(load_image("short_btn.png"), 3, 1, 96, 78)
short_light_button = [load_image("short_light_button.png")]
long_light_button = [load_image("long_light_button.png")]
control_window = load_image("control_window.png")
settings_window = load_image("window.png")
pause_window = load_image("window.png")
bg = load_image("bg.png")
blured_bg = load_image("blured_bg.png")
