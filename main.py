import pygame
import pygame_gui
from constants import *
from managers import GuiManager, DatabaseManager
from initialization_classes import Character
from other_functions import get_frame_current_background, get_weapon_settings, update_setting, buy

# import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        self.size = self.screen.get_size()

        # init classes
        self.gui_manager = GuiManager()
        self.database_manager = DatabaseManager()
        self.money, self.progress_bar1, self.progress_bar2, self.characters, self.weapon = get_weapon_settings()
        self.money, self.progress_bar1, self.progress_bar2 = int(self.money), int(self.progress_bar1), int(self.progress_bar2)
        self.progress_bar1_f, self.progress_bar2_f = self.progress_bar1, self.progress_bar2
        self.clock = pygame.time.Clock()

        # init variables
        self.all_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.running = True
        self.fps = 30
        self.flag_going_game = False
        self.flag_going_shop = False
        self.flag_going_setting = False
        self.flag_going_game1 = False
        self.place = 'menu'
        self.player = None
        self.time_delta = None
        self.music_menu = pygame.mixer.music.load("sound/music/menu.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(self.progress_bar1 / 100)
        self.sound_open = pygame.mixer.Sound("sound/effects/sound_button.mp3")
        self.sound_open.set_volume(self.progress_bar2 / 100)
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
            if self.flag_going_game:
                self.player.rect.x, self.player.rect.y = event.pos
            if event.type == pygame_gui.UI_BUTTON_PRESSED:  # Обработка нажатий кнопок GUI
                self.sound_open.play()
                if self.place == "menu": # Обработка меню
                    if event.ui_element == self.gui_manager.button_start:
                        self.gui_manager.kill_start_menu()
                        self.start_game1()
                        self.flag_going_game1 = True
                        self.place = 'start1'
                    elif event.ui_element == self.gui_manager.button_shop:
                        self.gui_manager.kill_start_menu()
                        self.flag_going_shop = True
                        self.gui_manager._load_shop()
                        self.place = 'shop'
                    elif event.ui_element == self.gui_manager.button_setting:
                        self.gui_manager.kill_start_menu()
                        self.flag_going_setting = True
                        self.gui_manager._load_setting()
                        self.place = 'setting'
                    elif event.ui_element == self.gui_manager.button_back:
                        self.gui_manager.load_start_menu()
                        self.gui_manager.button_back.kill()
                        if self.place == 'game1':
                            self.gui_manager.exit_game1()
                            self.flag_going_game1 = False
                        if self.place == 'setting':
                            self.gui_manager.exit_setting()
                            self.progress_bar1_f = self.progress_bar1
                            self.progress_bar2_f = self.progress_bar2
                            pygame.mixer.music.set_volume(self.progress_bar1 / 100)
                            self.sound_open.set_volume(self.progress_bar2 / 100)
                            self.flag_going_setting = False
                        if self.place == 'shop':
                            self.gui_manager.exit_shop()
                            self.flag_going_shop = False
                        self.place = 'menu'
                elif self.place == "setting": # Обработка настроек
                    if event.ui_element == self.gui_manager.button_minys1: 
                        if self.progress_bar1_f > 0:
                            self.gui_manager.progress_bar1_f.set_current_progress(self.progress_bar1_f - 5)
                            self.progress_bar1_f -= 5
                            pygame.mixer.music.set_volume(self.progress_bar1_f / 100)
                    elif event.ui_element == self.gui_manager.button_minys2:
                        if self.progress_bar2_f > 0:
                            self.gui_manager.progress_bar2_f.set_current_progress(self.progress_bar2_f - 5)
                            self.progress_bar2_f -= 5
                            self.sound_open.set_volume(self.progress_bar2_f / 100)
                    elif event.ui_element == self.gui_manager.button_plus1:
                        if self.progress_bar1_f < 100:
                            self.gui_manager.progress_bar1_f.set_current_progress(self.progress_bar1_f + 5)
                            self.progress_bar1_f += 5
                            pygame.mixer.music.set_volume(self.progress_bar1_f / 100)
                    elif event.ui_element == self.gui_manager.button_plus2:
                        if self.progress_bar2_f < 100:
                            self.gui_manager.progress_bar2_f.set_current_progress(self.progress_bar2_f + 5)
                            self.progress_bar2_f += 5
                            self.sound_open.set_volume(self.progress_bar2 / 100)
                    elif event.ui_element == self.gui_manager.button_save:
                        self.progress_bar1 = self.progress_bar1_f
                        self.progress_bar2 = self.progress_bar2_f
                        pygame.mixer.music.set_volume(self.progress_bar1 / 100)
                        self.sound_open.set_volume(self.progress_bar2 / 100)
                        update_setting(self.progress_bar1, self.progress_bar2)
                elif self.place == "shop": # Обработка магазина
                    if event.ui_element == self.gui_manager.button_buy:
                        self.database_manager.update_inventory(self.gui_manager.name)
                        self.gui_manager.update_shop()
                elif self.place == 'game1': # Обработка предигравого окна
                    if event.ui_element == self.gui_manager.button_weapon_swap:
                        self.gui_manager.load_swap_weapons()
                        self.place == 'weapon_swap'
                    elif event.ui_element == self.gui_manager.button_characters_swap:
                        self.gui_manager.load_swap_characters()
                        self.place == "characters_swap"
                elif self.place == "weapon_swap":
                    if event.ui_element == self.gui_manager.button_weapon2:
                        pass
                    if event.ui_element == self.gui_manager.button_weapon3:
                        pass
                elif self.place == "characters_swap":
                    if event.ui_element == self.gui_manager.button_characters2:
                        pass
                    if event.ui_element == self.gui_manager.button_characters3:
                        pass
        if self.flag_going_game:
            self.player.update(event=event, timedelta=self.time_delta, mode='event')

    def render(self):
        if self.flag_going_shop:
            fon = get_frame_current_background(1)
            self.screen.blit(fon, (0, 0))
        elif self.flag_going_setting:
            fon = get_frame_current_background(2)
            self.screen.blit(fon, (0, 0))
        elif self.flag_going_game1:
            fon = get_frame_current_background(3)
            self.screen.blit(fon, (0, 0))
        else:
            fon = get_frame_current_background(0)
            self.screen.blit(fon, (0, 0))
        if self.flag_going_game:
            self.player_group.draw(self.screen)
        self.gui_manager.manager.draw_ui(self.screen)

    def update(self) -> None:
        if self.flag_going_game:
            self.player.update(timedelta=self.time_delta, mode='update')
        self.gui_manager.manager.update(self.time_delta)
    
    def start_game1(self) -> None:
        self.gui_manager.load_start_game1()

    def start_game2(self):
        self.flag_going_game = True
        self.player = Character()
        self.player_group.add(self.player)

if __name__ == '__main__':
    game = Game()
    game.run()
    # main()