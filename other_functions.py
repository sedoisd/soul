import sys
import os
import pygame


def load_image(name, path=None) -> pygame.Surface:
    fullname = os.path.join('image', name)
    if path is not None:
        fullname = os.path.join('image', path, name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def get_front_frame_characters_by_id(character_id: int) -> pygame.surface:  # for gui
    atlas = load_image(f'char_{character_id}.png', 'characters')
    atlas_width = atlas.get_width()
    atlas_height = atlas.get_height()
    image_width = atlas_width / 3
    image_height = atlas_height / 4
    return atlas.subsurface(image_width, 0, image_width, image_height)


def get_frame_weapon_by_id(weapon_id: int) -> pygame.surface:  # for gui
    image = load_image(f'weapon_{weapon_id}.png', 'weapons')
    return image


def get_frames_background() -> dict:
    keys = ['menu', 'shop', 'setting', 'selection']
    backgrounds_dict = dict()
    for i in range(len(keys)):
        backgrounds_dict[keys[i]] = load_image(f'background_{i}.png', 'background')
    return backgrounds_dict
