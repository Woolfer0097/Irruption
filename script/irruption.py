from game_functions import *


def main():
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    start_screen()
    play_scene("../data/video/cut-scene#1.mp4")
    choose_hero()


if __name__ == '__main__':
    main()
