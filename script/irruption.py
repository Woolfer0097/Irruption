from moviepy.editor import *
from game_functions import *
from game import *


def play_scene(filename):
    scene = VideoFileClip(filename)
    scene.preview()
    return


def main():
    pygame.init()
    start_screen()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    play_scene("../data/katstsena1.mp4")
    game("lynx", 1)


if __name__ == '__main__':
    main()
