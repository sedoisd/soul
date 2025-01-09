from pygame import image, sprite
from other_functions import load_image
from constants import ID_CHARACTER



def get_front_frame_current_characters():
    atlas = load_image(f'char_{ID_CHARACTER}.png', 'characters')
    atlas_width = atlas.get_width()
    atlas_height = atlas.get_height()
    image_width = atlas_width / 3
    image_height = atlas_height / 4
    return atlas.subsurface(image_width, 0, image_width, image_height)


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
