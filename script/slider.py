import pygame as pg


def display_text(text, color, x, y, font):
    text_image = font.render(text, False, color)
    text_rect = text_image.get_rect(center=(x, y))
    screen.blit(text_image, text_rect)


pg.init()
screen = pg.display.set_mode((640, 480))
screen_rect = screen.get_rect()
clock = pg.time.Clock()
font = pg.font.Font(None, 52)
done = False

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

    screen.fill((30, 30, 30))
    display_text(
        'Lorem ipsum dolor sit amet', (0, 100, 200),
        screen_rect.centerx, 100, font)

    pg.display.flip()
    clock.tick(30)
