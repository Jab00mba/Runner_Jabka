import pygame
import sys
import random
from Enemy import Opponent
from Character import Character

pygame.init()


class logic():
    floor_surface = pygame.image.load('assets/sprites/Background/City4.png')

    road_surface = pygame.image.load('assets/sprites/Background/road.png')

    obstacles = [pygame.image.load('assets/sprites/Obstacles/Trash2.png'),
                 pygame.image.load('assets/sprites/Obstacles/boxes2.png'),
                 pygame.image.load('assets/sprites/Obstacles/minishop2.png'),
                 pygame.image.load('assets/sprites/Obstacles/wheels2.png'), ]

    def __init__(self, screen):
        self.all_enemies = pygame.sprite.Group()
        self.hp = 100

        self.EnemyKill = False
        self.EnemyAttack = False

        self.character_attack_rect = Character().get_attack_rect()
        self.character_body_rect = Character().get_body_rect()

        self.EnemyPos = 1280

        self.enemy_sprite = pygame.sprite.Sprite()
        self.abushka = 1280

        self.enemy_sprite_attack_rect = Opponent().get_attack_rect((1280, 610))
        self.enemy_sprite_body_rect = Opponent().get_body_rect((1278, 610))
        self.enemy_sprite_startattack_rect = Opponent().get_startattack_rect((1196, 610))

        self.floor_surface = logic.floor_surface
        self.road_surface = logic.road_surface
        self.obstacles = logic.obstacles

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

        self.animCount = 0

    def check_collision(self):
        if not self.EnemyKill:
            if self.Beat:
                if self.character_attack_rect.colliderect(self.enemy_sprite.rect):
                    self.EnemyKill = True
                    self.enemy_count = 0
            elif self.character_body_rect.colliderect(Opponent().get_startattack_rect((self.abushka - 200, 520))):
                self.enemy_count = 0
                self.EnemyAttack = True
            if not self.cant_beat:
                if self.character_body_rect.colliderect(self.enemy_sprite.rect):
                    if self.hp <= 0:
                        self.animCount = 0
                        self.Death = True
                    else:
                        self.hp -= 25
                        self.cant_beat = True

    def add_enemy(self):
        self.all_enemies.add(self.enemy_sprite)

    def value_of_enemies(self):
        return len(self.all_enemies)

    def animate_enemy(self):
        if self.enemy_count <= 0:
            self.enemy_frames.clear()
            self.enemy_frames = Opponent().get_frame(self.EnemyAttack, self.EnemyKill)
            self.EnemyAttack = False
        if self.enemy_count >= 24:
            if self.EnemyAttack:
                self.EnemyAttack = False
            if self.EnemyKill:
                self.EnemyAttack = False
                self.Death = False
                self.enemy_sprite.kill()
                self.abushka = 1280
                self.EnemyKill = False
            self.enemy_frames.clear()
            self.enemy_frames = Opponent().get_frame(self.EnemyAttack, self.EnemyKill)
            self.enemy_count = 0
        self.enemy_sprite.image = self.enemy_frames[self.enemy_count // 4]
        self.enemy_sprite.rect = self.enemy_sprite.image.get_rect()
        self.enemy_sprite.rect.y = 520
        self.abushka -= 8
        self.enemy_sprite.rect.x = self.abushka
        self.all_enemies.draw(self.screen)

        if self.enemy_sprite.rect.x <= -100:
            self.cant_beat = False
            self.abushka = 1280
        self.enemy_count += 1

    def draw_obstacles(self):
        if self.obstaclePos == 0:
            self.obstacle_index = random.randint(0, len(self.obstacles) - 1)
        self.obstaclePos -= 8
        self.screen.blit(self.obstacles[self.obstacle_index], (self.obstaclePos + 1280, 450))
        self.screen.blit(self.obstacles[self.obstacle_index - 1], (self.obstaclePos + 1616, 450))

    def animate_character(self):
        if self.animCount == 0:
            self.anim_frames.clear()
            self.anim_frames = Character().get_frame(self.Beat, self.hp)

        if self.animCount >= 18:
            if self.Death:
                self.game_active = False
            self.anim_frames.clear()
            self.anim_frames = Character().get_frame(self.Beat, self.hp)
            self.animCount = 0
            self.Beat = False
            self.Death = False

        self.screen.blit(self.anim_frames[self.animCount // 3], self.character_body_rect)
        self.animCount += 1

    def draw_floor(self):
        self.bg_pos -= 5
        self.screen.blit(self.floor_surface, (self.bg_pos, 0))
        self.screen.blit(self.floor_surface, (self.bg_pos + 1280, 0))

    def draw_road(self):
        self.road_pos -= 8
        self.screen.blit(self.road_surface, (self.road_pos, 0))
        self.screen.blit(self.road_surface, (self.road_pos + 1280, 0))


if __name__ == '__main__':

    FPS = 60
    SIZE = WIDTH, HEIGHT = 1280, 720

    running = True
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    game = logic(screen)
    GRAVITY = 1.5
    game_active = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.Beat = True

        game.draw_floor()
        game.draw_road()
        game.draw_obstacles()
        if game.value_of_enemies() == 0:
            game.add_enemy()
        game.animate_enemy()
        game.animate_character()
        game.check_collision()

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
