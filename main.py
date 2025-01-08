import pygame
import pygame_gui
from constants import *
from gui import GuiManager
from characters import Knight


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    fps = 60

    spr = pygame.sprite.Sprite()
    spr.image = pygame.transform.rotozoom(Knight.frames_forward[0], 0, 2)
    spr.rect = spr.image.get_rect()
    spr.rect.y = 30
    spr.rect.x = 30
    k = pygame.sprite.Group()
    k.add(spr)

    running = True
    my_manager = GuiManager()
    my_manager.load_start_menu()

    while running:
        time_delta = clock.tick(fps) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == my_manager.button_exit):
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                print(event.pos)

            my_manager.manager.process_events(event)
        screen.fill((0, 0, 0))
        k.draw(screen)

        my_manager.manager.update(time_delta)
        my_manager.manager.draw_ui(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
