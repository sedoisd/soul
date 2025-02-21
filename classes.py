from pygame import sprite, Rect
import pygame

from other_functions import load_image
from managers import DatabaseManager
from constants import CHARACTERS_FRAME_TIME, ENEMY_FRAME_TIME, SIZE, SCALE_HUD, SCALE_MAP


class Character(sprite.Sprite):
    frame_time = CHARACTERS_FRAME_TIME
    scale = 0.3

    def __init__(self, position: (int, int)):
        super().__init__()

        self.character_id = DatabaseManager.get_current_id_by_group('characters')
        self.flag_alive = True

        self._create_frames()
        self.image = self.front_frames[1]
        self.rect = self.image.get_rect()
        self.index_frame = 0
        self.timedelta = 0
        self.timedelta_for_trap = 0
        self.rect.x, self.rect.y = position
        self.mask = pygame.mask.from_surface(self.image)

        self._setup_character_characteristic()
        self.speed *= 100
        self.weapon = Weapon(self)

    def update(self, timedelta=None, mode: str = None, group_walls=None,
               group_enemy=None, group_trap=None):
        if self.flag_alive:
            if mode == 'update':
                self.movement(timedelta, group_walls, group_trap)
                self.take_damage_by_trap(timedelta, group_trap)
            elif mode == 'event':
                pass

    def get_value_for_hud(self) -> tuple[float, float]:
        health_percents = self.health / self.max_health
        armor_percents = self.armor / self.max_armor
        return health_percents, armor_percents

    def take_damage(self, value):
        """Получение урона от монстра   """
        if self.armor > 0:
            self.armor -= value
            if self.armor < 0:
                self.armor = 0
        else:
            self.health -= value
        if self.health <= 0:
            self.flag_alive = False

    def take_damage_by_trap(self, timedelta, traps):
        if self.timedelta_for_trap < 0.5:
            self.timedelta_for_trap += timedelta
        else:
            self.timedelta_for_trap = 0
            for trap in traps.sprites():
                if trap.enable and pygame.sprite.collide_mask(self, trap):
                    if self.health < 2:
                        self.flag_alive = False
                    else:
                        self.health = 1
                    break

    def movement(self, timedelta: float, group_walls: pygame.sprite.Group, group_trap):
        """Передвижение персонажа и смена фреймов анимации"""
        x, y = self.rect.x, self.rect.y
        delta_distance = self.speed * self.timedelta
        for trap in group_trap:
            if trap.enable and pygame.sprite.collide_mask(self, trap):
                delta_distance *= 0.2
                break
        if pygame.key.get_pressed()[pygame.K_w]:
            self.image = self.back_frames[self.index_frame]
            self.rect.y -= delta_distance
        if pygame.key.get_pressed()[pygame.K_s]:
            self.image = self.front_frames[self.index_frame]
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

    def _setup_character_characteristic(self):
        """Установка характеристик главного персонажа"""
        self.name, self.health, self.damage, self.speed, self.armor = DatabaseManager.get_characteristics_character()
        self.max_health = self.health
        self.max_armor = self.armor

    def _create_frames(self):
        """Создание фреймов анимации"""
        atlas = load_image(f'char_{self.character_id}.png', 'characters')
        atlas_width = atlas.get_width()
        atlas_height = atlas.get_height()
        frame_width = atlas_width / 3
        frame_height = atlas_height / 4
        self.rect = Rect(0, 0, frame_width, frame_height)
        self.front_frames = [pygame.transform.rotozoom(
            atlas.subsurface(frame_width * i, frame_height * 0, frame_width, frame_height), 0, self.scale)
            for i in range(0, 3)]
        self.back_frames = [pygame.transform.rotozoom(
            atlas.subsurface(frame_width * i, frame_height * 3, frame_width, frame_height), 0, self.scale)
            for i in range(0, 3)]
        self.left_frames = [pygame.transform.rotozoom(
            atlas.subsurface(frame_width * i, frame_height * 1 + 1, frame_width, frame_height), 0, self.scale)
            for i in range(0, 3)]
        self.right_frames = [pygame.transform.rotozoom(
            atlas.subsurface(frame_width * i, frame_height * 2, frame_width, frame_height), 0, self.scale)
            for i in range(0, 3)]


