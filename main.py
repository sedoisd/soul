import pygame
import pygame_gui
import pytmx
from constants import *
from managers import GuiManager, SpriteGroupManager
from classes import Character, Camera, Enemy, Cursor


# import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)

        # init classes
        self.gui_manager = GuiManager()
        self.sprite_group_manager = SpriteGroupManager()
        self.clock = pygame.time.Clock()
        self.camera = Camera()
        self.cursor = Cursor()
        self.sprite_group_manager.add_cursor_sprite(self.cursor)

        # init variables
        self.fps = 60
        self.scale_map = SCALE_MAP
        self.running = True
        self.is_going_game = False
        self.flag_create_game_cursor = False
        self.player = None
        self.time_delta = None

        self.gui_manager.load_start_menu()

    def run(self):
        """Основной цикл программы"""
        while self.running:
            self.time_delta = self.clock.tick(self.fps) / 1000
            for event in pygame.event.get():
                self._event_handling(event)
            self._update()
            self._render()
            pygame.display.flip()
        pygame.quit()

    def _event_handling(self, event):
        """Обработка событий"""
        self.gui_manager.manager.process_events(event)
        if event.type == pygame.QUIT or (
                event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.gui_manager.button_exit):
            self.running = False
        if event.type == pygame.MOUSEMOTION:
            if self.flag_create_game_cursor:
                self.cursor.update(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_going_game:
                for enemy in self.sprite_group_manager.enemies.sprites():
                    # print('iter')
                    if pygame.sprite.collide_mask(self.cursor, enemy):
                        enemy.take_damage(self.player)
                        print(enemy.health)
                        print(111)

            print(event.pos)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:  # Обработка нажатий кнопок GUI
            print(222)  # log
            if event.ui_element == self.gui_manager.button_start:
                self.gui_manager.kill_start_menu()
                print(111)  # log
                self._start_level()

    def _update(self):
        """Обновление"""
        self.sprite_group_manager.update(is_going_game=self.is_going_game, timedelta=self.time_delta)
        if self.is_going_game:
            self.camera.update(self.player)
            for sprite in self.sprite_group_manager.get_all_gameplay_sprites():
                self.camera.apply(sprite)
        self.gui_manager.manager.update(self.time_delta)

    def _render(self):
        """Отображение программы-игры"""
        self.screen.fill((0, 0, 0))
        if self.is_going_game:
            self.sprite_group_manager.draw(self.screen, self.is_going_game)
        self.gui_manager.manager.draw_ui(self.screen)

    def _start_level(self):
        """Создание уровня"""

        self.flag_create_game_cursor = True
        pygame.mouse.set_visible(False)

        self.is_going_game = True
        # self._create_hud()
        self.map = pytmx.load_pygame('tmx/test_map.tmx')
        self.tile_size = self.map.tilewidth * self.scale_map
        # print(self.tile_size) # log
        for i in range(4):
            self._init_layer_level(i)

        for object_livestock in self.map.objects:
            # print(object.name) # log
            x_object, y_object = object_livestock.x * self.scale_map, object_livestock.y * self.scale_map
            if object_livestock.name == 'Player':
                self.player = Character((x_object, y_object))
                self.sprite_group_manager.add_player_sprite(self.player)
            elif object_livestock.name == 'Enemy':
                enemy_id = int(object_livestock.properties['enemy_id'])
                enemy = Enemy(enemy_id, (x_object, y_object))
                self.sprite_group_manager.add_enemy_sprite(enemy)

    def _init_layer_level(self, id_layer):
        """Создание слоя по id. Слои из карты tmx формата"""
        for y in range(self.map.height):
            for x in range(self.map.width):
                image = self.map.get_tile_image(x, y, id_layer)
                if image:
                    tile_sprite = pygame.sprite.Sprite()
                    tile_sprite.image = pygame.transform.rotozoom(image, 0, self.scale_map)
                    tile_sprite.rect = tile_sprite.image.get_rect()
                    tile_sprite.rect.x, tile_sprite.rect.y = (
                        x * self.tile_size, y * self.tile_size)
                    tile_sprite.mask = pygame.mask.from_surface(tile_sprite.image)
                    self.sprite_group_manager.add_tile_sprite_by_id_layer(tile_sprite, id_layer)

    def _create_hud(self):
        # self.gen_hud = pygame.sprite.Sprite(self.group_hud)
        # self.gen_hud.image = pygame.transform.scale(load_image('hud.png', 'hud'), (600, 120))
        # self.gen_hud.rect = self.gen_hud.image.get_rect()
        # self.gen_hud.rect.x, self.gen_hud.rect.y = 150, 580
        pass


if __name__ == '__main__':
    game = Game()
    game.run()
