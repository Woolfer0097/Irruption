from game_functions import *
from constants import *


def game():
    cat_stay = AnimatedSprite(load_image(os.path.join("images", "cat_stay.png")), 5, 2, 0, 0).frames
    wolf_stay = AnimatedSprite(load_image(os.path.join("images", "wolf_stay.png")), 5, 2, 0, 0).frames
    cat_walking = AnimatedSprite(load_image(os.path.join("images", "walking_cat.png")), 2, 1, 0, 0).frames
    wolf_walking = AnimatedSprite(load_image(os.path.join("images", "walking_wolf.png")), 2, 1, 0, 0).frames
    animation = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_0]:
                animation = cat_stay
            if keys[pygame.K_1]:
                animation = cat_walking
            if keys[pygame.K_2]:
                animation = wolf_stay
            if keys[pygame.K_3]:
                animation = wolf_walking
        screen.fill(pygame.Color("black"))
        if animation:
            screen.blit(animation.image, (50, 100))
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)


if __name__ == '__main__':
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    clock = pygame.time.Clock()
    size = width, height = 1024, 768
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    screen.fill(pygame.Color("black"))
    choose_hero()
    game()
