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
    # atlas_width = atlas.get_width()
    # atlas_height = atlas.get_height()
    # image_width = atlas_width / 3
    # image_height = atlas_height / 4
    return image


def get_frame_current_background(num) -> pygame.surface:
    image = load_image(f'background_{num}.png', 'background')
    # atlas_width = atlas.get_width()
    # atlas_height = atlas.get_height()
    # image_width = atlas_width / 3
    # image_height = atlas_height / 4
    return image

#
# def buy(price):
#     f = get_weapon_settings()
#     text = open('text.txt', 'w')
#     print(f'{f[0] - price}\n{f[1]}\n{f[2]}\n{f[3]}\n{f[4]}')
#     text.write(f'{f[0] - price}\n{f[1]}\n{f[2]}\n{f[3]}\n{f[4]}')
#     text.close()
#
#
# def get_weapon_settings():
#     text = open('text.txt', 'r')
#     f = [i for i in text]
#     text.close()
#     return f
#
#
# def update_setting(progress_bar1, progress_bar2) -> None:
#     f = get_weapon_settings()
#     text = open('text.txt', 'w')
#     print(f'{f[0]}\n{progress_bar1}\n{progress_bar2}\n{f[3]}\n{f[4]}')
#     text.write(f'{f[0]}\n{progress_bar1}\n{progress_bar2}\n{f[3]}\n{f[4]}')
#     text.close()
#
#
# def update_weapon(progress_bar1, progress_bar2) -> None:
#     f = get_weapon_settings()
#     text = open('text.txt', 'w')
#     print(f'{f[0]}\n{progress_bar1}\n{progress_bar2}\n{f[3]}\n{f[4]}')
#     text.write(f'{f[0]}\n{progress_bar1}\n{progress_bar2}\n{f[3]}\n{f[4]}')
#     text.close()
