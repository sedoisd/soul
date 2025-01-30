from pygame import Rect
import pygame
import pygame_gui
from pygame_gui.elements import *
from constants import SIZE, FILENAME_DATABASE
from other_functions import get_frame_weapon_by_id, get_front_frame_characters_by_id
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
        self.image_character = get_front_frame_characters_by_id(DatabaseManager.get_current_character_id())
        # self.image_character = ц(self.image_character, 0, 0.2)
        self.label_image_character.set_image(self.image_character)
        self.label_name_character = UILabel(Rect((690, 310, 100, 30)), text='Рыцарь')

        # Weapon menu
        self.label_image_weapon = UILabel(Rect((350, 60, 150, 100)), text='')
        self.image_weapon = get_frame_weapon_by_id(DatabaseManager.get_current_weapon_and_mod_ids()[0])
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
    def get_characteristics_enemy_by_id(cls, enemy_id: int) -> tuple[str, int, int, float, int, int]:
        con, cur = cls._connection_to_database()
        result = cur.execute('''SELECT name, health, damage, scale, attack_distance, speed FROM enemies
                             WHERE id=?''', (enemy_id,)).fetchone()
        # print(result) # [LOG]
        con.close()
        return result

    @classmethod
    def get_quantities_frames_enemy_by_id(cls, enemy_id: int = None) -> tuple[int, int, int, int, int]:
        con, cur = cls._connection_to_database()
        result = cur.execute('''SELECT quan_walking_frames, quan_attack_frames, 
                             quan_death_frames, quan_stand_frame, quan_kinds_frames FROM enemies
                             WHERE ID=?''', (enemy_id,)).fetchone()
        # print(result) # [LOG]
        con.close()
        return result

    @classmethod
    def get_current_character_id(cls) -> int:
        con, cur = cls._connection_to_database()
        result = cur.execute('''SELECT current_character FROM user''').fetchone()[0]
        # print(result) # [LOG]
        con.close()
        return result

    @classmethod
    def get_current_weapon_and_mod_ids(cls) -> (int, int):
        con, cur = cls._connection_to_database()
        result = cur.execute('''SELECT current_weapon, current_weapon_mod FROM user''').fetchone()
        # print(result) # [LOG]
        con.close()
        return result


class SpriteGroupManager:
    def __init__(self):

        self.all_gameplay = pygame.sprite.Group()
        self.movable_for_gameplay = pygame.sprite.Group()
        self.player = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.trap = pygame.sprite.Group()
        self.hud = pygame.sprite.Group()
        self.hud_main_sprite = None

        self.all_tiles = pygame.sprite.Group()
        self.cursor = pygame.sprite.Group()

    def update(self, is_going_game: bool, timedelta: float) -> None:
        if is_going_game:
            self.player.update(timedelta=timedelta, mode='update', group_walls=self.walls)
            self.enemies.update(*self.player.sprites(), timedelta)
            self.hud_main_sprite.update(*self.player.sprites()[0].get_value_for_hud())
            self.trap.update(any(map(lambda x: x.flag_angry, self.enemies)))

    def draw(self, screen, is_going_game: bool) -> None:
        if is_going_game:
            self.all_tiles.draw(screen)
            self.trap.draw(screen)
            self.player.draw(screen)
            self.enemies.draw(screen)
            self.hud.draw(screen)
            self.cursor.draw(screen)

    def add_hud(self, sprite: pygame.sprite.Sprite):
        self.hud_main_sprite = sprite
        self.hud.add(sprite)
        for subsprite in sprite.get_sprites_status_bar():
            self.hud.add(subsprite)

    def _add_gameplay(self, sprite):
        self.all_gameplay.add(sprite)
        self.movable_for_gameplay.add(sprite)

    def get_movable_sprites(self) -> list:
        return self.movable_for_gameplay.sprites()

    def add_tile_sprite_by_id_layer(self, sprite: pygame.sprite.Sprite, id_layer: int) -> None:
        groups = [self.all_gameplay, self.movable_for_gameplay, self.all_tiles]
        # if id_layer in (0, 1):
        #     groups.extend(self.all_tiles)
        if id_layer == 2:
            groups.append(self.walls)
        elif id_layer == 3:
            groups.append(self.trap)

        for group in groups:
            group.add(sprite)

    def add_player(self, sprite: pygame.sprite.Sprite) -> None:
        self._add_gameplay(sprite)
        self.player.add(sprite)

    def add_enemy(self, sprite: pygame.sprite.Sprite) -> None:
        self._add_gameplay(sprite)
        self.enemies.add(sprite)

    def add_cursor(self, sprite: pygame.sprite.Sprite) -> None:
        self.cursor.add(sprite)

    def kill_gameplay_sprites(self) -> None:
        for sprite in self.all_gameplay:
            sprite.kill()
        for sprite in self.hud:
            sprite.kill()
