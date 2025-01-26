import pygame
import pygame_gui
import pytmx
from constants import *
from managers import GuiManager, DatabaseManager
from classes import Character, Camera, Enemy
from other_functions import load_image


# import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)

        # init classes
        self.gui_manager = GuiManager()
        self.clock = pygame.time.Clock()
        self.camera = Camera()

        # init variables
        self.group_hud = pygame.sprite.Group()
        self.group_all_game_spites = pygame.sprite.Group()
        self.group_all_tiles = pygame.sprite.Group()
        self.group_player = pygame.sprite.Group()
        self.group_enemies = pygame.sprite.Group()
        self.group_walls_sprites = pygame.sprite.Group()
        self.group_trap = pygame.sprite.Group()
        self.fps = 60
        self.scale_map = SCALE_MAP
        self.running = True
        self.flag_going_game = False
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
        if event.type == pygame.MOUSEBUTTONUP:
            print(event.pos)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:  # Обработка нажатий кнопок GUI
            print(222)  # log
            if event.ui_element == self.gui_manager.button_start:
                self.gui_manager.kill_start_menu()
                print(111)  # log
                self._start_level()

    def _update(self):
        """Обновление"""
        if self.flag_going_game:
            self.player.update(timedelta=self.time_delta, mode='update', group_walls=self.group_walls_sprites)
            self.group_enemies.update(self.player)
            self.camera.update(self.player)
            for sprite in self.group_all_game_spites.sprites():
                self.camera.apply(sprite)
        self.gui_manager.manager.update(self.time_delta)

    def _render(self):
        """Отображение программы-игры"""
        self.screen.fill((0, 0, 0))
        if self.flag_going_game:
            self.group_all_tiles.draw(self.screen)
            self.group_player.draw(self.screen)
            self.group_enemies.draw(self.screen)
            self.group_hud.draw(self.screen)
            # pygame.draw.rect(self.screen, pygame.Color('#49423d'), (150, 580, 600, 120))
        self.gui_manager.manager.draw_ui(self.screen)

    def _start_level(self):
        """Создание уровня"""
        self.flag_going_game = True
        self._create_hud()
        self.map = pytmx.load_pygame('tmx/test_map.tmx')
        self.tile_size = self.map.tilewidth * self.scale_map
        # print(self.tile_size) # log
        layers = [[0, self.group_all_game_spites, self.group_all_tiles],
                  [1, self.group_all_game_spites, self.group_all_tiles],
                  [2, self.group_all_game_spites, self.group_all_tiles, self.group_walls_sprites],
                  [3, [self.group_all_game_spites, self.group_all_tiles, self.group_trap]]]
        for i in layers:
            self._init_layer_level(*i)

        for object_livestock in self.map.objects:
            # print(object.name) # log
            x_object, y_object = object_livestock.x * self.scale_map, object_livestock.y * self.scale_map
            sprite_groups = [self.group_all_game_spites]
            if object_livestock.name == 'Player':
                sprite_groups += [self.group_player]
                self.player = Character((x_object, y_object), sprite_groups)
            elif object_livestock.name == 'Enemy':
                enemy_id = int(object_livestock.properties['enemy_id'])
                sprite_groups += [self.group_enemies]
                enemy = Enemy(enemy_id, (x_object, y_object),
                              sprite_groups=sprite_groups)

    def _create_hud(self):
        self.gen_hud = pygame.sprite.Sprite(self.group_hud)
        self.gen_hud.image = pygame.transform.scale(load_image('hud.png', 'hud'), (600, 120))
        self.gen_hud.rect = self.gen_hud.image.get_rect()
        self.gen_hud.rect.x, self.gen_hud.rect.y = 150, 580

    def _init_layer_level(self, number_layer, *groups):
        """Создание слоёв карты tmx формата"""
        for y in range(self.map.height):
            for x in range(self.map.width):
                image = self.map.get_tile_image(x, y, number_layer)
                if image:
                    tile_sprite = pygame.sprite.Sprite(*groups)
                    tile_sprite.image = pygame.transform.rotozoom(image, 0, self.scale_map)
                    tile_sprite.rect = tile_sprite.image.get_rect()
                    tile_sprite.rect.x, tile_sprite.rect.y = (
                        x * self.tile_size, y * self.tile_size)
                    tile_sprite.mask = pygame.mask.from_surface(tile_sprite.image)


if __name__ == '__main__':
    game = Game()
    game.run()
