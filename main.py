import pygame
import pygame_gui
import pytmx
from constants import *
from managers import GuiManager, SpriteGroupManager
from classes import Character, Camera, Enemy, Cursor, Hud, Trap, Portal


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

        # init variables
        self.fps = 60
        self.scale_map = SCALE_MAP
        self.running = True
        self.is_going_game = False
        self.flag_create_game_cursor = False
        self.player = None
        self.time_delta = None

        # init counting variables
        self.max_enemy = 0
        self.killed_enemy = 0

        # function exe
        self.sprite_group_manager.add_cursor(self.cursor)
        self.gui_manager.load_start_menu()

    def run(self):
        """Основной цикл программы"""
        while self.running:
            self.time_delta = self.clock.tick(self.fps) / 1000

            if self.is_going_game and not self.player.flag_alive:
                self._completion_level()

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
            print(event.pos)
            if self.is_going_game:
                for enemy in self.sprite_group_manager.enemies.sprites():
                    # print('iter') # [LOG]
                    if pygame.sprite.collide_mask(self.cursor, enemy):
                        if enemy.take_damage(self.player):
                            self.killed_enemy += 1
                        # print(enemy.health) # [LOG]
                        # print(111) # [LOG]

        if event.type == pygame_gui.UI_BUTTON_PRESSED:  # Обработка нажатий кнопок GUI
            # print(222)  # [LOG]
            if event.ui_element == self.gui_manager.button_start:
                self.gui_manager.kill_start_menu()
                # print(111)  # [LOG]
                self._start_level()

    def _update(self):
        """Отправка обновлений"""
        self.sprite_group_manager.update(is_going_game=self.is_going_game, timedelta=self.time_delta)
        if self.is_going_game:
            self.camera.update(self.player)
            for sprite in self.sprite_group_manager.get_movable_sprites():
                self.camera.apply(sprite)
            portal = self.sprite_group_manager.get_portal_sprite()
            if pygame.sprite.collide_mask(self.player, portal):
                self._completion_level()
        self.gui_manager.manager.update(self.time_delta)

    def _render(self):
        """Отображение программы-игры"""
        color = (122, 122, 122)
        self.screen.fill(color)
        if self.is_going_game:
            self.sprite_group_manager.draw(self.screen, self.is_going_game)
        self.gui_manager.manager.draw_ui(self.screen)

    def _completion_level(self):
        print(self.max_enemy, self.killed_enemy)
        self.max_enemy = 0
        self.killed_enemy = 0
        self.is_going_game = False
        pygame.mouse.set_visible(True)
        self.sprite_group_manager.kill_gameplay_sprites()

        self.gui_manager.load_start_menu()

    def _start_level(self):
        """Создание уровня"""
        self.flag_create_game_cursor = True
        pygame.mouse.set_visible(False)

        self.is_going_game = True
        hud = Hud()
        self.sprite_group_manager.add_hud(hud)
        self.map = pytmx.load_pygame('tmx/test_map.tmx')
        self.tile_size = self.map.tilewidth * self.scale_map
        # print(self.tile_size) # [LOG]
        for i in range(4):
            self._init_layer_level(i)
        for game_object in self.map.objects:
            # print(object.name) # [LOG]
            x_object, y_object = game_object.x * self.scale_map, game_object.y * self.scale_map
            if game_object.name == 'Player':
                self.player = Character((x_object, y_object))
                self.sprite_group_manager.add_player(self.player)
            elif game_object.name == 'Portal':
                self.portal = Portal((x_object, y_object))
                self.sprite_group_manager.add_portal(self.portal)
            elif game_object.name == 'Enemy':
                self.max_enemy += 1
                enemy_id = int(game_object.properties['enemy_id'])
                enemy = Enemy(enemy_id, (x_object, y_object))
                self.sprite_group_manager.add_enemy(enemy)

    def _init_layer_level(self, id_layer: int):
        """Создание слоя по id. Слои из карты tmx формата"""
        for y in range(self.map.height):
            for x in range(self.map.width):
                flag_trap = False
                if id_layer == 3:
                    tile_properties = self.map.get_tile_properties(x, y, id_layer)
                    if tile_properties and tile_properties['type'] == 'trap':
                        trap = Trap(x * self.tile_size, y * self.tile_size)
                        self.sprite_group_manager.add_tile_sprite_by_id_layer(trap, id_layer)
                        flag_trap = True
                image = self.map.get_tile_image(x, y, id_layer)
                if not flag_trap and image:
                    tile_sprite = pygame.sprite.Sprite()
                    tile_sprite.image = pygame.transform.rotozoom(image, 0, self.scale_map)
                    tile_sprite.rect = tile_sprite.image.get_rect()
                    tile_sprite.rect.x, tile_sprite.rect.y = (
                        x * self.tile_size, y * self.tile_size)
                    tile_sprite.mask = pygame.mask.from_surface(tile_sprite.image)
                    self.sprite_group_manager.add_tile_sprite_by_id_layer(tile_sprite, id_layer)


if __name__ == '__main__':
    game = Game()
    game.run()
