import pygame
import sys
import random
from Enemy import Opponent
from Character import Character

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()


class Logic:
    pass


class Logic:
    def __init__(self, screen):
        # Звуки
        self.wave_sound = pygame.mixer.Sound('assets/audio/wing.wav')
        self.beat_sound = pygame.mixer.Sound('assets/audio/hit.wav')
        self.die_sound = pygame.mixer.Sound('assets/audio/damage1.wav')
        # Группа спрайтов врагов, это понадобится когда добавлю по несколько врагов на сцену
        self.all_enemies = pygame.sprite.Group()
        self.hp = 100
        self.target_health = 100
        self.max_hp = 100
        self.hp_bar_length = 300
        self.health_chang_speed = 5
        self.health_ratio = self.max_hp / self.hp_bar_length
        self.EnemyKill = False
        self.EnemyAttack = False
        # область атаки персонажа
        self.character_attack_rect = Character().get_attack_rect()
        self.character_body_rect = Character().get_body_rect()
        self.enemy_sprite = pygame.sprite.Sprite()
        self.EnemyPos = 1280
        self.floor_surface = pygame.image.load('assets/sprites/Background/City4.png')
        self.road_surface = pygame.image.load('assets/sprites/Background/road.png')
        self.obstacles = [pygame.image.load('assets/sprites/Obstacles/Trash2.png'),
                          pygame.image.load('assets/sprites/Obstacles/boxes2.png'),
                          pygame.image.load('assets/sprites/Obstacles/minishop2.png'),
                          pygame.image.load('assets/sprites/Obstacles/wheels2.png'), ]
        self.anim_frames = []
        self.enemy_frames = []
        self.screen = screen
        self.bg_pos = 0
        self.road_pos = 0
        self.obstaclePos = 0
        self.obstacle_index = 0
        self.Beat = False
        self.enemy_count = 0
        self.Death = False
        self.game_active = True
        self.cant_beat = False
        # область атаки врага
        self.Enemy_anim_start = Opponent().get_startattack_rect((self.EnemyPos - 200, 520))
        self.animCount = 0

    # Функция отрисовки полосы здоровья

    def advanced_health(self):
        transition_width = 0
        transition_color = (255, 0, 0)
        if self.hp < self.target_health:
            self.hp += self.health_chang_speed
            transition_width = int((self.target_health - self.hp) / self.health_ratio)
            transition_color = (0, 255, 0)

        if self.hp > self.target_health:
            self.hp -= self.health_chang_speed
            transition_width = int((self.target_health - self.hp) / self.health_ratio)
            transition_color = (255, 255, 0)
            print('sdf')
        health_bar_rect = pygame.Rect(10, 45, self.hp / self.health_ratio, 25)
        transition_bar_rect = pygame.Rect(health_bar_rect.right, 45, transition_width, 25)
        pygame.draw.rect(self.screen, (255, 0, 0), health_bar_rect)
        pygame.draw.rect(self.screen, transition_color, transition_bar_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), (10, 45, self.hp_bar_length, 25), 2)

    # Проигрывает звук
    def reproduce(self, beat=False, wave=False, die=False):
        if beat:
            beat.play()
        if wave:
            wave.play()
        if die:
            die.play()

    # Проверка произошло ли столкновение
    def check_collision(self):
        # Если враг еще не умер
        if not self.EnemyKill:
            # Если персонаж бьет
            if self.Beat:
                # Если фрейм атакующего персонажа касается врага, то враг умрет
                if self.character_attack_rect.colliderect(self.enemy_sprite.rect):
                    self.enemy_count = 0
                    self.EnemyKill = True
            # Если персонаж попадает в зону атаки врага, то он начинает атаку
            elif self.character_body_rect.colliderect(self.Enemy_anim_start):
                self.enemy_count = 0
                self.EnemyAttack = True
            # Это условие проверяет что анимация атаки точно не запущена
            if not self.cant_beat:
                # Если персонаж касается врага, то хп становится на 25 едениц меньше
                if self.character_body_rect.colliderect(self.enemy_sprite.rect):
                    self.target_health -= 25
                    if not self.Death:
                        if self.target_health <= 0:
                            self.animCount = 0
                            self.Death = True
                        else:
                            self.cant_beat = True

    def add_enemy(self):
        # добавляет 1 врага на сцену
        self.all_enemies.add(self.enemy_sprite)

    def value_of_enemies(self):
        # возвращает количество врагов на сцене
        return len(self.all_enemies)

    def animate_enemy(self):
        if self.enemy_count <= 0:
            if self.Beat:
                self.reproduce(self.beat_sound)
            self.enemy_frames.clear()
            self.enemy_frames = Opponent().get_frame(self.EnemyAttack, self.EnemyKill)
            if self.EnemyAttack:
                self.reproduce(self.wave_sound)
                if self.enemy_count == 20:
                    self.reproduce(self.beat_sound)
                self.EnemyAttack = False
        if self.enemy_count >= 24:
            # Если враг умер то
            if self.EnemyKill:
                self.enemy_sprite.kill()
                # обнуляем позицию
                self.EnemyPos = 1280
                # обнуляем позицию области атаки
                self.Enemy_anim_start.centerx = 1280 - 200
                # отменяем смерть персонажа, и флаг смерти врага
                self.Death = False
                self.EnemyKill = False
            # Очищаем список кадров
            self.enemy_frames.clear()
            self.enemy_frames = Opponent().get_frame(self.EnemyAttack, self.EnemyKill)
            # Если завершился цикл анимаций, то обнуляем счетчик
            self.enemy_count = 0
        self.enemy_sprite.image = self.enemy_frames[self.enemy_count // 4]
        self.enemy_sprite.rect = self.enemy_sprite.image.get_rect()
        self.enemy_sprite.rect.y = 520
        # Смещаем координату врага, и область его атаки
        self.Enemy_anim_start.centerx -= 8
        self.EnemyPos -= 8
        # Присваиваем координату к врагу
        self.enemy_sprite.rect.x = self.EnemyPos
        # Рисуем врага
        self.all_enemies.draw(self.screen)
        # Если враг ушел за границы экрана, то перемещаем обратно
        if self.enemy_sprite.rect.x <= -100:
            self.cant_beat = False
            self.EnemyPos = 1280
            self.Enemy_anim_start.centerx = 1280 - 200
        self.enemy_count += 1

    def draw_obstacles(self):
        if self.obstaclePos == 0:
            self.obstacle_index = random.randint(0, len(self.obstacles) - 1)
        self.obstaclePos -= 8
        self.screen.blit(self.obstacles[self.obstacle_index], (self.obstaclePos + 1280, 450))
        self.screen.blit(self.obstacles[self.obstacle_index - 1], (self.obstaclePos + 1616, 450))

    def animate_character(self):
        if self.animCount == 0 or self.animCount >= 18:
            # Если персонаж бьет или умирает, то воспроизводится соответствующий звук
            if self.Beat:
                self.reproduce(self.wave_sound)
            if self.Death:
                self.reproduce(self.die_sound)
            # очищаем завершенный список кадров анимаций
            self.anim_frames.clear()
            # запрашиваем новый список кадров
            self.anim_frames = Character().get_frame(self.Beat, self.Death)
        # Если завершился цикл анимаций, то обнуляем счетчик
        if self.animCount >= 18:
            self.animCount = 0
            # Если персонаж умер, то запрашиваем анимацию смерти и отключаем игру
            if self.animCount == 0 and self.Death:
                self.Death = False
                self.anim_frames = Character().get_frame(self.Beat, self.Death)
                self.game_active = False
            self.Beat = False
        self.screen.blit(self.anim_frames[self.animCount // 3], self.character_body_rect)
        self.animCount += 1

    def draw_back(self):
        # изменяет координату земли
        self.bg_pos -= 5
        # чтобы создать эффект бесконечного бэкграунда мы создаем 2 спрайта дороги,
        # и просто в нужный момент их переносим
        self.screen.blit(self.floor_surface, (self.bg_pos, 0))
        self.screen.blit(self.floor_surface, (self.bg_pos + 1280, 0))

    def draw_road(self):
        self.road_pos -= 8
        self.screen.blit(self.road_surface, (self.road_pos, 0))
        self.screen.blit(self.road_surface, (self.road_pos + 1280, 0))


if __name__ == '__main__':
    FPS = 60
    SIZE = WIDTH, HEIGHT = 1280, 720
    vol = 1.0
    running = True
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    game = Logic(screen)
    GRAVITY = 1.5
    game_active = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game.game_active:
                        game.obstaclePos = 0
                        game.Enemy_anim_start.centerx = 1080
                        game.EnemyPos = 1280
                        game.target_health = 100
                        game.Death = False
                        game.EnemyAttack = False
                        game.enemy_sprite.kill()
                        game.game_active = True
                    else:
                        game.Beat = True
        game.draw_back()
        game.draw_road()
        if game.game_active:
            game.draw_obstacles()
            # Если врагов на сцене нет, то добавляем
            if game.value_of_enemies() == 0:
                game.add_enemy()
            #            game.basic_health()
            game.advanced_health()
            game.animate_enemy()
            game.animate_character()
            game.check_collision()
        # этот блок обнуляет координаты если объекты вышли за сцену
        if game.EnemyPos <= -144:
            game.EnemyPos = 1280
        if game.bg_pos <= -1280:
            game.bg_pos = 0
        if game.road_pos <= -1280:
            game.road_pos = 0
        if game.obstaclePos <= -1952:
            game.obstaclePos = 0
        pygame.display.update()
        clock.tick(FPS)
