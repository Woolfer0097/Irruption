from moviepy.editor import *
from game_functions import *
from constants import *


def play_scene(filename):
    scene = VideoFileClip(filename)
    scene.preview()
    return


def main():
    pygame.init()
    pygame.display.set_caption("Irruption")
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    play_scene("../data/katstsena1.mp4")
    start_screen()
    choose_hero()
    print("Игра")


main()
