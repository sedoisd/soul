from pygame import Rect
import pygame
import pygame_gui
from pygame_gui.elements import *
from constants import SIZE, FILENAME_DATABASE, ID_CHARACTER
# from initialization_classes import
from other_functions import get_front_frame_current_characters, get_frame_current_weapon, buy, get_weapon_settings
import sqlite3


class GuiManager:
    def __init__(self):
        self.manager = pygame_gui.UIManager(SIZE, 'theme.json')
        self.name = None
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
        self.label_image_character = UILabel(Rect((420, 370, 400, 400)), text='')
        self.image_character = get_front_frame_current_characters()
        # self.image_character = ц(self.image_character, 0, 0.2)
        self.label_image_character.set_image(self.image_character)
        self.label_name_character = UILabel(Rect((490, 600, 100, 30)), text='Рыцарь')
        # Weapon menu
        self.label_image_weapon = UILabel(Rect((170, 400, 150, 100)), text='')
        self.image_weapon = get_frame_current_weapon(0)
        self.label_image_weapon.set_image(self.image_weapon)
        self.label_name_weapon = UILabel(Rect((220, 600, 100, 30)), text='Меч')
        self.button_weapon_swap = UIButton(relative_rect=Rect((190, 650, 150, 50)),
                                text='сменить оружие', manager=self.manager, )
        self.button_characters_swap = UIButton(relative_rect=Rect((470, 650, 150, 50)),
                                text='сменить персонажа', manager=self.manager, )
        self.button_level1 = UIButton(relative_rect=Rect((140, 100, 100, 70)),
                                text='1 уровень', manager=self.manager, )
        self.button_level2 = UIButton(relative_rect=Rect((340, 100, 100, 70)),
                                text='2 уровень', manager=self.manager, )
        self.button_level3 = UIButton(relative_rect=Rect((540, 100, 100, 70)),
                                text='3 уровень', manager=self.manager, )
        self.button_play = UIButton(relative_rect=Rect((290, 250, 200, 70)),
                                text='ИГРАТЬ', manager=self.manager, )

    def _load_setting(self) -> None:
        money, progress_bar1, progress_bar2 = get_weapon_settings()
        self.button_back = UIButton(relative_rect=pygame.Rect(2, 2, 50, 30), text='назад',
                                    manager=self.manager)
        # image_button_back = pygame.image.load('image/back.png')
        # self.button_back._set_image(image_button_back)
        self.scroll_setting = UIVerticalScrollBar(relative_rect=pygame.Rect(10, 150, 20, 400), visible_percentage=0.5,
                                    manager=self.manager)
        self.button_sound = UILabel(relative_rect=pygame.Rect(50, 50, 100, 40), text='музыка',
                                    manager=self.manager)
        self.button_fihki = UILabel(relative_rect=pygame.Rect(50, 100, 100, 40), text='эффекты',
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
        shop = self.database_manager.shop()
        self.label_name_weapon  = UILabel(Rect((150, 400, 60, 30)), text=f'{shop[0][1]} - {shop[0][4]}$')
        self.label_image_weapon = UILabel(Rect((100, 180, 150, 100)), text='')
        self.image_weapon = get_frame_current_weapon(shop[0][2])
        self.label_image_weapon.set_image(self.image_weapon)
        self.scroll_shop = UIHorizontalScrollBar(relative_rect=pygame.Rect(200, 650, 400, 20), visible_percentage=0.5,
                            manager=self.manager)
        if not shop[0][3]:
            self.button_buy = UIButton(relative_rect=pygame.Rect(150, 450, 60, 30), text='купить',
                                    manager=self.manager)
            self.name = shop[0][1]
        else:
            self.label_image_weapon = UILabel(Rect((150, 450, 60, 30)), text='купленно')
        myonets = get_weapon_settings()[0]
        self.label_name_myonets  = UILabel(Rect((150, 50, 50, 30)), text=str(myonets)+"$")
        self.label_image_myonets = UILabel(Rect((120, 50, 30, 30)), text='')
        self.image_myonets =  pygame.image.load('image/other/icon-coin.png')
        self.label_image_myonets.set_image(self.image_myonets)


    def update_shop(self) -> None:
        self.button_buy.kill()
        self.label_image_weapon = UILabel(Rect((150, 450, 60, 30)), text='купленно')
        self.database_manager.update_inventory(self.name)
        buy(self.database_manager.buy(self.name))

    def load_swap_characters(self) -> None:
        self.exit_setting()
        f = get_weapon_settings
        self.button_back = UIButton(relative_rect=pygame.Rect(2, 2, 50, 30), text='назад',
                                    manager=self.manager, )
        self.label_image_characters1 = UILabel(Rect((100, 50, 400, 400)), text=f'')
        self.image_characters1 = get_front_frame_current_characters(0)
        self.label_image_characters1.set_image(self.image_weapon1)
        self.label_name_characters1 = UILabel(Rect((300, 500, 100, 50)), text=f'{f[4]}')
        self.label_name1  = UILabel(Rect((300, 600, 50, 30)), text='выбрано')
        characters = self.database_manager.get_character()
        self.label_image_characters2 = UILabel(Rect((550, 50, 400, 400)), text=f'')
        self.image_characters2 = get_front_frame_current_characters(1)
        self.label_image_characters2.set_image(self.image_weapon1)
        self.label_name_characters2 = UILabel(Rect((750, 500, 100, 50)), text=f'{characters[0][1]}')
        self.button_characters2  = UIButton(Rect((600, 600, 50, 30)), text='выбрать')
        self.label_image_characters3 = UILabel(Rect((550, 50, 400, 400)), text=f'')
        self.image_characters3 = get_front_frame_current_characters(2)
        self.label_image_characters3.set_image(self.image_weapon1)
        self.label_name_characters3 = UILabel(Rect((750, 500, 100, 50)), text=f'{characters[1][1]}')
        self.button_characters3  = UIButton(Rect((600, 600, 50, 30)), text='выбрать')

    def load_swap_weapons(self) -> None:
        self.exit_setting()
        f = get_weapon_settings
        self.button_back = UIButton(relative_rect=pygame.Rect(2, 2, 50, 30), text='назад',
                                    manager=self.manager, )
        self.label_image_weapon1 = UILabel(Rect((100, 50, 400, 400)), text=f'')
        self.image_weapon1 = get_front_frame_current_characters(0)
        self.label_image_weapon1.set_image(self.image_weapon1)
        self.label_name_weapon1 = UILabel(Rect((300, 500, 100, 50)), text=f'{f[4]}')
        self.label_name1  = UILabel(Rect((300, 600, 50, 30)), text='выбрано')
        characters = self.database_manager.get_character()
        self.label_image_weapon2 = UILabel(Rect((550, 50, 400, 400)), text=f'')
        self.image_weapon2 = get_front_frame_current_characters(1)
        self.label_image_weapon2.set_image(self.image_weapon1)
        self.label_name_weapon2 = UILabel(Rect((750, 500, 100, 50)), text=f'{characters[0][1]}')
        self.button_weapon2  = UIButton(Rect((600, 600, 50, 30)), text='выбрать')
        self.label_image_weapon3 = UILabel(Rect((550, 50, 400, 400)), text=f'')
        self.image_weapon3 = get_front_frame_current_characters(2)
        self.label_image_weapon3.set_image(self.image_weapon1)
        self.label_name_weapon3 = UILabel(Rect((750, 500, 100, 50)), text=f'{characters[1][1]}')
        self.button_weapon3  = UIButton(Rect((600, 600, 50, 30)), text='выбрать')

    def exit_setting(self):
        self.button_fihki.kill()
        self.button_sound.kill()
        self.progress_bar1_f.kill()
        self.progress_bar2_f.kill()
        self.button_save.kill()
        self.button_minys1.kill()
        self.button_minys2.kill()
        self.button_plus1.kill()
        self.button_plus2.kill()
        self.scroll_setting.kill()
    
    def exit_game1(self):
        self.label_image_character.kill()
        self.label_image_weapon.kill()
        self.label_name_character.kill()
        self.label_name_weapon.kill()
        self.button_weapon_swap.kill()
        self.button_characters_swap.kill()
        self.button_level1.kill()
        self.button_level2.kill()
        self.button_level3.kill()
        self.button_play.kill()
        
    def exit_shop(self):
        self.label_image_weapon.kill()
        self.label_name_weapon.kill()
        self.button_buy.kill()
        self.label_image_weapon.kill()
        self.scroll_shop.kill()
        self.label_image_myonets.kill()
        self.label_name_myonets.kill()



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
    
    @classmethod
    def update_inventory(cls, name):
        con, cur = cls._connection_to_database()
        cur.execute("UPDATE Weapons SET purchased = ? WHERE Name = ?", (1, name.lower())) 
        cur.execute
        con.close()

    def buy(cls, name):
        con, cur = cls._connection_to_database()
        answer = cur.execute("SELECT purchased WHERE Name = ?", (name.lower())).fetchone()
        print(answer)
        cur.execute
        con.close()
        return answer

    def shop(cls):
        con, cur = cls._connection_to_database()
        result = cur.execute(f"SELECT * FROM Weapons").fetchall()
        con.close()
        return result
    
    def get_characters(cls):
        con, cur = cls._connection_to_database()
        result = cur.execute('SELECT name, health, damage, speed FROM characters '
                             'WHERE id=?', (ID_CHARACTER,)).fetchall()
        con.close()
        return result
    
    def get_weapon(cls):
        con, cur = cls._connection_to_database()
        result = cur.execute('SELECT Name, filename_image, purchased, price FROM Weapons '
                             'WHERE id=?', (ID_CHARACTER,)).fetchall()
        con.close()
        return result