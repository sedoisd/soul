from pygame import Rect
import pygame
import pygame_gui
from pygame_gui.elements import *

from constants import SIZE, FILENAME_DATABASE
from other_functions import *
import sqlite3


class GuiManager:
    def __init__(self, func_start_level):
        self.manager = pygame_gui.UIManager(SIZE, 'theme.json')
        self.name = None
        self.mode = 'menu'
        self.func_start_level = func_start_level

    def get_mode(self):
        return self.mode

    def load_values_mixer(self, sound_open):
        self.sound_open = sound_open

    def start_game(self):
        pass

    def update(self):
        pass

    def event_processing(self, event):
        self.manager.process_events(event)
        # try:
        if event.type == pygame_gui.UI_BUTTON_PRESSED:  # Нажатие на кнопки
            self.sound_open.play()
            if self.mode == 'menu':
                if event.ui_element == self.button_start:
                    self.kill_start_menu()
            elif self.mode == 'selection':
                if event.ui_element == self.button_back:
                    self.exit_selection_window()
                    self.load_start_menu()
            elif self.mode == 'setting':
                if event.ui_element == self.button_back:
                    self.exit_setting()
                    self.load_start_menu()
                    DatabaseManager.update_volume_settings(*self.get_values_volume())
                volume_music = self.music_progress_bar.current_progress
                if event.ui_element == self.music_button_minus and volume_music >= 5:  # Обработка громкости музыки
                    volume_music -= 5
                    self.music_progress_bar.set_current_progress(volume_music)
                elif event.ui_element == self.music_button_plus and volume_music <= 95:
                    volume_music += 5
                    self.music_progress_bar.set_current_progress(volume_music)
                volume_effects = self.effects_progress_bar.current_progress
                if event.ui_element == self.effects_button_minus and volume_effects >= 5:  # Обр. громкости эффектов
                    volume_effects -= 5
                    self.effects_progress_bar.set_current_progress(volume_effects)
                elif event.ui_element == self.effects_button_plus and volume_effects <= 95:
                    volume_effects += 5
                    self.effects_progress_bar.set_current_progress(volume_effects)
                self.sound_open.set_volume(volume_effects / 100)
                DatabaseManager.update_volume_settings(volume_music, volume_effects)
            elif self.mode == 'shop':
                if event.ui_element == self.button_back:
                    self.exit_shop()
                    self.load_start_menu()
        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if self.mode == 'selection':
                if event.ui_element == self.weapon_drop_menu:
                    new_current_weapon_id = self.dict_purchased_weapons_by_name[event.text]
                    DatabaseManager.update_current_id_by_group('weapons', new_current_weapon_id)
                    new_weapon_image = get_frame_weapon_by_id(DatabaseManager.get_current_id_by_group('weapons'))
                    new_name_weapon = DatabaseManager.get_current_name_by_group('weapons')
                    self.weapon_ui_image.set_image(new_weapon_image)
                    self.weapon_name_label.set_text(new_name_weapon)
                elif event.ui_element == self.characters_drop_menu:
                    new_current_character_id = self.dict_purchased_characters_by_name[event.text]
                    DatabaseManager.update_current_id_by_group('characters', new_current_character_id)
                    new_character_image = get_front_frame_characters_by_id(
                        DatabaseManager.get_current_id_by_group('characters'))
                    new_name_characters = DatabaseManager.get_current_name_by_group('characters')
                    self.character_ui_image.set_image(new_character_image)
                    self.weapon_name_label.set_text(new_name_characters)
                # print(event.text, event.selected_option_id, event.ui_element == self.weapon_drop_menu)
            #     elif self.gui_mode == 'shop':
            #         if event.ui_element == self.gui_manager.button_buy:
            #             self.database_manager.update_inventory(self.gui_manager.name)
            #             self.gui_manager.update_shop()
            #         elif event.ui_element == self.gui_manager.button_weapon_swap:
            #             self.gui_manager.load_swap_weapon()
            #         elif event.ui_element == self.gui_manager.button_characters_swap:
            #             self.gui_manager.load_swap_characters()

    def load_start_menu(self) -> None:
        def redirection(command_load=None) -> None:
            self.kill_start_menu()
            command_load()

        self.mode = 'menu'

        self.button_start = UIButton(relative_rect=Rect((340, 220, 200, 70)),
                                     text='Играть', manager=self.manager,
                                     command=lambda: redirection(self._load_selection_window))
        self.button_shop = UIButton(relative_rect=Rect((340, 320, 200, 70)),
                                    text='Магазин', manager=self.manager,
                                    command=lambda: redirection(self._load_shop))
        self.button_setting = UIButton(relative_rect=Rect((340, 420, 200, 70)),
                                       text='Настройки', manager=self.manager,
                                       command=lambda: redirection(self._load_setting))
        self.button_exit = UIButton(relative_rect=Rect((340, 520, 200, 70)),
                                    text='Выход', manager=self.manager)

    def kill_start_menu(self) -> None:
        self.button_start.kill()
        self.button_shop.kill()
        self.button_setting.kill()
        self.button_exit.kill()

    def _load_selection_window(self) -> None:
        def edit_current_lvl(id_lvl):
            self.current_lvl = id_lvl

        def start_lvl(current_lvl):
            self.mode = None
            self.exit_selection_window()
            self.func_start_level(current_lvl)

        self.mode = 'selection'
        self.current_lvl = 1
        self.button_back = UIButton(relative_rect=pygame.Rect(2, 2, 50, 30), text='назад',
                                    manager=self.manager)
        # Character
        characters_image = get_front_frame_characters_by_id(DatabaseManager.get_current_id_by_group('characters'))
        name_characters = DatabaseManager.get_current_name_by_group('characters')
        purchased_characters = DatabaseManager.get_purchased_items_by_group('characters')
        characters_optional_list = list(map(lambda x: x[1], purchased_characters))
        characters_start_option = DatabaseManager.get_current_name_by_group('characters')
        self.dict_purchased_characters_by_name = dict()
        for char_id, name in purchased_characters:
            self.dict_purchased_characters_by_name[name] = char_id

        self.character_ui_image = UIImage(Rect((515, 30, 100, 100)), characters_image)
        self.character_name_label = UILabel(Rect((515, 145, 100, 30)), text=name_characters)
        self.characters_drop_menu = UIDropDownMenu(relative_rect=Rect((502, 250, 150, 50)), manager=self.manager,
                                                   options_list=characters_optional_list,
                                                   starting_option=characters_start_option)

        # Weapon
        weapon_image = get_frame_weapon_by_id(DatabaseManager.get_current_id_by_group('weapons'))
        weapon_name = DatabaseManager.get_current_name_by_group('weapons')
        purchased_weapons = DatabaseManager.get_purchased_items_by_group('weapons')
        weapon_optional_list = list(map(lambda x: x[1], purchased_weapons))
        weapon_start_option = DatabaseManager.get_current_name_by_group('weapons')
        self.dict_purchased_weapons_by_name = dict()
        for char_id, name in purchased_weapons:
            self.dict_purchased_weapons_by_name[name] = char_id

        self.weapon_ui_image = UIImage(Rect((140, 30, 100, 100)), weapon_image)
        self.weapon_name_label = UILabel(Rect((160, 200, 100, 30)), text=weapon_name)
        self.weapon_drop_menu = UIDropDownMenu(relative_rect=Rect((160, 240, 150, 50)), manager=self.manager,
                                               options_list=weapon_optional_list, starting_option=weapon_start_option)

        # Выбор ЛВЛа и старт
        self.button_level1 = UIButton(relative_rect=Rect((300, 600, 100, 70)),
                                      text='1 уровень', manager=self.manager,
                                      command=lambda: edit_current_lvl(1))
        self.button_level2 = UIButton(relative_rect=Rect((400, 600, 100, 70)),
                                      text='2 уровень', manager=self.manager,
                                      command=lambda: edit_current_lvl(2))
        self.button_level3 = UIButton(relative_rect=Rect((500, 600, 100, 70)),
                                      text='3 уровень', manager=self.manager,
                                      command=lambda: edit_current_lvl(3))
        self.button_play = UIButton(relative_rect=Rect((350, 500, 200, 70)),
                                    text='ИГРАТЬ', manager=self.manager,
                                    command=lambda: start_lvl(self.current_lvl))

    def exit_selection_window(self):
        self.button_back.kill()

        self.character_ui_image.kill()
        self.character_name_label.kill()
        self.characters_drop_menu.kill()

        self.weapon_ui_image.kill()
        self.weapon_name_label.kill()
        self.weapon_drop_menu.kill()

        self.button_level1.kill()
        self.button_level2.kill()
        self.button_level3.kill()
        self.button_play.kill()

    def _load_setting(self) -> None:
        self.mode = 'setting'
        # Громкость звука всe категории
        volume_music, volume_effects = DatabaseManager.get_settings_values()
        self.button_back = UIButton(relative_rect=pygame.Rect(2, 2, 50, 30), text='назад',
                                    manager=self.manager)
        # image_button_back = pygame.image.load('image/back.png')
        # self.button_back._set_image(image_button_back)
        self.scroll_setting = UIVerticalScrollBar(relative_rect=pygame.Rect(10, 150, 20, 400), visible_percentage=0.5,
                                                  manager=self.manager)
        self.music_label = UILabel(relative_rect=pygame.Rect(50, 50, 100, 40), text='Музыка',
                                   manager=self.manager)
        self.effects_label = UILabel(relative_rect=pygame.Rect(50, 100, 100, 40), text='Эффекты',
                                     manager=self.manager)

        self.music_progress_bar = UIProgressBar(relative_rect=pygame.Rect((250, 55), (100, 30)),
                                                manager=self.manager)
        self.music_progress_bar.set_current_progress(volume_music)
        self.effects_progress_bar = UIProgressBar(relative_rect=pygame.Rect((250, 105), (100, 30)),
                                                  manager=self.manager)
        self.effects_progress_bar.set_current_progress(volume_effects)

        self.music_button_minus = UIButton(relative_rect=pygame.Rect(210, 55, 30, 30), text='-',
                                           manager=self.manager)
        self.music_button_plus = UIButton(relative_rect=pygame.Rect(360, 55, 30, 30), text='+',
                                          manager=self.manager)

        self.effects_button_minus = UIButton(relative_rect=pygame.Rect(210, 105, 30, 30), text='-',
                                             manager=self.manager)
        self.effects_button_plus = UIButton(relative_rect=pygame.Rect(360, 105, 30, 30), text='+',
                                            manager=self.manager)
        # print(self.music_progress_bar.current_progress)
        # self.button_save = UIButton(relative_rect=pygame.Rect(820, 0, 80, 50), text='сохранить',
        #                             manager=self.manager)

    def get_values_volume(self) -> (int, int):
        return self.music_progress_bar.current_progress, self.effects_progress_bar.current_progress

    def exit_setting(self):
        self.button_back.kill()
        self.music_label.kill()
        self.music_progress_bar.kill()
        self.music_button_minus.kill()
        self.music_button_plus.kill()

        self.effects_label.kill()
        self.effects_progress_bar.kill()
        self.effects_button_plus.kill()
        self.effects_button_minus.kill()

        self.scroll_setting.kill()

    def _load_shop(self) -> None:
        def characters_navigation(direction: str):
            if direction == 'father':
                self.characters_viewing_index += 1
                if self.characters_viewing_index == 1:
                    self.characters_button_back.enable()
                if self.characters_viewing_index == len(self.shop_characteristic_all_characters) - 1:
                    self.characters_button_farther.disable()
            elif direction == 'back':
                self.characters_viewing_index -= 1
                if self.characters_viewing_index == 0:
                    self.characters_button_back.disable()
                if self.characters_viewing_index == len(self.shop_characteristic_all_characters) - 2:
                    self.characters_button_farther.enable()
            # Загрузка нового содержимого
            new_character_image = get_front_frame_characters_by_id(
                self.shop_characteristic_all_characters[self.characters_viewing_index][0])
            new_character_name = self.shop_characteristic_all_characters[self.characters_viewing_index][1]
            new_character_price = str(self.shop_characteristic_all_characters[self.characters_viewing_index][2])
            self.character_ui_image.set_image(new_character_image)
            self.character_name_label.set_text(new_character_name)
            self.character_price_label.set_text(new_character_price)

        def weapons_navigation(direction: str):
            if direction == 'father':
                self.weapons_viewing_index += 1
                if self.weapons_viewing_index == 1:
                    self.weapons_button_back.enable()
                if self.weapons_viewing_index == len(self.shop_characteristic_all_weapons) - 1:
                    self.weapons_button_farther.disable()
            elif direction == 'back':
                self.weapons_viewing_index -= 1
                if self.weapons_viewing_index == 0:
                    self.weapons_button_back.disable()
                if self.weapons_viewing_index == len(self.shop_characteristic_all_weapons) - 2:
                    self.weapons_button_farther.enable()
            # Загрузка нового содержимого
            new_weapon_image = get_frame_weapon_by_id(
                self.shop_characteristic_all_weapons[self.weapons_viewing_index][0])
            new_weapon_name = self.shop_characteristic_all_weapons[self.weapons_viewing_index][1]
            new_weapon_price = str(self.shop_characteristic_all_weapons[self.weapons_viewing_index][2])
            self.weapon_ui_image.set_image(new_weapon_image)
            self.weapon_name_label.set_text(new_weapon_name)
            self.weapon_price_label.set_text(new_weapon_price)

        self.mode = 'shop'
        self.button_back = UIButton(relative_rect=pygame.Rect(2, 2, 50, 30), text='назад',
                                    manager=self.manager)
        # Загрузка монет
        money = DatabaseManager.get_money()
        money_image = load_image('coin.png', 'other')
        self.money_label = UILabel(Rect((150, 40, 60, 30)), text=f'{money} монет')
        self.money_ui_image = UIImage(Rect((100, 40, 40, 40)), money_image)

        # загрузка магазина персонажей
        self.characters_viewing_index = 0
        self.shop_characteristic_all_characters = DatabaseManager.get_shop_characteristic_all_items_by_group(
            'characters')  # [(id, name, price, health, armor, speed), (int, name, int, int, int), ...]
        character_image = get_front_frame_characters_by_id(
            self.shop_characteristic_all_characters[self.characters_viewing_index][0])
        character_name = self.shop_characteristic_all_characters[self.characters_viewing_index][1]
        character_price = str(self.shop_characteristic_all_characters[
                                  self.characters_viewing_index][2])
        self.character_ui_image = UIImage(Rect((150, 200, 100, 100)), character_image)
        self.character_name_label = UILabel(Rect((155, 310, 80, 30)), text=character_name)
        # print(self.shop_characteristic_all_characters)
        self.character_price_label = UILabel(Rect((175, 345, 40, 20)),
                                             text=character_price)

        self.characters_button_back = UIButton(Rect((110, 280, 30, 25)), text='<-',
                                               command=lambda: characters_navigation('back'))
        self.characters_button_back.disable()
        self.characters_button_farther = UIButton(Rect((275, 280, 30, 25)), text='->',
                                                  command=lambda: characters_navigation('father'))

        # загрузка магазина оружий
        self.weapons_viewing_index = 0
        self.shop_characteristic_all_weapons = DatabaseManager.get_shop_characteristic_all_items_by_group(
            'weapons')  # [(id, name, price, damage, attack_distance), (int, name, int, int), ...]
        weapon_image = get_frame_weapon_by_id(
            self.shop_characteristic_all_weapons[self.characters_viewing_index][0])
        weapon_name = self.shop_characteristic_all_characters[self.characters_viewing_index][1]
        weapon_price = str(self.shop_characteristic_all_weapons[
                                  self.weapons_viewing_index][2])
        self.weapon_ui_image = UIImage(Rect((560, 180, 100, 100)), weapon_image)
        self.weapon_name_label = UILabel(Rect((580, 310, 80, 30)), text=weapon_name)
        # print(self.shop_characteristic_all_characters)
        self.weapon_price_label = UILabel(Rect((600, 345, 40, 20)),
                                             text=weapon_price)

        self.weapons_button_back = UIButton(Rect((520, 280, 30, 25)), text='<-',
                                               command=lambda: weapons_navigation('back'))
        self.weapons_button_back.disable()
        self.weapons_button_farther = UIButton(Rect((680, 280, 30, 25)), text='->',
                                                  command=lambda: weapons_navigation('father'))

    def exit_shop(self):
        self.button_back.kill()

        self.money_ui_image.kill()
        self.money_label.kill()

        self.character_ui_image.kill()
        self.character_name_label.kill()
        self.character_price_label.kill()
        self.characters_button_back.kill()
        self.characters_button_farther.kill()

    # def load_swap_characters(self) -> None:
    #     self.exit_setting()
    #     f = get_weapon_settings
    #     self.button_back = UIButton(relative_rect=pygame.Rect(2, 2, 50, 30), text='назад',
    #                                 manager=self.manager, )
    #     self.label_image_characters1 = UILabel(Rect((100, 50, 400, 400)), text=f'')
    #     self.image_characters1 = get_front_frame_characters_by_id(DatabaseManager.get_current_character_id())
    #     self.label_image_characters1.set_image(self.image_weapon1)
    #     self.label_name_characters1 = UILabel(Rect((300, 500, 100, 50)), text=f'{f[4]}')
    #     self.label_name1 = UILabel(Rect((300, 600, 50, 30)), text='выбрано')
    #     characters = self.database_manager.get_character()
    #     self.label_image_characters2 = UILabel(Rect((550, 50, 400, 400)), text=f'')
    #     self.image_characters2 = get_front_frame_characters_by_id(DatabaseManager.get_current_character_id())
    #     self.label_image_characters2.set_image(self.image_weapon1)
    #     self.label_name_characters2 = UILabel(Rect((750, 500, 100, 50)), text=f'{characters[0][1]}')
    #     self.button_characters2 = UIButton(Rect((600, 600, 50, 30)), text='выбрать')
    #     self.label_image_characters3 = UILabel(Rect((550, 50, 400, 400)), text=f'')
    #     self.image_characters3 = get_front_frame_characters_by_id(DatabaseManager.get_current_character_id())
    #     self.label_image_characters3.set_image(self.image_weapon1)
    #     self.label_name_characters3 = UILabel(Rect((750, 500, 100, 50)), text=f'{characters[1][1]}')
    #     self.button_characters3 = UIButton(Rect((600, 600, 50, 30)), text='выбрать')

    # def load_swap_weapons(self) -> None:
    #     self.exit_setting()
    #     f = get_weapon_settings
    #     self.button_back = UIButton(relative_rect=pygame.Rect(2, 2, 50, 30), text='назад',
    #                                 manager=self.manager, )
    #     self.label_image_weapon1 = UILabel(Rect((100, 50, 400, 400)), text=f'')
    #     self.image_weapon1 = get_frame_weapon_by_id(DatabaseManager.get_current_weapon_id())
    #     self.label_image_weapon1.set_image(self.image_weapon1)
    #     self.label_name_weapon1 = UILabel(Rect((300, 500, 100, 50)), text=f'{f}')
    #     self.label_name1 = UILabel(Rect((300, 600, 50, 30)), text='выбрано')
    #     characters = DatabaseManager.get_current_character_id()
    #     self.label_image_weapon2 = UILabel(Rect((550, 50, 400, 400)), text=f'')
    #     self.image_weapon2 = get_frame_weapon_by_id(DatabaseManager.get_current_weapon_id())
    #     self.label_image_weapon2.set_image(self.image_weapon1)
    #     self.label_name_weapon2 = UILabel(Rect((750, 500, 100, 50)), text=f'{characters}')
    #     self.button_weapon2 = UIButton(Rect((600, 600, 50, 30)), text='выбрать')
    #     self.label_image_weapon3 = UILabel(Rect((550, 50, 400, 400)), text=f'')
    #     self.image_weapon3 = get_frame_weapon_by_id(DatabaseManager.get_current_weapon_id())
    #     self.label_image_weapon3.set_image(self.image_weapon1)
    #     self.label_name_weapon3 = UILabel(Rect((750, 500, 100, 50)), text=f'{characters}')
    #     self.button_weapon3 = UIButton(Rect((600, 600, 50, 30)), text='выбрать')


