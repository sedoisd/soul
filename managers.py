from pygame import Rect
import pygame
import pygame_gui
from pygame_gui.elements import *
from constants import SIZE, FILENAME_DATABASE, ID_CHARACTER
# from initialization_classes import
from other_functions import get_front_frame_current_characters, get_frame_current_weapon
import sqlite3


class GuiManager:
    def __init__(self):
        self.manager = pygame_gui.UIManager(SIZE)
        self.database_manager = DatabaseManager()

    def start_game(self):
        pass

    def kill_start_menu(self) -> None:
        self.button_start.kill()
        self.button_shop.kill()
        self.button_setting.kill()
        self.button_exit.kill()
        self.image_character = None
        # self.label_image_character.kill()
        # self.label_name_character.kill()
        self.image_weapon = None
        # self.label_image_weapon.kill()
        # self.label_name_weapon.kill()

    def load_start_menu(self) -> None:
        def redirection(command_load=None) -> None:
            self.kill_start_menu()
            command_load()
        # size_button = (200, 70)
        self.button_start = UIButton(relative_rect=Rect((363, 430, 200, 70)),
                                     text='Играть', manager=self.manager, )
        self.button_shop = UIButton(relative_rect=Rect((170, 370, 100, 50)),
                                    text='Магазин', manager=self.manager,
                                    )
        self.button_setting = UIButton(relative_rect=Rect((0, 650, 80, 50)),
                                       text='Настройки', manager=self.manager,
                                    )
        self.button_exit = UIButton(relative_rect=Rect((775, 290, 100, 50)),
                                    text='Выход', manager=self.manager)
        
    def load_start_game1(self) -> None:
        self.button_back = UIButton(relative_rect=pygame.Rect(2, 2, 50, 30), text='назад',
                                    manager=self.manager)
        # Character menu
        self.label_image_character = UILabel(Rect((620, 290, 150, 400)), text='')
        self.image_character = get_front_frame_current_characters()
        # self.image_character = ц(self.image_character, 0, 0.2)
        self.label_image_character.set_image(self.image_character)
        self.label_name_character = UILabel(Rect((690, 520, 100, 30)), text='Рыцарь')

        # Weapon menu
        self.label_image_weapon = UILabel(Rect((300, 330, 150, 100)), text='')
        self.image_weapon = get_frame_current_weapon()
        self.label_image_weapon.set_image(self.image_weapon)
        self.label_name_weapon = UILabel(Rect((350, 520, 60, 30)), text='Меч')



    def _load_setting(self) -> None:
        progress_bar1, progress_bar2 = self.database_manager.get_characteristics_settings()
        self.button_back = UIButton(relative_rect=pygame.Rect(2, 2, 50, 30), text='назад',
                                    manager=self.manager)
        # image_button_back = pygame.image.load('image/back.png')
        # self.button_back._set_image(image_button_back)
        self.button_sound = UIButton(relative_rect=pygame.Rect(50, 50, 100, 40), text='музыка',
                                    manager=self.manager)
        self.button_fihki = UIButton(relative_rect=pygame.Rect(50, 100, 100, 40), text='эффекты',
                            manager=self.manager)
        self.progress_bar1_f = UIProgressBar(relative_rect=pygame.Rect((250, 55), (100, 30)),
                             manager=self.manager)
        self.progress_bar1_f.set_current_progress(progress_bar1)
        self.progress_bar2_f = UIProgressBar(relative_rect=pygame.Rect((250, 105), (100, 30)),
                             manager=self.manager)
        self.progress_bar2_f.set_current_progress(progress_bar2)
        self.button_minys1 = UIButton(relative_rect=pygame.Rect(210, 55, 30, 30), text='-',
                                    manager=self.manager)
        self.button_plus1 = UIButton(relative_rect=pygame.Rect(360, 55, 30, 30), text='+',
                                    manager=self.manager)
        self.button_minys2 = UIButton(relative_rect=pygame.Rect(210, 105, 30, 30), text='-',
                                    manager=self.manager)
        self.button_plus2 = UIButton(relative_rect=pygame.Rect(360, 105, 30, 30), text='+',
                                    manager=self.manager)
        self.button_save = UIButton(relative_rect=pygame.Rect(820, 0, 80, 50), text='сохранить',
                                    manager=self.manager)
        


    def _load_shop(self) -> None:
        self.button_back = UIButton(relative_rect=pygame.Rect(2, 2, 50, 30), text='назад',
                                    manager=self.manager, )



class DatabaseManager:
    @classmethod
    def _connection_to_database(cls):
        with sqlite3.connect(FILENAME_DATABASE) as con:
            cur = con.cursor()
            print(type(con), type(cur))
            return con, cur

    @classmethod
    def get_characteristics_character(cls) -> tuple[str, int, int, int]:
        con, cur = cls._connection_to_database()
        result = cur.execute('SELECT name, health, damage, speed FROM characters '
                             'WHERE id=?', (ID_CHARACTER,)).fetchone()
        # print(result)
        con.close()
        return result
    
    def get_characteristics_settings(cls) -> tuple[int, int]:
        con, cur = cls._connection_to_database()
        result = cur.execute('SELECT progress_bar1, progress_bar2 FROM settings ').fetchone()
        con.close()
        print(result)
        return result
    
    def update_setting(cls, progress_bar1, progress_bar2) -> None:
        con, cur = cls._connection_to_database()
        cur.execute(f"UPDATE settings SET progress_bar1 = {progress_bar1}, progress_bar2 = {progress_bar2}")
        con.close()
        