class Weapon(sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.weapon_id = DatabaseManager.get_current_id_by_group('weapons')
        self._setup_characteristics()
        self._create_frame()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 30, 30
        self.owner = player
        self.timedelta = 0

    def deal_damage(self, enemy):
        if (((enemy.rect.centerx - self.owner.rect.centerx) ** 2 +
             (enemy.rect.centery - self.owner.rect.centery) ** 2) ** 0.5 < self.attack_distance):
            return enemy.take_damage(self.damage)
        return False

    def _setup_characteristics(self):
        self.damage, self.scale, self.attack_distance = DatabaseManager.get_characteristics_weapon_by_id(self.weapon_id)

    def _create_frame(self):
        self.image = pygame.transform.rotozoom(load_image(f'weapon_{self.weapon_id}.png', 'weapons'),
                                               0, self.scale)


class Enemy(sprite.Sprite):
    frame_time = ENEMY_FRAME_TIME
    scale = 2

    def __init__(self, enemy_id: int, position: (int, int)):
        super().__init__()

        self.enemy_id = enemy_id
        self.flag_angry = False  # Идёт ли монстр в атаку на игрока.
        self.flag_alive = True  # Жив ли монстр
        self.flag_full_death_animation = False  # Проиграна ли полная анимация смерти
        self.flag_attack = False  # Совершает ли атаку монстр
        self.direction = 'left'
        self.index_frame = 0
        self.timedelta = 0
        self.timedelta_for_attack_speed = 0
        self.distance_visible = 250

        self._setup_enemy_characteristic()
        self._create_frames()
        self.image = self.stand_frames[0]
        self.current_type_frame = self.stand_frames

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = position

        self.status_bar = EnemyStatusBar()

    def update(self, player: Character, timedelta: float):
        """Обновление"""
        if self.flag_alive:
            self.ai_movement(player)
            self.attack_to_player(player)
        elif self.current_type_frame != self.death_frames:
            self._edit_current_frames('death')
        elif self.index_frame == len(self.death_frames) - 1:
            self.flag_full_death_animation = True
        # Подсчёт временного промежутка и смена кадра анимации
        if self.flag_alive or not self.flag_full_death_animation:
            if self.timedelta < self.frame_time:
                self.timedelta += timedelta
            else:
                self.index_frame = (self.index_frame + 1) % len(self.current_type_frame)
                self.timedelta = 0
        self.image = self.current_type_frame[self.index_frame]
        self.status_bar.update((self.rect.centerx, self.rect.y), self.health / self.max_health)

    def attack_to_player(self, player: Character):
        """Логика и выдача булева значения успеха атаки"""
        if not self.flag_attack and self._is_attack_distance(player):
            self.flag_attack = True
            self._edit_current_frames('attack')
        if self.flag_attack and self.index_frame == len(self.death_frames) - 2:
            if self._is_attack_distance(player):
                player.take_damage(self.damage)
            self.flag_attack = False

    def ai_movement(self, player: Character):
        """Логика передвижения монстра относительно главного героя"""
        if not self.flag_angry and ((self.rect.centerx - player.rect.centerx) ** 2 + (
                self.rect.centery - player.rect.centery) ** 2) ** 0.5 < self.distance_visible:
            self.flag_angry = True
        if not self.flag_attack and self.flag_angry:
            if self.rect.x > player.rect.x:
                self.rect.x -= 1
                self._edit_current_frames('left')
            elif self.rect.x < player.rect.x:
                self.rect.x += 1
                self._edit_current_frames('right')
            if self.rect.y > player.rect.y:
                self.rect.y -= 1
            elif self.rect.y < player.rect.y:
                self.rect.y += 1

    def take_damage(self, value) -> bool:
        """Получение урона от игрока"""
        self.health -= value
        if self.flag_alive and self.health <= 0:
            self.flag_alive = False
            self.flag_angry = False
            return True
        return False

    def _edit_current_frames(self, mode: str = None):
        """Смена текущих фреймов анимации"""
        if mode == 'death' and self.current_type_frame != self.death_frames:
            self.current_type_frame = self.death_frames
            self.index_frame = 0
        elif mode == 'left' and self.current_type_frame != self.left_walking_frames:
            self.current_type_frame = self.left_walking_frames
            self.direction = 'left'
        elif mode == 'right' and self.current_type_frame != self.right_walking_frames:
            self.current_type_frame = self.right_walking_frames
            self.direction = 'right'
        elif mode == 'attack':
            if self.direction == 'left':
                self.current_type_frame = list(map(lambda x: pygame.transform.flip(x, True, False),
                                                   self.attack_frames))
            else:
                self.current_type_frame = self.attack_frames
            self.index_frame = 0

    def _is_attack_distance(self, player: Character) -> bool:
        return (((self.rect.centerx - player.rect.centerx) ** 2 + (self.rect.centery - player.rect.centery) ** 2) ** 0.5
                < self.attack_distance)

    def _setup_enemy_characteristic(self):
        """Установка характеристик монстра"""
        self.name, self.health, self.damage, self.attack_distance, self.speed = (
            DatabaseManager.get_characteristics_enemy_by_id(self.enemy_id))
        self.max_health = self.health
        print(self.name, self.health, self.damage, self.speed)  # [LOG]

    def _create_frames(self):
        """Создание фреймов анимации"""
        quan_walking, quan_attack, quan_death, quan_stand = (
            DatabaseManager.get_quantities_frames_enemy_by_id(self.enemy_id))
        atlas = load_image(f'enemy_{self.enemy_id}.png', 'enemies')
        atlas_width = atlas.get_width()
        atlas_height = atlas.get_height()
        frame_width = atlas_width / max(quan_walking, quan_attack, quan_death, quan_stand)
        frame_height = atlas_height / 4
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
    def apply(self, obj: pygame.sprite.Sprite):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target: pygame.sprite.Sprite):
        self.dx = SIZE[0] // 2 - (target.rect.x + target.rect.w // 2)
        self.dy = SIZE[1] // 2 - (target.rect.y + target.rect.h // 2)


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._create_frames()
        self.mask = pygame.mask.from_surface(self.image)

    def _create_frames(self):
        image = load_image('cursors.png', 'hud')
        frame_width = image.get_width() // 2
        frame_height = image.get_height()
        self.is_going_game = False
        self.frames = [image.subsurface(frame_width * i, 0, frame_width, frame_height) for i in range(2)]
        self.image = self.frames[0]
        self.rect = self.image.get_rect()

    def update_frame(self, is_going_game: bool):
        self.is_going_game = is_going_game
        if self.is_going_game:
            self.image = self.frames[1]
        else:
            self.image = self.frames[0]

    def update(self, pos: (int, int)):
        x, y = pos[0] - 3, pos[1] - 2
        if self.is_going_game:
            x, y = pos[0] - self.rect.width // 2, pos[1] - self.rect.height // 2
        self.rect.x, self.rect.y = x, y