class DatabaseManager:
    @classmethod
    def _connection_to_database(cls):
        with sqlite3.connect(FILENAME_DATABASE) as con:
            cur = con.cursor()
            return con, cur

    @classmethod
    def get_characteristics_character(cls) -> tuple[str, int, int, int, int]:
        con, cur = cls._connection_to_database()
        result = cur.execute('''SELECT name, health, damage, speed, armor FROM characters
                             WHERE id=?''',
                             (DatabaseManager.get_current_id_by_group('characters'),)).fetchone()
        # print(result) # [LOG]
        con.close()
        return result

    @classmethod
    def get_characteristics_enemy_by_id(cls, enemy_id: int) -> tuple[str, int, int, int, int]:
        con, cur = cls._connection_to_database()
        result = cur.execute('''SELECT name, health, damage, attack_distance, speed FROM enemies
                             WHERE id=?''', (enemy_id,)).fetchone()
        # print(result) # [LOG]
        con.close()
        return result

    @classmethod
    def get_quantities_frames_enemy_by_id(cls, enemy_id: int) -> tuple[int, int, int, int]:
        con, cur = cls._connection_to_database()
        result = cur.execute('''SELECT quan_walking_frames, quan_attack_frames, 
                             quan_death_frames, quan_stand_frame FROM enemies
                             WHERE ID=?''', (enemy_id,)).fetchone()
        con.close()
        return result

    @classmethod
    def get_current_id_by_group(cls, group_name: str) -> int:
        con, cur = cls._connection_to_database()
        if group_name == 'characters':
            result = cur.execute('''SELECT current_character FROM user''').fetchone()[0]
        elif group_name == 'weapons':
            result = cur.execute('''SELECT current_weapon FROM user''').fetchone()[0]
        con.close()
        return result

    @classmethod
    def get_current_name_by_group(cls, group_name: str) -> str:
        con, cur = cls._connection_to_database()
        cur_id = DatabaseManager.get_current_id_by_group(group_name)
        if group_name == 'characters':
            result = cur.execute('''SELECT name FROM characters WHERE id=?''', (cur_id,)).fetchone()[0]
        elif group_name == 'weapons':
            result = cur.execute('''SELECT name FROM weapons WHERE id=?''', (cur_id,)).fetchone()[0]
        con.close()
        return result

    @classmethod
    def get_shop_characteristic_all_items_by_group(cls, group_name: str):
        con, cur = cls._connection_to_database()
        if group_name == 'characters':
            result = cur.execute('''SELECT id, name, price, health, armor, speed FROM characters''').fetchall()
        elif group_name == 'weapons':
            result = cur.execute('''SELECT id, name, price, damage, attack_distance FROM weapons''').fetchall()
            con.close()
        return result

    @classmethod
    def get_characteristics_weapon_by_id(cls, weapon_id: int) -> tuple[float, float, int]:
        con, cur = cls._connection_to_database()
        result = cur.execute('''SELECT damage, scale, attack_distance FROM weapons WHERE id=?''',
                             (weapon_id,)).fetchone()
        con.close()
        return result

    @classmethod
    def get_settings_values(cls) -> tuple[int, int]:
        con, cur = cls._connection_to_database()
        result = cur.execute('SELECT volume_music, volume_effects FROM user').fetchone()
        # print(result)
        con.close()
        return result

    @classmethod
    def get_purchased_items_by_group(cls, group_name: str):
        con, cur = cls._connection_to_database()
        if group_name == 'characters':
            result = cur.execute('''SELECT id, name FROM characters WHERE purchased=1''').fetchall()
        elif group_name == 'weapons':
            result = cur.execute('''SELECT id, name FROM weapons WHERE purchased=1''').fetchall()
        con.close()
        return result

    @classmethod
    def get_money(cls) -> int:
        con, cur = cls._connection_to_database()
        result = cur.execute('''SELECT money FROM user''').fetchone()[0]
        con.close()
        return result

    @classmethod
    def update_volume_settings(cls, volume_music, volume_effects) -> None:
        con, cur = cls._connection_to_database()
        cur.execute('''UPDATE user SET 
                            volume_music = ?, 
                            volume_effects = ?
                    ''', (volume_music, volume_effects))
        con.commit()
        con.close()

    @classmethod
    def update_current_id_by_group(cls, group_name, current_id: int) -> None:
        con, cur = cls._connection_to_database()
        if group_name == 'characters':
            cur.execute('''UPDATE user SET current_character = ? ''', (current_id,))
        elif group_name == 'weapons':
            cur.execute('''UPDATE user SET current_weapon = ?''', (current_id,))
        con.commit()
        con.close()

    # @classmethod
    # def shop(cls):
    #     con, cur = cls._connection_to_database()
    #     result = cur.execute(f"SELECT * FROM Weapons").fetchall()
    #     con.close()
    #     return result

    @classmethod
    def update_inventory(cls, name):
        con, cur = cls._connection_to_database()
        cur.execute(f"UPDATE settings SET purchased = {1} WHERE Name = {name}")
        con.close()


