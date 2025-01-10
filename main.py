import pygame
import pygame_gui
from constants import *
from managers import GuiManager, GameManager
from characters import Knight
# from weapons import


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    fps = 60



    running = True
    gui_manager = GuiManager()
    gui_manager.load_start_menu()
    game_manager = GameManager()

    while running:
        time_delta = clock.tick(fps) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == gui_manager.button_exit):
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                print(event.pos)

            gui_manager.manager.process_events(event)
        screen.fill((0, 0, 0))

        gui_manager.manager.update(time_delta)
        gui_manager.manager.draw_ui(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
