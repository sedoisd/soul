import sys
import os
import pygame
from constants import ID_CHARACTER, ID_WEAPON


def load_image(name, path=None) -> pygame.Surface:
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


def get_front_frame_current_characters() -> pygame.surface:
    atlas = load_image(f'char_{ID_CHARACTER}.png', 'characters')
    atlas_width = atlas.get_width()
    atlas_height = atlas.get_height()
    image_width = atlas_width / 3
    image_height = atlas_height / 4
    return atlas.subsurface(image_width, 0, image_width, image_height)


def get_frame_current_weapon() -> pygame.surface:
    image = load_image(f'weapon_{ID_WEAPON}.png', 'weapons')
    # atlas_width = atlas.get_width()
    # atlas_height = atlas.get_height()
    # image_width = atlas_width / 3
    # image_height = atlas_height / 4
    return image


