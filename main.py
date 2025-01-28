import pygame
import pygame_gui
from constants import *
from managers import GuiManager, DatabaseManager
from initialization_classes import Character
from other_functions import get_frame_current_background

# import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        self.size = self.screen.get_size()

        # init classes
        self.gui_manager = GuiManager()
        self.database_manager = DatabaseManager()
        self.progress_bar1, self.progress_bar2 = self.database_manager.get_characteristics_settings()
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
        self.player = None
        self.time_delta = None
        self.music_menu = pygame.mixer.music.load("sound/music/menu.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(self.progress_bar1 / 100)
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
            if event.ui_element == self.gui_manager.button_start:
                self.gui_manager.kill_start_menu()
                self.start_game1()
                self.flag_going_game1 = True
            elif event.ui_element == self.gui_manager.button_shop:
                self.gui_manager.kill_start_menu()
                self.flag_going_shop = True
                self.gui_manager._load_shop()
            elif event.ui_element == self.gui_manager.button_setting:
                self.gui_manager.kill_start_menu()
                self.flag_going_setting = True
                self.gui_manager._load_setting()
            elif event.ui_element == self.gui_manager.button_back:
                self.gui_manager.load_start_menu()
                self.gui_manager.button_back.kill()
                if self.flag_going_game1:
                    self.gui_manager.label_image_character.kill()
                    self.gui_manager.label_image_weapon.kill()
                    self.gui_manager.label_name_character.kill()
                    self.gui_manager.label_name_weapon.kill()
                if self.flag_going_setting:
                    self.gui_manager.button_fihki.kill()
                    self.gui_manager.button_sound.kill()
                    self.gui_manager.progress_bar1_f.kill()
                    self.gui_manager.progress_bar2_f.kill()
                    self.gui_manager.button_save.kill()
                    self.gui_manager.button_minys1.kill()
                    self.gui_manager.button_minys2.kill()
                    self.gui_manager.button_plus1.kill()
                    self.gui_manager.button_plus2.kill()
                    self.progress_bar1_f = self.progress_bar1
                    self.progress_bar2_f = self.progress_bar2
                    pygame.mixer.music.set_volume(self.progress_bar1 / 100)
                self.flag_going_shop = False
                self.flag_going_setting = False
                self.flag_going_game1 = False
            elif event.ui_element == self.gui_manager.button_minys1: # Обработка настроек
                if self.progress_bar1_f > 0:
                    self.gui_manager.progress_bar1_f.set_current_progress(self.progress_bar1_f - 5)
                    self.progress_bar1_f -= 5
                    pygame.mixer.music.set_volume(self.progress_bar1_f / 100)
            elif event.ui_element == self.gui_manager.button_minys2:
                if self.progress_bar2_f > 0:
                    self.gui_manager.progress_bar2_f.set_current_progress(self.progress_bar2_f - 5)
                    self.progress_bar2_f -= 5
            elif event.ui_element == self.gui_manager.button_plus1:
                if self.progress_bar1_f < 100:
                    self.gui_manager.progress_bar1_f.set_current_progress(self.progress_bar1_f + 5)
                    self.progress_bar1_f += 5
                    pygame.mixer.music.set_volume(self.progress_bar1_f / 100)
            elif event.ui_element == self.gui_manager.button_plus2:
                if self.progress_bar2_f < 100:
                    self.gui_manager.progress_bar2_f.set_current_progress(self.progress_bar2_f + 5)
                    self.progress_bar2_f += 5
            elif event.ui_element == self.gui_manager.button_save:
                self.progress_bar1 = self.progress_bar1_f
                self.progress_bar2 = self.progress_bar2_f
                pygame.mixer.music.set_volume(self.progress_bar1 / 100)
                self.database_manager.update_setting(self.progress_bar1, self.progress_bar2)

                

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