from game_classes import *
from constants import *


# Функция запуска начального экрана
def start_screen():
    current_frame = 0
    volume = 0.2
    settings_flag = False
    control_flag = False
    info_flag = False
    saves = False
    info_label = InfoLabel(save_screen_label, 106)
    pygame.mixer.music.load("../data/sounds/bg.mp3")
    pygame.mixer.music.play(-1)
    while True:
        if settings_flag:
            # Настройки
            buttons.empty()
            volume_on_btn = Button(short_light_button, 375, 471, "", icons["volume_up"])
            volume_off_btn = Button(short_light_button, 567, 471, "", icons["volume_down"])
            control = Button(long_light_button, 362, 342, "Управление")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                # Обработка нажатий на кнопки
                if event.type == pygame.MOUSEBUTTONUP:
                    pygame.mixer.music.set_volume(volume)
                    if volume_off_btn.on_hovered(event.pos):
                        volume -= 0.05
                    if volume_on_btn.on_hovered(event.pos):
                        volume += 0.05
                    if control.on_hovered(event.pos):
                        control_flag = True
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    if control_flag:
                        control_flag = False
                    else:
                        settings_flag = False
                        control_flag = False
            check_hovered()
            # Отрисовка нужных изображений
            screen.blit(blurred_bg, (0, 0))
            if control_flag:
                screen.blit(control_window, (0, 0))
            else:
                screen.blit(settings_window, (293, 43))
                font = pygame.font.Font("../data/fonts/thintel.ttf", 72)
                text = font.render("Настройки", True, WHITE)
                screen.blit(text, (416, 189))
                buttons.draw(screen)
                buttons.update()
            # Отрисовка
            pygame.display.flip()
            clock.tick(FPS)
        elif saves:
            buttons.empty()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        for sprite in info_labels:
                            if sprite.dy < 0:
                                sprite.scroll_down()
                    elif event.button == 5:
                        for sprite in info_labels:
                            if sprite.dy > info_label.length:
                                sprite.scroll_up()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    saves = False
            screen.blit(blurred_bg, (0, 0))
            info_label.render()
            screen.blit(saves_screen, (106, -31))
            # Отрисовка
            pygame.display.flip()
            clock.tick(FPS)
        else:
            # Начальный экран
            buttons.empty()
            start_btn = Button(long_button_frames, 384, 310, "Играть")
            info_btn = Button(long_button_frames, 384, 406, "Об авторах")
            exit_btn = Button(long_button_frames, 384, 502, "Выход")
            settings_btn = Button(short_button_frames, 910, 584, "", icons["settings"])
            saves_btn = Button(short_button_frames, 917, 26, "", icons["cup"])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONUP:
                    if start_btn.on_hovered(event.pos):
                        return
                    if info_btn.on_hovered(event.pos):
                        info_flag = True
                    if exit_btn.on_hovered(event.pos):
                        transition()
                        terminate()
                    if settings_btn.on_hovered(event.pos):
                        settings_flag = True
                    if saves_btn.on_hovered(event.pos):
                        saves = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        info_flag = False
            check_hovered()
            screen.blit(bg_frames[current_frame // ANIMATION_FPS], (0, 0))
            current_frame = calculate_frame(current_frame, bg_frames)
            buttons.draw(screen)
            buttons.update()
            if info_flag:
                screen.blit(info_screen, (0, 0))
            # Отрисовка
            pygame.display.flip()
            clock.tick(FPS)


# Функция ввода имени игрока
def name_window(identifier):
    text = ""
    error_label_flag = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    error = create_account(identifier, text)
                    if error == "unique_error":
                        error_label_flag = True
                    else:
                        if text != "":
                            return text
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if len(text) < MAX_TEXT_LENGTH:
                        if event.unicode in ACCEPTED_SYMBOLS:
                            text += event.unicode
        textbox = TextBox(input_box, 184, 123)
        screen.blit(blurred_bg, (0, 0))
        screen.blit(input_box, (184, 83))
        set_text(textbox, text, 120)
        if error_label_flag:
            error_label("unique_error")
        # Отрисовка
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
                    return "wolf"
                if lynx_btn.on_hovered(event.pos):
                    return "lynx"
        check_hovered()
        screen.blit(choose_screen, (0, 0))
        buttons.draw(screen)
        buttons.update()
        # Отрисовка
        pygame.display.flip()
        clock.tick(FPS)


# Функция запуска игры
def game(hero, lvl):
    camera = Camera()
    player_group.empty()
    objects_group.empty()
    borders.empty()
    dialog_count = 0
    stay_parameters = [5, 2, 256, 256]  # Параметры для создания спрайт-листа бездействия игрока
    walk_parameters = [2, 1, 256, 256]  # Параметры для создания спрайт-листа ходьбы игрока
    level = Level(LEVELS[lvl])  # создаём объект уровня, передаём сложность
    level.render()
    # Установка игрока
    if hero == "lynx":
        player = Player(
            cut_sheet(load_image("lynx_stay.png"), *stay_parameters),
            cut_sheet(load_image("walking_lynx.png"), *walk_parameters), (0, 0))
    else:
        player = Player(
            cut_sheet(load_image("wolf_stay.png"), *stay_parameters),
            cut_sheet(load_image("walking_wolf.png"), *walk_parameters), (0, 0))
    npc = Player(cut_sheet(load_image("bars_stay.png"), 3, 2, 256, 256),
                 None, (300, 90), npc=True)
    paused = False
    dialog = False
    control_flag = False
    volume = 0.4
    buttons.empty()
    while True:
        if paused:
            # Пауза
            pygame.mixer.music.pause()
            buttons.empty()
            volume_on_btn = Button(short_light_button, 375, 471, icon=icons["volume_up"])
            volume_off_btn = Button(short_light_button, 567, 471, icon=icons["volume_down"])
            control = Button(long_light_button, 362, 314, "Управление")
            exit_btn = Button(long_light_button, 362, 380, "Выход")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONUP:
                    pygame.mixer.music.set_volume(volume)
                    if volume_off_btn.on_hovered(event.pos):
                        volume -= 0.05
                    if volume_on_btn.on_hovered(event.pos):
                        volume -= 0.05
                    if exit_btn.on_hovered(event.pos):
                        # update_db()
                        transition()
                        start_screen()
                    if control.on_hovered(event.pos):
                        control_flag = True
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    if control_flag:
                        control_flag = False
                    else:
                        paused = False
                        control_flag = False
            check_hovered()
            screen.blit(blurred_bg, (0, 0))
            if control_flag:
                screen.blit(control_window, (0, 0))
            else:
                screen.blit(settings_window, (293, 43))
                font = pygame.font.Font("../data/fonts/thintel.ttf", 72)
                text = font.render("Пауза", True, WHITE)
                screen.blit(text, (457, 189))
                buttons.draw(screen)
                buttons.update()
            # Отрисовка
            pygame.display.flip()
            clock.tick(FPS)
        else:
            pygame.mixer.music.unpause()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE] and not player.is_jump:
                    paused = True
                if keys[pygame.K_RETURN]:
                    dialog_count += 1
                player_group.update(event)
            if player.rect.y > SCREEN_HEIGHT + 200:
                player.rect.y = 0
                player.walk_left()
                move(camera, player, -STEP)
            if objects_group.sprites()[-1].rect.colliderect(player.rect):
                dialog = True
            screen.fill(WHITE)  # Очищаем экран
            screen.blit(bg, (0, 0))  # Рисуем задний фон
            objects_group.draw(screen)  # Рисуем все платформы из группы спрайтов
            objects_group.update()  # Обновляем
            screen.blit(player.image, (player.rect.x, player.rect.y))  # Отрисовываем игрока и NPC
            player.update()  # Обновляем
            if dialog:
                # Диалог
                player.is_jump = False
                dialog_text = dialog_texts[lvl]
                if dialog_count >= len(dialog_text):
                    return
                for hero_speaker, text in dialog_text[dialog_count].items():
                    if hero_speaker == "hero":
                        avatar_frame, dialog_frame = dialog_frame_generate(hero, text)
                    else:
                        avatar_frame, dialog_frame = dialog_frame_generate(hero_speaker, text)
                    dialog_frame_draw(avatar_frame, dialog_frame)
                player_group.draw(screen)
                npc.idle()
            else:
                # Игра
                player_frame = frame_generate(hero)  # Генерируем рамку с данными игрока
                screen.blit(player_frame, (10, 10))  # Отрисовываем рамку
                if player.occupation == 0:
                    player.idle()
                if player.occupation == 1:
                    if level.level_length >= abs(camera.dx) >= level.level_start:
                        player.camera_stop = False
                        player.walk_right()
                        move(camera, player, STEP)
                    else:
                        player.camera_stop = True
                        player.walk_right()
                if player.occupation == 2:
                    if camera.dx < level.level_start:
                        player.camera_stop = False
                        player.walk_left()
                        move(camera, player, -STEP)
                    else:
                        player.camera_stop = True
                        player.walk_left()
                if player.is_jump:
                    player.jump()
            font_text = pygame.font.Font("../data/fonts/thintel.ttf", 72)
            text_result = font_text.render(str(lvl), True, WHITE)
            screen.blit(text_result, (989, 5))
            # Отрисовка
            pygame.display.flip()
            clock.tick(FPS)


# Функция запуска мини-игры "Крестики-Нолики"
def mini_game():
    board = Board(3, 3, 293, 33)
    dialog = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not dialog:
                    check = board.player_step(event.pos)
                    if check:
                        if board.step != 9:
                            board.ai_step()
                        result = board.check_win()
                        dialog = mini_game_result_analysis(result)
                    else:
                        pass
            if dialog:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    return
        screen.blit(blurred_bg, (0, 0))
        screen.blit(board.screen, (board.left, board.top))
        board.render()
        if dialog:
            if dialog == "win":
                avatar_frame, dialog_frame = dialog_frame_generate("bars", "Спасибо за игру! Увидимся!")
                dialog_frame_draw(avatar_frame, dialog_frame)
            elif dialog == "lose":
                avatar_frame, dialog_frame = dialog_frame_generate("bars", "Ха-ха, победишь в следующий раз!")
                dialog_frame_draw(avatar_frame, dialog_frame)
            else:
                avatar_frame, dialog_frame = dialog_frame_generate("bars", "Ничья..., ну ничего, ещё увидимся!")
                dialog_frame_draw(avatar_frame, dialog_frame)
        pygame.display.flip()
        clock.tick(FPS)


# Анализ результата проверки на победу в мини-игре
def mini_game_result_analysis(result):
    if result:
        if result == "X":
            return "win"
        elif result == "O":
            return "lose"
        elif result == "draw":
            return "draw"


# Отрисовка ошибок на экран
def error_label(error):
    font_text = pygame.font.Font("../data/fonts/thintel.ttf", 92)
    text_result = font_text.render(error, True, WHITE)
    screen.blit(text_result, (0, 0))


# Генерация рамки с игроком
def frame_generate(hero_):
    if hero_ == "lynx":
        hero_image = load_image("lynx_avatar.png")
        hero_name = "Рыська"
    elif hero_ == "bars":
        hero_image = load_image("bars_avatar.png")
        hero_name = "Ирбис"
    else:
        hero_image = load_image("wolf_avatar.png")
        hero_name = "Волчи"
    player_frame = load_image("player_frame.png")
    player_frame.blit(hero_image, (0, 0))
    font = pygame.font.Font("../data/fonts/thintel.ttf", 72)
    text = font.render(hero_name, True, WHITE)
    player_frame.blit(text, (200 - text.get_width() // 2, text.get_height() // 2))
    return player_frame


# Проверка наведён ли курсор на кнопку
def check_hovered():
    mouse_pos = pygame.mouse.get_pos()
    for btn in buttons:
        if btn.on_hovered(mouse_pos):
            btn.highlight()
        else:
            btn.set_default_image()


# Генерация диалоговой рамки с игроком
def dialog_frame_generate(hero_speaker, text):
    if hero_speaker == "lynx":
        hero_avatar = load_image("lynx_avatar.png")
        hero_name = "Рыська"
    elif hero_speaker == "bars":
        hero_avatar = load_image("bars_avatar.png")
        hero_name = "Ирбис"
    else:
        hero_avatar = load_image("wolf_avatar.png")
        hero_name = "Волчи"
    avatar_frame = load_image("avatar_frame.png")
    dialog_frame = load_image("dialog_frame.png")
    avatar_frame.blit(hero_avatar, (-6, -6))
    font_text = pygame.font.Font("../data/fonts/thintel.ttf", 36)
    text_result = font_text.render(f"{hero_name}: {text}", True, WHITE)
    dialog_frame.blit(text_result, text_result.get_rect(center=dialog_frame.get_rect().center))
    return [avatar_frame, dialog_frame]


# Отрисовка рамки игрока
def dialog_frame_draw(avatar_frame, dialog_frame):
    screen.blit(avatar_frame, (74, 533))
    screen.blit(dialog_frame, (250, 533))


# Движение камеры
def move(camera, player, x):
    camera.dx -= (x - player.x)
    player.x -= (x + player.x)
    for sprite in objects_group:
        camera.apply(sprite)
