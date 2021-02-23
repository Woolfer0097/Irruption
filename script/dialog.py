from constants import *


class DialogFrame(pygame.sprite.Sprite):
    def __init__(self, avatar_frame, dialog_frame, text_dictionary):
        super(DialogFrame, self).__init__(buttons)
        self.image = pygame.Surface((885, 100))
        self.avatar_frame = avatar_frame
        self.dialog_frame = dialog_frame
        self.dialog_number = 0
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.rect = self.image.get_rect()
        self.text_dictionary = text_dictionary

    def dialog_generate(self, i):
        for hero_speaker, text in self.text_dictionary[i].items():
            avatar_frame, dialog_frame = self.dialog_frame_generate(hero_speaker, text)
            screen.blit(avatar_frame, (74, 533))
            screen.blit(dialog_frame, (250, 533))
            pygame.time.delay(5000)

    def dialog_frame_generate(self, hero_speaker, text):
        if hero_speaker == "lynx":
            hero_avatar = load_image("lynx_avatar.png")
            hero_name = "Рыська"
        elif hero_speaker == "bars":
            hero_avatar = load_image("wolf_avatar.png")
            hero_name = "Ирбис"
        else:
            hero_avatar = load_image("wolf_avatar.png")
            hero_name = "Волчи"
        self.avatar_frame.blit(hero_avatar, (-6, -6))
        font_text = pygame.font.Font("../data/fonts/thintel.ttf", 48)
        text_result = font_text.render(f"{hero_name}: {text}", True, WHITE)
        self.dialog_frame.blit(text_result, text_result.get_rect(center=self.dialog_frame.get_rect().center))
        return [self.avatar_frame, self.dialog_frame]