class SpriteGroupManager:
    def __init__(self):

        self.all_gameplay = pygame.sprite.Group()
        self.movable_for_gameplay = pygame.sprite.Group()
        self.player = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.trap = pygame.sprite.Group()
        self.hud = pygame.sprite.Group()
        self.portal = pygame.sprite.Group()
        self.hud_main_sprite = None
        self.cursor = pygame.sprite.Group()
        self.weapon = pygame.sprite.Group()
        self.enemy_status_bar = pygame.sprite.Group()

        self.all_tiles = pygame.sprite.Group()

    def update(self, is_going_game: bool, timedelta: float):
        if is_going_game:
            self.player.update(timedelta=timedelta, mode='update', group_walls=self.walls, group_trap=self.trap)
            self.enemies.update(*self.player.sprites(), timedelta)
            self.hud_main_sprite.update(*self.player.sprites()[0].get_value_for_hud())
            flag_trap = any(map(lambda x: x.flag_angry, self.enemies))  # or self._is_nearby_enemy()
            self.trap.update(flag_trap)
            self.portal.update(timedelta, self.enemies)

    def draw(self, screen: pygame.Surface, is_going_game: bool):
        if is_going_game:
            self.all_tiles.draw(screen)
            self.trap.draw(screen)
            self.portal.draw(screen)
            self.player.draw(screen)
            self.enemies.draw(screen)
            self.enemy_status_bar.draw(screen)
            self.hud.draw(screen)
            self.weapon.draw(screen)
            self.cursor.draw(screen)

    def add_hud(self, sprite):
        self.hud_main_sprite = sprite
        self.hud.add(sprite)
        for subsprite in sprite.get_sprites_status_bar():
            self.hud.add(subsprite)

    def _add_gameplay(self, sprite):
        self.all_gameplay.add(sprite)
        self.movable_for_gameplay.add(sprite)

    def get_movable_sprites(self) -> list:
        return self.movable_for_gameplay.sprites()

    def get_portal_sprite(self):
        return self.portal.sprites()[0]

    def add_tile_sprite_by_id_layer(self, sprite, id_layer: int):

        groups = [self.all_gameplay, self.movable_for_gameplay, self.all_tiles]
        if id_layer == 2:
            groups.append(self.walls)
        elif id_layer == 3:
            groups.append(self.trap)

        for group in groups:
            group.add(sprite)

    def add_player(self, sprite):
        self._add_gameplay(sprite)
        self.player.add(sprite)
        # self._add_gameplay(sprite.weapon)
        self.weapon.add(sprite.weapon)

    def add_enemy(self, sprite):
        self._add_gameplay(sprite)
        self.enemies.add(sprite)
        self._add_gameplay(sprite.status_bar)
        self.enemy_status_bar.add(sprite.status_bar)

    def add_portal(self, sprite):
        self._add_gameplay(sprite)
        self.portal.add(sprite)

    def add_cursor(self, sprite):
        self.cursor.add(sprite)

    def kill_gameplay_sprites(self):
        for sprite in self.all_gameplay:
            sprite.kill()
        for sprite in self.hud:
            sprite.kill()
        for sprite in self.weapon:
            sprite.kill()
