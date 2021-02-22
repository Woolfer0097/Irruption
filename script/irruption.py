from game_functions import *


def main():
    pygame.init()
    start_screen()
    choose_hero()
    os.environ['SDL_VIDEO_CENTERED'] = '1'


if __name__ == '__main__':
    main()
