from game_functions import *


# Функция отвечающая за последовательность включения экранов
def main():
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    start_screen()
    name = show_name_input()
    hero = show_choose_hero_screen()
    create_account(hero, name)
    transition()
    play_scene("./data/video/cut-scene#1.mp4")
    pygame.mixer.music.load("./data/sounds/bg.mp3")
    pygame.mixer.music.play(-1)
    for level in range(len(LEVELS)):
        update_saves(name, hero, level)
        game(hero, level)
        if level != 3:
            mini_game()
        else:
            play_scene("./data/video/cut-scene#2.mp4")
            return
    return


if __name__ == '__main__':
    main()
