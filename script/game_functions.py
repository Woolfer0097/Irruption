from game import *
from button import *
from constants import *


# Функция запуска начального экрана
def start_screen():
    current_frame = 0
    volume = 0.2
    settings_flag = False
    control_flag = False
    info_flag = False
    pygame.mixer.music.load("../data/sounds/bg.mp3")
    pygame.mixer.music.play(-1)
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
                        return
                    if info_btn.on_hovered(event.pos):
                        info_flag = True
                    if exit_btn.on_hovered(event.pos):
                        transition()
                        terminate()
                    if settings_btn.on_hovered(event.pos):
                        settings_flag = True
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
                    game("wolf")
                if lynx_btn.on_hovered(event.pos):
                    game("lynx")
        check_hovered()
        screen.blit(choose_screen, (0, 0))
        buttons.draw(screen)
        buttons.update()
        pygame.display.flip()
        clock.tick(FPS)


# Функция запуска мини-игры
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
    text = font.render(hero_name, True, WHITE)
    player_frame.blit(text, (200 - text.get_width() // 2, text.get_height() // 2))
    return player_frame


def check_hovered():
    mouse_pos = pygame.mouse.get_pos()
    for btn in buttons:
        if btn.on_hovered(mouse_pos):
            btn.highlight()
        else:
            btn.set_default_image()


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
    font_text = pygame.font.Font("../data/fonts/thintel.ttf", 48)
    text_result = font_text.render(f"{hero_name}: {text}", True, WHITE)
    dialog_frame.blit(text_result, text_result.get_rect(center=dialog_frame.get_rect().center))
    return [avatar_frame, dialog_frame]


def game(hero, lvl=0):
    FPS = 60
    dialog_count = 0
    stay_parameters = [5, 2, 256, 256]  # Параметры для создания спрайт-листа бездействия игрока
    walk_parameters = [2, 1, 256, 256]  # Параметры для создания спрайт-листа ходьбы игрока
    level = Level("hard")  # создаём объект уровня, передаём сложность
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
                 None, (350, 90), npc=True)
    paused = False
    dialog = False
    control_flag = False
    volume = 0.4
    buttons.empty()
    pygame.mixer.music.load("../data/sounds/bg.mp3")
    pygame.mixer.music.play(-1)
    while True:
        if paused:
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
                        update_db()
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
            screen.blit(blured_bg, (0, 0))
            if control_flag:
                screen.blit(control_window, (0, 0))
            else:
                screen.blit(settings_window, (293, 43))
                text = font.render("Пауза", True, WHITE)
                screen.blit(text, (457, 189))
                buttons.draw(screen)
                buttons.update()
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
            if objects_group.sprites()[-1].rect.colliderect(player.rect):
                dialog = True
            screen.fill(WHITE)  # Очищаем экран
            screen.blit(bg, (0, 0))  # Рисуем задний фон
            objects_group.draw(screen)  # Рисуем все платформы из группы спрайтов
            objects_group.update()  # Обновляем
            screen.blit(player.image, (player.rect.x, player.rect.y))  # Отрисовываем игрока и NPC
            player.update()  # Обновляем
            # death_count = player.deaths
            # Проверка на то, чем занят игрок
            if dialog:
                player.is_jump = False
                dialog_text = texts[lvl]
                if dialog_count >= len(dialog_text):
                    game(hero)
                for hero_speaker, text in dialog_text[dialog_count].items():
                    if hero_speaker == "hero":
                        avatar_frame, dialog_frame = dialog_frame_generate(hero, text)
                    else:
                        avatar_frame, dialog_frame = dialog_frame_generate(hero_speaker, text)
                    screen.blit(avatar_frame, (74, 533))
                    screen.blit(dialog_frame, (250, 533))
                player_group.draw(screen)
                npc.idle()
            else:
                player_frame = frame_generate(hero)  # Генерируем рамку с данными игрока
                screen.blit(player_frame, (10, 10))  # Отрисовываем рамку
                if player.occupation == 0:
                    player.idle()
                if player.occupation == 1:
                    if level.level_length >= abs(camera.dx) >= level.level_start:
                        player.camera_stop = False
                        player.walk_right()
                        move(player, STEP)
                    else:
                        player.camera_stop = True
                        player.walk_right()
                if player.occupation == 2:
                    if camera.dx < level.level_start:
                        player.camera_stop = False
                        player.walk_left()
                        move(player, -STEP)
                    else:
                        player.camera_stop = True
                        player.walk_left()
                if player.is_jump:
                    player.jump()
            pygame.display.flip()
            clock.tick(FPS)


camera = Camera()


def move(player, x):
    camera.dx -= (x - player.x)
    player.x -= (x + player.x)
    for sprite in objects_group:
        camera.apply(sprite)
