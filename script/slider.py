from game_functions import *

screen = pygame.display.set_mode((1024, 768))
img = load_image("images/main_menu.png")

for opacity in range(255, 0, -15):
     pygame.draw.rect(screen, (0, 0, 0, opacity),  (0, 0, 1024, 768))
     pygame.display.flip()
     pygame.time.delay(100)
