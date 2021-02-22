from game_functions import *


def main():
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    start_screen()
    choose_hero()
    game(hero)


if __name__ == '__main__':
    main()
