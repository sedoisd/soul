import pygame
import pygame_gui
from constants import *
from managers import GuiManager
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
        self.clock = pygame.time.Clock()

        # init variables
        self.all_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.running = True
        self.fps = 30
        self.flag_going_game = False
        self.player = None
        self.time_delta = None
        self.background_image = None
        
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
            print(222)
            if event.ui_element == self.gui_manager.button_start:
                self.gui_manager.kill_start_menu()
                print(111)
                self.start_game()
        # if self.flag_going_game:
        #     self.player.update(event=event, timedelta=self.time_delta, mode='event')

    def render(self):
        self.screen.fill((0, 0, 0))
        fon = get_frame_current_background()
        self.screen.blit(fon, (0, 0))
        if self.flag_going_game:
            self.player_group.draw(self.screen)
        self.gui_manager.manager.draw_ui(self.screen)

    def update(self):
        if self.flag_going_game:
            self.player.update(timedelta=self.time_delta, mode='update')
        self.gui_manager.manager.update(self.time_delta) 

    def start_game(self):
        self.flag_going_game = True
        self.player = Character()
        self.player_group.add(self.player)


if __name__ == '__main__':
    game = Game()
    game.run()
    # main()


