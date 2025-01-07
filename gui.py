from pygame import Rect
import pygame
import pygame_gui
from pygame_gui.elements import *
from constants import SIZE
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start():
    print('start')


class GuiManager:
    def __init__(self):
        self.manager = pygame_gui.UIManager(SIZE)

    def load_start_menu(self):
        def redirection(command_load=None):
            self.button_start.kill()
            self.button_shop.kill()
            self.button_setting.kill()
            self.button_exit.kill()
            self.image_character = None
            self.label_image_character.kill()
            self.label_name_character.kill()
            self.image_weapon = None
            self.label_image_weapon.kill()
            self.label_name_weapon.kill()
            command_load()

        size_button = (200, 70)
        self.button_start = UIButton(relative_rect=Rect((30, 180, *size_button)),
                                     text='Старт', manager=self.manager, command=start)
        self.button_shop = UIButton(relative_rect=Rect((30, 270, *size_button)),
                                    text='Магазин', manager=self.manager,
                                    command=lambda: redirection(self.load_shop))
        self.button_setting = UIButton(relative_rect=Rect((30, 360, *size_button)),
                                       text='Настройки', manager=self.manager,
                                       command=lambda: redirection(self.load_setting))
        self.button_exit = UIButton(relative_rect=Rect((30, 450, *size_button)),
                                    text='Выход', manager=self.manager)

        # Character menu
        self.label_image_character = UILabel(Rect((650, 0, 150, 150)), text='')
        self.image_character = pygame.image.load('image/test_pers.png').subsurface((53, 0, 52, 72))
        self.image_character = pygame.transform.rotozoom(self.image_character, 0, 4)
        self.label_image_character.set_image(self.image_character)
        self.label_name_character = UILabel(Rect((690, 310, 100, 30)), text='Рыцарь')

        # Weapon menu
        self.label_image_weapon = UILabel(Rect((350, 60, 150, 100)), text='')
        self.image_weapon = pygame.image.load('image/weapon.png')
        self.label_image_weapon.set_image(self.image_weapon)
        self.label_name_weapon = UILabel(Rect((410, 315, 60, 30)), text='Меч')

    def load_setting(self):
        def back():
            self.button_back.kill()
            self.load_start_menu()

        self.button_back = UIButton(relative_rect=pygame.Rect(2, 2, 40, 40), text='back',
                                    manager=self.manager, command=back)
        # image_button_back = pygame.image.load('image/back.png')
        # self.button_back._set_image(image_button_back)

    def load_shop(self):
        def back():
            self.button_back.kill()
            self.load_start_menu()

        self.button_back = UIButton(relative_rect=pygame.Rect(2, 2, 40, 40), text='back',
                                    manager=self.manager, command=back)
