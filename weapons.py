from pygame import image, sprite
from other_functions import load_image
from constants import ID_WEAPON

def get_frame_current_weapon():
    image = load_image(f'weapon_{ID_WEAPON}.png', 'weapons')
    # atlas_width = atlas.get_width()
    # atlas_height = atlas.get_height()
    # image_width = atlas_width / 3
    # image_height = atlas_height / 4
    return image

class Sword(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.damage = 15

    def update(self, *args, **kwargs):
        pass