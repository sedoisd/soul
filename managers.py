from pygame import Rect
import pygame
import pygame_gui
from pygame_gui.elements import *

from constants import SIZE, FILENAME_DATABASE
from other_functions import *
import sqlite3


# class GuiManager:
#     def __init__(self):
#         self.manager = pygame_gui.UIManager(SIZE)
#
#     def start_game(self):
#         pass
#
#     def kill_start_menu(self) -> None:
#         self.button_start.kill()
#         self.button_shop.kill()
#         self.button_setting.kill()
#         self.button_exit.kill()
#         self.image_character = None
#         self.label_image_character.kill()
#         self.label_name_character.kill()
#         self.image_weapon = None
#         self.label_image_weapon.kill()
#         self.label_name_weapon.kill()
#
#     def load_start_menu(self) -> None:
#         def redirection(command_load=None) -> None:
#             self.kill_start_menu()
#             command_load()
#
#         size_button = (200, 70)
#         self.button_start = UIButton(relative_rect=Rect((30, 180, *size_button)),
#                                      text='Старт', manager=self.manager, )
#         self.button_shop = UIButton(relative_rect=Rect((30, 270, *size_button)),
#                                     text='Магазин', manager=self.manager,
#                                     command=lambda: redirection(self._load_shop))
#         self.button_setting = UIButton(relative_rect=Rect((30, 360, *size_button)),
#                                        text='Настройки', manager=self.manager,
#                                        command=lambda: redirection(self._load_setting))
#         self.button_exit = UIButton(relative_rect=Rect((30, 450, *size_button)),
#                                     text='Выход', manager=self.manager)
#
#         # Character menu
#         self.label_image_character = UILabel(Rect((620, 50, 150, 400)), text='')
#         self.image_character = get_front_frame_characters_by_id(DatabaseManager.get_current_character_id())
#         # self.image_character = ц(self.image_character, 0, 0.2)
#         self.label_image_character.set_image(self.image_character)
#         self.label_name_character = UILabel(Rect((690, 310, 100, 30)), text='Рыцарь')
#
#         # Weapon menu
#         self.label_image_weapon = UILabel(Rect((350, 60, 150, 100)), text='')
#         self.image_weapon = get_frame_weapon_by_id(DatabaseManager.get_current_weapon_id())
#         # self.label_image_weapon.set_image(self.image_weapon)
#         self.label_name_weapon = UILabel(Rect((410, 315, 60, 30)), text='Меч')
#
#     def _load_setting(self) -> None:
#         def back():
#             self.button_back.kill()
#             self.load_start_menu()
#
#         self.button_back = UIButton(relative_rect=pygame.Rect(2, 2, 40, 40), text='back',
#                                     manager=self.manager, command=back)
#         # image_button_back = pygame.image.load('image/back.png')
#         # self.button_back._set_image(image_button_back)
#
#     def _load_shop(self) -> None:
#         def back():
#             self.button_back.kill()
#             self.load_start_menu()
#
#         self.button_back = UIButton(relative_rect=pygame.Rect(2, 2, 40, 40), text='back',
#                                     manager=self.manager, command=back)
class GuiManager:
    def __init__(self, func_start_level):
        self.manager = pygame_gui.UIManager(SIZE, 'theme.json')
        self.name = None
        self.mode = 'menu'
        self.func_start_level = func_start_level

    def load_values_mixer(self, sound_open):
        self.sound_open = sound_open

    def start_game(self):
        pass

    def update(self):
        pass

    def event_processing(self, event):
        self.manager.process_events(event)
        # try:
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            self.sound_open.play()
            if self.mode == 'menu':
                if event.ui_element == self.button_start:
                    self.kill_start_menu()
                    # self.start_game1()
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
            #     elif self.gui_mode == 'shop':
            #         if event.ui_element == self.gui_manager.button_buy:
            #             self.database_manager.update_inventory(self.gui_manager.name)
            #             self.gui_manager.update_shop()
            #         elif event.ui_element == self.gui_manager.button_weapon_swap:
            #             self.gui_manager.load_swap_weapon()
            #         elif event.ui_element == self.gui_manager.button_characters_swap:
            #             self.gui_manager.load_swap_characters()

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
        self.button_start = UIButton(relative_rect=Rect((340, 220, 200, 70)),
                                     text='Играть', manager=self.manager,
                                     command=lambda: redirection(self._load_selection_window_for_start_game))
        self.button_shop = UIButton(relative_rect=Rect((340, 320, 200, 70)),
                                    text='Магазин', manager=self.manager,
                                    command=lambda: redirection(self._load_shop))
        self.button_setting = UIButton(relative_rect=Rect((340, 420, 200, 70)),
                                       text='Настройки', manager=self.manager,
                                       command=lambda: redirection(self._load_setting))
        self.button_exit = UIButton(relative_rect=Rect((340, 520, 200, 70)),
                                    text='Выход', manager=self.manager)

    def _load_selection_window_for_start_game(self) -> None:
        def edit_cur_lvl(id_lvl):
            self.current_lvl = id_lvl

        def start_lvl(cur_lvl):
            self.exit_selection_window()
            self.func_start_level(cur_lvl)

        self.mode = 'selection'
        self.current_lvl = 1
        self.button_back = UIButton(relative_rect=pygame.Rect(2, 2, 50, 30), text='назад',
                                    manager=self.manager)
        # Character menu
        self.label_image_character = UILabel(Rect((420, 370, 400, 400)), text='')
        self.image_character = get_front_frame_characters_by_id(DatabaseManager.get_current_character_id())
        # self.image_character = ц(self.image_character, 0, 0.2)
        self.label_image_character.set_image(self.image_character)
        self.label_name_character = UILabel(Rect((490, 600, 100, 30)), text='Рыцарь')
        # Weapon menu
        self.label_image_weapon = UILabel(Rect((170, 400, 150, 100)), text='')
        self.image_weapon = get_frame_weapon_by_id(DatabaseManager.get_current_weapon_id())
        self.label_image_weapon.set_image(self.image_weapon)
        self.label_name_weapon = UILabel(Rect((220, 600, 100, 30)), text='Меч')

        self.button_weapon_swap = UIButton(relative_rect=Rect((190, 650, 150, 50)),
                                           text='Cменить оружие', manager=self.manager, )
        self.button_characters_swap = UIButton(relative_rect=Rect((470, 650, 150, 50)),
                                               text='Cменить персонажа', manager=self.manager, )
        self.button_level1 = UIButton(relative_rect=Rect((140, 100, 100, 70)),
                                      text='1 уровень', manager=self.manager,
                                      command=lambda: edit_cur_lvl(1))
        self.button_level2 = UIButton(relative_rect=Rect((340, 100, 100, 70)),
                                      text='2 уровень', manager=self.manager,
                                      command=lambda: edit_cur_lvl(2))
        self.button_level3 = UIButton(relative_rect=Rect((540, 100, 100, 70)),
                                      text='3 уровень', manager=self.manager,
                                      command=lambda: edit_cur_lvl(3))
        self.button_play = UIButton(relative_rect=Rect((290, 250, 200, 70)),
                                    text='ИГРАТЬ', manager=self.manager,
                                    command=lambda: start_lvl(self.current_lvl))

    def exit_selection_window(self):
        self.button_back.kill()
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

    def _load_setting(self) -> None:
        self.mode = 'setting'
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

    def get_values_volume(self):
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
        self.mode = 'shop'
        self.button_back = UIButton(relative_rect=pygame.Rect(2, 2, 50, 30), text='назад',
                                    manager=self.manager, )
        shop = DatabaseManager.shop()
        self.label_name_weapon = UILabel(Rect((150, 400, 60, 30)), text=f'{shop[0][1]} - {shop[0][4]}$')
        self.label_image_weapon = UILabel(Rect((100, 180, 150, 100)), text='')
        self.image_weapon = get_frame_weapon_by_id(DatabaseManager.get_current_weapon_id())
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
        self.label_name_myonets = UILabel(Rect((150, 50, 50, 30)), text=str(myonets) + "$")
        self.label_image_myonets = UILabel(Rect((120, 50, 30, 30)), text='')
        self.image_myonets = pygame.image.load('image/other/icon-coin.png')
        self.label_image_myonets.set_image(self.image_myonets)

    def update_shop(self) -> None:
        self.button_buy.kill()
        self.label_image_weapon = UILabel(Rect((150, 450, 60, 30)), text='купленно')
        DatabaseManager.update_inventory(self.name)
        buy(DatabaseManager.buy(self.name))

    def exit_shop(self):
        self.button_back.kill()
        self.label_image_weapon.kill()
        self.label_name_weapon.kill()
        # self.button_buy.kill()
        self.label_image_weapon.kill()
        self.scroll_shop.kill()
        self.label_image_myonets.kill()
        self.label_name_myonets.kill()

    def load_swap_characters(self) -> None:
        self.exit_setting()
        f = get_weapon_settings
        self.button_back = UIButton(relative_rect=pygame.Rect(2, 2, 50, 30), text='назад',
                                    manager=self.manager, )
        self.label_image_characters1 = UILabel(Rect((100, 50, 400, 400)), text=f'')
        self.image_characters1 = get_front_frame_characters_by_id(DatabaseManager.get_current_character_id())
        self.label_image_characters1.set_image(self.image_weapon1)
        self.label_name_characters1 = UILabel(Rect((300, 500, 100, 50)), text=f'{f[4]}')
        self.label_name1 = UILabel(Rect((300, 600, 50, 30)), text='выбрано')
        characters = self.database_manager.get_character()
        self.label_image_characters2 = UILabel(Rect((550, 50, 400, 400)), text=f'')
        self.image_characters2 = get_front_frame_characters_by_id(DatabaseManager.get_current_character_id())
        self.label_image_characters2.set_image(self.image_weapon1)
        self.label_name_characters2 = UILabel(Rect((750, 500, 100, 50)), text=f'{characters[0][1]}')
        self.button_characters2 = UIButton(Rect((600, 600, 50, 30)), text='выбрать')
        self.label_image_characters3 = UILabel(Rect((550, 50, 400, 400)), text=f'')
        self.image_characters3 = get_front_frame_characters_by_id(DatabaseManager.get_current_character_id())
        self.label_image_characters3.set_image(self.image_weapon1)
        self.label_name_characters3 = UILabel(Rect((750, 500, 100, 50)), text=f'{characters[1][1]}')
        self.button_characters3 = UIButton(Rect((600, 600, 50, 30)), text='выбрать')

    def load_swap_weapons(self) -> None:
        self.exit_setting()
        f = get_weapon_settings
        self.button_back = UIButton(relative_rect=pygame.Rect(2, 2, 50, 30), text='назад',
                                    manager=self.manager, )
        self.label_image_weapon1 = UILabel(Rect((100, 50, 400, 400)), text=f'')
        self.image_weapon1 = get_frame_weapon_by_id(DatabaseManager.get_current_weapon_id())
        self.label_image_weapon1.set_image(self.image_weapon1)
        self.label_name_weapon1 = UILabel(Rect((300, 500, 100, 50)), text=f'{f[4]}')
        self.label_name1 = UILabel(Rect((300, 600, 50, 30)), text='выбрано')
        characters = self.database_manager.get_character()
        self.label_image_weapon2 = UILabel(Rect((550, 50, 400, 400)), text=f'')
        self.image_weapon2 = get_frame_weapon_by_id(DatabaseManager.get_current_weapon_id())
        self.label_image_weapon2.set_image(self.image_weapon1)
        self.label_name_weapon2 = UILabel(Rect((750, 500, 100, 50)), text=f'{characters[0][1]}')
        self.button_weapon2 = UIButton(Rect((600, 600, 50, 30)), text='выбрать')
        self.label_image_weapon3 = UILabel(Rect((550, 50, 400, 400)), text=f'')
        self.image_weapon3 = get_frame_weapon_by_id(DatabaseManager.get_current_weapon_id())
        self.label_image_weapon3.set_image(self.image_weapon1)
        self.label_name_weapon3 = UILabel(Rect((750, 500, 100, 50)), text=f'{characters[1][1]}')
        self.button_weapon3 = UIButton(Rect((600, 600, 50, 30)), text='выбрать')


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
                             WHERE id=?''', (DatabaseManager.get_current_character_id(),)).fetchone()
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
    def get_current_character_id(cls) -> int:
        con, cur = cls._connection_to_database()
        result = cur.execute('''SELECT current_character FROM user''').fetchone()[0]
        con.close()
        return result

    @classmethod
    def get_current_weapon_id(cls) -> int:
        con, cur = cls._connection_to_database()
        result = cur.execute('''SELECT current_weapon FROM user''').fetchone()[0]
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
        print(result)
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
    def shop(cls):
        con, cur = cls._connection_to_database()
        result = cur.execute(f"SELECT * FROM Weapons").fetchall()
        con.close()
        return result

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
