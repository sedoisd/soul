from pygame import Rect
import pygame
import pygame_gui
from pygame_gui.elements import *
from constants import SIZE, FILENAME_DATABASE, ID_CHARACTER
from other_functions import get_frame_current_weapon, get_front_frame_current_characters
import sqlite3


class GuiManager:
    def __init__(self):
        self.manager = pygame_gui.UIManager(SIZE)

    def start_game(self):
        pass

    def kill_start_menu(self) -> None:
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

    def load_start_menu(self) -> None:
        def redirection(command_load=None) -> None:
            self.kill_start_menu()
            command_load()

        size_button = (200, 70)
        self.button_start = UIButton(relative_rect=Rect((30, 180, *size_button)),
                                     text='Старт', manager=self.manager, )
        self.button_shop = UIButton(relative_rect=Rect((30, 270, *size_button)),
                                    text='Магазин', manager=self.manager,
                                    command=lambda: redirection(self._load_shop))
        self.button_setting = UIButton(relative_rect=Rect((30, 360, *size_button)),
                                       text='Настройки', manager=self.manager,
                                       command=lambda: redirection(self._load_setting))
        self.button_exit = UIButton(relative_rect=Rect((30, 450, *size_button)),
                                    text='Выход', manager=self.manager)

        # Character menu
        self.label_image_character = UILabel(Rect((620, 50, 150, 400)), text='')
        self.image_character = get_front_frame_current_characters()
        # self.image_character = ц(self.image_character, 0, 0.2)
        self.label_image_character.set_image(self.image_character)
        self.label_name_character = UILabel(Rect((690, 310, 100, 30)), text='Рыцарь')

        # Weapon menu
        self.label_image_weapon = UILabel(Rect((350, 60, 150, 100)), text='')
        self.image_weapon = get_frame_current_weapon()
        self.label_image_weapon.set_image(self.image_weapon)
        self.label_name_weapon = UILabel(Rect((410, 315, 60, 30)), text='Меч')

    def _load_setting(self) -> None:
        def back():
            self.button_back.kill()
            self.load_start_menu()

        self.button_back = UIButton(relative_rect=pygame.Rect(2, 2, 40, 40), text='back',
                                    manager=self.manager, command=back)
        # image_button_back = pygame.image.load('image/back.png')
        # self.button_back._set_image(image_button_back)

    def _load_shop(self) -> None:
        def back():
            self.button_back.kill()
            self.load_start_menu()

        self.button_back = UIButton(relative_rect=pygame.Rect(2, 2, 40, 40), text='back',
                                    manager=self.manager, command=back)


class DatabaseManager:
    @classmethod
    def _connection_to_database(cls):
        with sqlite3.connect(FILENAME_DATABASE) as con:
            cur = con.cursor()
            # print(type(con), type(cur))
            return con, cur

    @classmethod
    def get_characteristics_character(cls) -> tuple[str, int, int, int]:
        con, cur = cls._connection_to_database()
        result = cur.execute('SELECT name, health, damage, speed FROM characters '
                             'WHERE id=?', (ID_CHARACTER,)).fetchone()
        # print(result)
        con.close()
        return result

    @classmethod
    def get_characteristics_enemy_by_id(cls, enemy_id: int = None) -> tuple[str, int, int, int]:
        con, cur = cls._connection_to_database()
        result = cur.execute('SELECT name, health, damage, speed FROM enemies'
                             'WHERE id=?', (enemy_id,)).fetchone()
        # print(result)
        con.close()
        return result

    @classmethod
    def get_quantities_frames_enemy_by_id(cls, enemy_id: int = None) -> tuple[int, int, int, int]:
        con, cur = cls._connection_to_database()
        result = cur.execute('SELECT quan_walking_frames, quan_attack_frames, '
                             'quan_death_frames, quan_kinds_frames FROM enemies'
                             'WHERE id=?', (enemy_id,)).fetchone()
        # print(result)
        con.close()
        return result
