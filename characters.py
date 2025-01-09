from pygame import image, sprite
from other_functions import load_image
from constants import CHARACTER, CH_WIDTH, CH_HEIGHT



def get_frame_font_current_characters():
    # переписать функцию. взять widht height фото и делать формулы
    if CHARACTER == 0:
        return load_image('characters.png').subsurface((CH_WIDTH * 8, 0, CH_WIDTH, CH_HEIGHT))
    elif CHARACTER == 1:
        return load_image('characters.png').subsurface((0, 0, CH_WIDTH, CH_HEIGHT))
    elif CHARACTER == 2:
        return load_image('characters.png').subsurface((0, 0, CH_WIDTH, CH_HEIGHT))
    elif CHARACTER == 3:
        return load_image('characters.png').subsurface((0, 0, CH_WIDTH, CH_HEIGHT))
    elif CHARACTER == 4:
        return load_image('characters.png').subsurface((0, 0, CH_WIDTH, CH_HEIGHT))
    elif CHARACTER == 5:
        return load_image('characters.png').subsurface((0, 0, CH_WIDTH, CH_HEIGHT))
    return 'image'


class Knight(sprite.Sprite):
    # frame_front = load_image('characters.png').subsurface((0, 0, 237, 224))
    # frames_forward = [load_image('characters.jpeg').subsurface((0, i, 55.5, 55.5)) for i in range(0, 166, 55)]
    # frames_back = [load_image('characters.jpeg').subsurface((55.5, i, 55.5, 55.5)) for i in range(0, 166, 55)]
    # frames_left = [load_image('characters.jpeg').subsurface((111, i, 55.5, 55.5)) for i in range(0, 166, 55)]
    # frames_right = [load_image('characters.jpeg').subsurface((166.5, i, 55.5, 55.5)) for i in range(0, 166, 55)]

    def __init__(self):
        super().__init__()
        self.defualt_damage = 5
        self.speed = 10
        self.armor = 2

    def update(self):
        pass


class Magician(sprite.Sprite):
    def __init__(self):
        super().__init__()

    def update(self):
        pass

# class
