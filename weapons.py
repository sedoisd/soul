from pygame import image, sprite
from other_functions import load_image
from constants import ID_CHARACTER



class Sword(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.damage = 15

    def update(self, *args, **kwargs):
        pass