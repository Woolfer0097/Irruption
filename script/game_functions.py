from game import *
from button import Button


# Функция выключения
def terminate():
    pygame.quit()
    sys.exit()


def play_scene(filename):
    scene = VideoFileClip(filename)
    scene.preview()
    return


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
    buttons.empty()
    while True:
        wolf_btn = Button([load_image("avatar_frame.png")], 99, 180)
        wolf_btn.image.blit(load_image("wolf_avatar.png"), (-6, -6))
        lynx_btn = Button([load_image("avatar_frame.png")], 610, 180)
        lynx_btn.image.blit(load_image("lynx_avatar.png"), (-6, -6))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONUP:
                if wolf_btn.on_hovered(event.pos):
                    play_scene("../data/katstsena1.mp4")
                    game("wolf")
                if lynx_btn.on_hovered(event.pos):
                    play_scene("../data/katstsena1.mp4")
                    game("lynx")
        mouse_pos = pygame.mouse.get_pos()
        for btn in buttons:
            if btn.on_hovered(mouse_pos):
                btn.highlight()
            else:
                btn.set_default_image()
        screen.blit(choose_screen, (0, 0))
        buttons.draw(screen)
        buttons.update()
        pygame.display.flip()
        clock.tick(FPS)


# Функция запуска мини-игры
def frame_generate(hero):
    if hero == "lynx":
        hero_image = load_image("lynx_avatar.png")
        hero_name = "Рыська"
    else:
        hero_image = load_image("wolf_avatar.png")
        hero_name = "Волчи"
    player_frame = load_image("player_frame.png")
    player_frame.blit(hero_image, (0, 0))
    text = font.render(hero_name, True, WHITE)
    player_frame.blit(text, (200 - text.get_width() // 2, text.get_height() // 2))
    return player_frame


def game(hero, lvl=1):
    stay_parameters = [5, 2, 256, 256]  # Параметры для создания спрайт-листа бездействия игрока
    walk_parameters = [2, 1, 256, 256]  # Параметры для создания спрайт-листа ходьбы игрока
    # Установка игрока
    if hero == "lynx":
        player = Player(
            cut_sheet(load_image("lynx_stay.png"), *stay_parameters),
            cut_sheet(load_image("walking_lynx.png"), *walk_parameters), (0, 1))
    else:
        player = Player(
            cut_sheet(load_image("wolf_stay.png"), *stay_parameters),
            cut_sheet(load_image("walking_wolf.png"), *walk_parameters), (135, 100))
    paused = False
    buttons.empty()
    level = Level("tutorial")  # создаём объект уровня, передаём сложность
    level.render()
    camera = Camera()
    camera.update(player)  # привязываем игрока к камере (позиционировать камеру на игрока)
    while True:
        if paused:
            buttons.empty()
            volume_on_btn = Button(short_light_button, 375, 471, icon=icons["volume_up"])
            volume_off_btn = Button(short_light_button, 567, 471, icon=icons["volume_down"])
            exit_btn = Button(long_light_button, 362, 342, "Выход")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONUP:
                    if volume_off_btn.on_hovered(event.pos):
                        transition()
                    if volume_on_btn.on_hovered(event.pos):
                        transition()
                    if exit_btn.on_hovered(event.pos):
                        update_db()
                        transition()
                        start_screen()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    paused = False
            mouse_pos = pygame.mouse.get_pos()
            for btn in buttons:
                if btn.on_hovered(mouse_pos):
                    btn.highlight()
                else:
                    btn.set_default_image()
            screen.blit(blured_bg, (0, 0))
            screen.blit(settings_window, (293, 43))
            text = font.render("Пауза", True, WHITE)
            screen.blit(text, (457, 189))
            buttons.draw(screen)
            buttons.update()
            pygame.display.flip()
            clock.tick(FPS)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE] and not player.is_jump:
                    paused = True
                player_group.update(event)
            # Рисуем задний фон
            screen.fill(WHITE)
            screen.blit(bg, (0, 0))
            player_frame = frame_generate(hero)
            screen.blit(player_frame, (10, 10))
            # Рисуем все платформы из группы спрайтов
            objects_group.draw(screen)
            objects_group.update()
            player_group.draw(screen)  # Отрисовываем игрока
            player_group.update()  # Обновляем игрока каждый цикл
            # death_count = player.deaths
            # Проверка на то, чем занят игрок
            if player.occupation == 0:
                player.idle()
            if player.occupation == 1:
                player.walk_right()
            if player.occupation == 2:
                player.walk_left()
            if player.is_jump:
                player.jump()
            pygame.display.flip()
            clock.tick(FPS)
