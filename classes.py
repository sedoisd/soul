from pygame import sprite, Rect
import pygame
from other_functions import load_image
from managers import DatabaseManager
from constants import ID_CHARACTER, FRAME_TIME, SIZE


class Character(sprite.Sprite):
    def __init__(self, position: (int, int), groups=None):
        super().__init__(groups)
        self.character_id = ID_CHARACTER
        self.frame_time = FRAME_TIME

        self.scale = 0.3
        self._create_frames()
        self.image = self.front_frames[1]
        self.rect = self.image.get_rect()
        self.index_frame = 0
        self.timedelta = 0
        self.rect.x, self.rect.y = position
        self.mask = pygame.mask.from_surface(self.image)

        self._setup_character_characteristic()
        self.speed *= 150

    def _setup_character_characteristic(self) -> None:
        self.name, self.health, self.damage, self.speed = DatabaseManager.get_characteristics_character()
        print(self.name, self.health, self.damage, self.speed)

    def _create_frames(self) -> None:
        atlas = load_image(f'char_{ID_CHARACTER}.png', 'characters')
        atlas_width = atlas.get_width()
        atlas_height = atlas.get_height()
        frame_width = atlas_width / 3
        frame_height = atlas_height / 4
        self.rect = Rect(0, 0, frame_width, frame_height)
        self.front_frames = [pygame.transform.rotozoom(
            atlas.subsurface(frame_width * i, frame_height * 3, frame_width, frame_height), 0, self.scale)
            for i in range(0, 3)]
        self.back_frames = [pygame.transform.rotozoom(
            atlas.subsurface(frame_width * i, 0, frame_width, frame_height), 0, self.scale)
            for i in range(0, 3)]
        self.left_frames = [pygame.transform.rotozoom(
            atlas.subsurface(frame_width * i, frame_height * 1 + 1, frame_width, frame_height), 0, self.scale)
            for i in range(0, 3)]
        self.right_frames = [pygame.transform.rotozoom(
            atlas.subsurface(frame_width * i, frame_height * 2, frame_width, frame_height), 0, self.scale)
            for i in range(0, 3)]

    def update(self, event=None, timedelta=None, mode: str = None, group_walls: pygame.sprite.Group = None) -> None:
        if mode == 'update':
            x, y = self.rect.x, self.rect.y
            delta_distance = self.speed * self.timedelta
            if pygame.key.get_pressed()[pygame.K_w]:
                self.image = self.front_frames[self.index_frame]
                self.rect.y -= delta_distance
            if pygame.key.get_pressed()[pygame.K_s]:
                self.image = self.back_frames[self.index_frame]
                self.rect.y += delta_distance
            for tile in group_walls:
                if pygame.sprite.collide_mask(self, tile):
                    self.rect.y = y
            if pygame.key.get_pressed()[pygame.K_a]:
                self.image = self.left_frames[self.index_frame]
                self.rect.x -= delta_distance
            if pygame.key.get_pressed()[pygame.K_d]:
                self.image = self.right_frames[self.index_frame]
                self.rect.x += delta_distance
            for tile in group_walls:
                if pygame.sprite.collide_mask(self, tile):
                    self.rect.x = x
            if self.timedelta < self.frame_time:
                self.timedelta += timedelta
            else:
                self.index_frame = (self.index_frame + 1) % 3
                self.timedelta = 0

        elif mode == 'event':
            pass


class Weapon(sprite.Sprite):
    def __init__(self):
        super().__init__()

    def update(self, *args, **kwargs):
        pass


class Enemy(sprite.Sprite):
    def __init__(self, enemy_id):
        super().__init__()
        self.enemy_id = enemy_id
        self.frame_time = FRAME_TIME

        self._create_frames()
        self._setup_enemy_characteristic()

    def _setup_enemy_characteristic(self) -> None:
        self.name, self.health, self.damage, self.speed = DatabaseManager.get_characteristics_enemy_by_id(self.enemy_id)
        print(self.name, self.health, self.damage, self.speed)

    def _create_frames(self):
        quan_walking, quan_attack, quan_death, quan_kinds = (
            DatabaseManager.get_quantities_frames_enemy_by_id(self.enemy_id))
        atlas = load_image(f'enemy_{self.enemy_id}.png', 'enemies')
        atlas_width = atlas.get_width()
        atlas_height = atlas.get_height()
        self.walking_frames = []
        self.attack_frames = []
        self.death_frames = []

    def update(self, *args, **kwargs):
        pass


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = SIZE[0] // 2 - (target.rect.x + target.rect.w // 2)
        self.dy = SIZE[1] // 2 - (target.rect.y + target.rect.h // 2)
