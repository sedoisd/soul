import sys
import os
import pygame
from constants import SIZE


def load_image(name, path=None):
    fullname = fullname = os.path.join('image', name)
    if path is not None:
        fullname = os.path.join('image', path, name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    # if colorkey is not None:
    #     image = image.convert()
    #     if colorkey == -1:
    #         colorkey = image.get_at((0, 0))
    #     image.set_colorkey(colorkey)
    # else:
    #     image = image.convert_alpha()
    return image
