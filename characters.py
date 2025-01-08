from pygame import image, sprite
from other_functions import load_image


def get_image_for_start_menu(number_characters):
    pass


class Knight(sprite.Sprite):
    frames_forward = [load_image('characters.jpeg').subsurface((0, i, 55.5, 55.5)) for i in range(0, 166, 55)]
    frames_back = [load_image('characters.jpeg').subsurface((55.5, i, 55.5, 55.5)) for i in range(0, 166, 55)]
    frames_left = [load_image('characters.jpeg').subsurface((111, i, 55.5, 55.5)) for i in range(0, 166, 55)]
    frames_right = [load_image('characters.jpeg').subsurface((166.5, i, 55.5, 55.5)) for i in range(0, 166, 55)]

    def __init(self):
        self.defualt_damage = 5
        self.speed = 10
        self.armor = 2