class Hud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(load_image('empty_hud.png', 'hud'), 0, SCALE_HUD)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 10, 10
        self._init_status_bar()

    def _init_status_bar(self):
        self.health_bar = HudStatusBar('health')
        self.armor_bar = HudStatusBar('armor')
        self.ammunation_bar = HudStatusBar('ammunation')

    def get_sprites_status_bar(self) -> tuple:
        return self.health_bar, self.armor_bar, self.ammunation_bar

    def update(self, health: float, armor: float):  # ammunation: float
        self.health_bar.update(health)
        self.armor_bar.update(armor)


class HudStatusBar(pygame.sprite.Sprite):
    def __init__(self, mode: str):
        super().__init__()
        self._create_frame(mode)

    def _create_frame(self, mode: str):
        image = pygame.transform.rotozoom(load_image('statusbar.png', 'hud'), 0, SCALE_HUD)
        self.frame_width = image.get_width()
        self.frame_height = image.get_height() // 3
        if mode == 'health':
            self.full_image = image.subsurface(0, 0, self.frame_width, self.frame_height)
            self.x, self.y = 112, 22
        elif mode == 'armor':
            self.full_image = image.subsurface(0, self.frame_height, self.frame_width, self.frame_height)
            self.x, self.y = 112, 50
        elif mode == 'ammunation':
            self.full_image = image.subsurface(0, self.frame_height * 2, self.frame_width, self.frame_height)
            self.x, self.y = 112, 77
        self.image = self.full_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

    def update(self, value: float):
        if value < 0:
            value = 0
        self.image = self.full_image.subsurface(0, 0, self.frame_width * value, self.frame_height)
        self.rect.x, self.rect.y = self.x, self.y


class EnemyStatusBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = load_image('scale_status_bar.png', 'enemies')
        self.empty = load_image('empty_status_bar.png', 'enemies')
        self.image = self.empty
        self.rect = self.image.get_rect()

    def update(self, position: (int, int), value: float):
        image = self.empty.copy()
        if value < 0:
            value = 0
        image.blit(self.scale.subsurface(0, 0, self.scale.width * value, self.scale.height), (2, 2))
        self.image = image
        self.rect.x, self.rect.y = position[0] - self.rect.width // 2, position[1] - 15


class Trap(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self._create_frames()
        self.enable = False
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self, enable: bool):
        self.enable = enable
        if self.enable:
            if self.index_frame > 0:
                self.index_frame -= 1
        if not self.enable:
            if self.index_frame < len(self.frames) - 1:
                self.index_frame += 1
        self.image = self.frames[self.index_frame]

    def _create_frames(self):
        image = pygame.transform.rotozoom(load_image('trap.png', 'for_game'), 0, SCALE_MAP)
        width = image.get_width() // 3
        height = image.get_height()
        self.frames = [image.subsurface(width * i, 0, width, height) for i in range(3)]
        self.index_frame = 2
        self.image = self.frames[self.index_frame]


class Portal(pygame.sprite.Sprite):
    def __init__(self, position: (int, int)):
        super().__init__()
        self._create_frames()
        self.timedelta = 0
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position[0] - self.rect.width // 2, position[1] - self.rect.height // 2

    def update(self, timedelta, enemies):
        if self.timedelta < 0.2:
            self.timedelta += timedelta
        else:
            self.index_frame = (self.index_frame + 1) % 7
            self.timedelta = 0
        self.image = self.frames[self.index_frame]

    def _create_frames(self):
        image = load_image('portal.png', 'for_game')
        width = image.get_width() // 8
        height = image.get_height() // 3
        self.frames = [pygame.transform.rotozoom(image.subsurface(width * i, 0, width, height), 0, 3)
                       for i in range(7)]
        self.index_frame = 0
        self.image = self.frames[self.index_frame]
