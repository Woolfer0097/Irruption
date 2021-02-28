from game_functions import *


# Функция отвечающая за последовательность включения экранов
def main():
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    start_screen()
    identifier = int(*[str(*i) for i in cursor.execute("SELECT MAX(id) FROM saves")]) + 1  # Идентификатор игрока
    name_window(identifier)
    transition()
    play_scene("../data/video/cut-scene#1.mp4")
    pygame.mixer.music.load("../data/sounds/bg.mp3")
    pygame.mixer.music.play(-1)
    hero = choose_hero()
    for level in range(len(LEVELS)):
        update_db(identifier, hero, level)
        game(hero, level)
        if level != 3:
            mini_game()
        else:
            play_scene("../data/video/cut-scene#2.mp4")
            return
    return


if __name__ == '__main__':
    main()
