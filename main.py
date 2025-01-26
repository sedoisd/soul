import pygame
import pygame_gui
import pytmx
from constants import *
from managers import GuiManager
from classes import Character, Camera, Enemy


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
        self.group_all_sprites = pygame.sprite.Group()
        self.group_all_tiles = pygame.sprite.Group()
        self.group_player_group = pygame.sprite.Group()
        self.group_enemies_group = pygame.sprite.Group()
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
        while self.running:
            self.time_delta = self.clock.tick(self.fps) / 1000
            for event in pygame.event.get():
                self.event_handling(event)
            self.update()
            self.render()
            pygame.display.flip()
        pygame.quit()

    def event_handling(self, event):
        self.gui_manager.manager.process_events(event)
        if event.type == pygame.QUIT or (
                event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.gui_manager.button_exit):
            self.running = False
        if event.type == pygame.MOUSEBUTTONUP:
            print(event.pos)
            # if self.flag_going_game:
            #     self.player.rect.x, self.player.rect.y = event.pos
        if event.type == pygame_gui.UI_BUTTON_PRESSED:  # Обработка нажатий кнопок GUI
            print(222)
            if event.ui_element == self.gui_manager.button_start:
                self.gui_manager.kill_start_menu()
                print(111)
                self.start_level()
        # if self.flag_going_game:
        #     self.player.update(event=event, timedelta=self.time_delta, mode='event')

    def update(self):
        if self.flag_going_game:
            self.player.update(timedelta=self.time_delta, mode='update', group_walls=self.group_walls_sprites)
            self.group_enemies_group.update(self.player)
            self.camera.update(self.player)
            for sprite in self.group_all_sprites.sprites():
                self.camera.apply(sprite)
        self.gui_manager.manager.update(self.time_delta)

    def render(self):
        self.screen.fill((0, 0, 0))
        if self.flag_going_game:
            self.group_all_tiles.draw(self.screen)
            self.group_player_group.draw(self.screen)
            self.group_enemies_group.draw(self.screen)
        self.gui_manager.manager.draw_ui(self.screen)

    def start_level(self):
        self.flag_going_game = True
        self.map = pytmx.load_pygame('tmx/test_map.tmx')
        self.tile_size = self.map.tilewidth * self.scale_map
        print(self.tile_size)
        layers = [[0, self.group_all_sprites, self.group_all_tiles], [1, self.group_all_sprites, self.group_all_tiles],
                  [2, self.group_all_sprites, self.group_all_tiles, self.group_walls_sprites],
                  [3, [self.group_all_sprites, self.group_all_tiles, self.group_trap]]]
        for i in layers:
            self._init_layer_level(*i)

        for object in self.map.objects:
            # print(object.name) # log
            x_object, y_object = object.x * self.scale_map, object.y * self.scale_map
            sprite_groups = [self.group_all_sprites]
            if object.name == 'Player':
                sprite_groups += [self.group_player_group]
                self.player = Character((x_object, y_object), sprite_groups)
            elif object.name == 'Enemy':
                enemy_id = int(object.properties['enemy_id'])
                sprite_groups += [self.group_enemies_group]
                enemy = Enemy(enemy_id, (x_object, y_object),
                              sprite_groups=sprite_groups)


    def _init_layer_level(self, number_layer, *groups):
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
    # main()
