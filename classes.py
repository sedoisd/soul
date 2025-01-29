from pygame import sprite, Rect
import pygame
from other_functions import load_image
from managers import DatabaseManager
from constants import CHARACTERS_FRAME_TIME, ENEMY_FRAME_TIME, SIZE


class Character(sprite.Sprite):
    frame_time = CHARACTERS_FRAME_TIME
    scale = 0.3

    def __init__(self, position: (int, int)):
        super().__init__()
        self.character_id = DatabaseManager.get_current_character_id()
        self.is_alive = True

        self._create_frames()
        self.image = self.front_frames[1]
        self.rect = self.image.get_rect()
        self.index_frame = 0
        self.timedelta = 0
        self.rect.x, self.rect.y = position
        self.mask = pygame.mask.from_surface(self.image)

        self._setup_character_characteristic()
        self.speed *= 100

    def update(self, event=None, timedelta=None, mode: str = None, group_walls: pygame.sprite.Group = None,
               group_enemy: pygame.sprite.Sprite = None) -> None:

        if mode == 'update':
            self.movement(timedelta, group_walls)
        elif mode == 'event':
            pass

    def take_damage(self, damager):
        self.health -= damager.damage
        if self.health <= 0:
            self.is_alive = False

    def movement(self, timedelta, group_walls):
        """Передвижение персонажа и смена фреймов анимации"""
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

    def _setup_character_characteristic(self) -> None:
        """Установка характеристик главного персонажа"""
        self.name, self.health, self.damage, self.speed = DatabaseManager.get_characteristics_character()
        print(self.name, self.health, self.damage, self.speed)  # [LOG]

    def _create_frames(self) -> None:
        """Создание фреймов анимации"""
        atlas = load_image(f'char_{self.character_id}.png', 'characters')
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


class Weapon(sprite.Sprite):
    def __init__(self):
        super().__init__()

    def update(self, *args, **kwargs):
        pass


class Enemy(sprite.Sprite):
    frame_time = ENEMY_FRAME_TIME

    def __init__(self, enemy_id: int, position: (int, int)):
        super().__init__()

        self.enemy_id = enemy_id
        self.is_attacking = False
        self.is_alive = True
        self.full_death_animation = False
        self.index_frame = 0
        self.timedelta = 0
        self.distance_visible = 150

        self._setup_enemy_characteristic()
        self._create_frames()
        self.image = self.stand_frames[0]
        self.current_type_frame = self.stand_frames

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = position

    def update(self, player, timedelta) -> None:
        """Обновление"""
        if self.is_alive:
            self.ai_movement(player)
            self.attack_to_player(player)
        elif self.current_type_frame != self.death_frames:
            self.edit_current_frames('death')
        elif self.index_frame == len(self.death_frames) - 1:
            self.full_death_animation = True
        # Подсчёт временного промежутка и смена кадра анимации
        if self.is_alive or not self.full_death_animation:
            if self.timedelta < self.frame_time:
                self.timedelta += timedelta
            else:
                self.index_frame = (self.index_frame + 1) % len(self.current_type_frame)
                self.timedelta = 0
            # print(self.index_frame, self.current_type_frame) # [LOG]
        self.image = self.current_type_frame[self.index_frame]

    def attack_to_player(self, player: pygame.sprite.Sprite) -> None:
        """Логика и выдача булева значения успеха атаки"""
        if (((self.rect.x - player.rect.x) ** 2 + (self.rect.y - player.rect.y) ** 2) ** 0.5 <
                self.attack_distance):
            player.take_damage(player)

    def ai_movement(self, player) -> None:
        """Логика передвижения монстра относительно главного героя"""
        if not self.is_attacking and ((self.rect.x - player.rect.x) ** 2 + (
                self.rect.y - player.rect.y) ** 2) ** 0.5 < self.distance_visible:
            self.is_attacking = True
        if self.is_attacking:
            if self.rect.x > player.rect.x:
                self.rect.x -= 1
                self.edit_current_frames('left')
            elif self.rect.x < player.rect.x:
                self.rect.x += 1
                self.edit_current_frames('right')
            if self.rect.y > player.rect.y:
                self.rect.y -= 1
            elif self.rect.y < player.rect.y:
                self.rect.y += 1

    def take_damage(self, damager) -> None:
        """Получение урона от игрока"""
        self.health -= damager.damage
        if self.health <= 0:
            self.is_alive = False

    def edit_current_frames(self, mode=None) -> None:
        """Смена текущих фреймов анимации"""
        if mode == 'death' and self.current_type_frame != self.death_frames:
            self.current_type_frame = self.death_frames
            self.index_frame = 0
        elif mode == 'left' and self.current_type_frame != self.left_walking_frames:
            self.current_type_frame = self.left_walking_frames
        elif mode == 'right' and self.current_type_frame != self.right_walking_frames:
            self.current_type_frame = self.right_walking_frames

    def _setup_enemy_characteristic(self) -> None:
        """Установка характеристик монстра"""
        self.scale = 2
        self.name, self.health, self.damage, self.attack_speed, self.attack_distance, self.speed = (
            DatabaseManager.get_characteristics_enemy_by_id(self.enemy_id))
        print(self.name, self.health, self.damage, self.speed)  # [LOG]

    def _create_frames(self) -> None:
        """Создание фреймов анимации"""
        quan_walking, quan_attack, quan_death, quan_stand, quan_kinds = (
            DatabaseManager.get_quantities_frames_enemy_by_id(self.enemy_id))
        atlas = load_image(f'enemy_{self.enemy_id}.png', 'enemies')
        atlas_width = atlas.get_width()
        atlas_height = atlas.get_height()
        frame_width = atlas_width / max(quan_walking, quan_attack, quan_death, quan_stand)
        frame_height = atlas_height / quan_kinds
        self.rect = Rect(0, 0, frame_width, frame_height)
        self.stand_frames = [pygame.transform.rotozoom(
            atlas.subsurface(frame_width * i, 0, frame_width, frame_height), 0, self.scale)
            for i in range(0, quan_stand)]
        self.right_walking_frames = [pygame.transform.rotozoom(
            atlas.subsurface(frame_width * i, frame_height, frame_width, frame_height), 0, self.scale)
            for i in range(0, quan_walking)]
        self.attack_frames = [pygame.transform.rotozoom(
            atlas.subsurface(frame_width * i, frame_height * 2, frame_width, frame_height), 0, self.scale)
            for i in range(0, quan_attack)]
        self.death_frames = [pygame.transform.rotozoom(
            atlas.subsurface(frame_width * i, frame_height * 3, frame_width, frame_height), 0, self.scale)
            for i in range(0, quan_death)]
        self.left_walking_frames = list(map(lambda x: pygame.transform.flip(x, True, False),
                                            self.right_walking_frames))


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


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('cursor.png', 'hud')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, pos: (int, int)):
        self.rect.x, self.rect.y = pos[0] - self.rect.width // 2, pos[1] - self.rect.height // 2
