import pygame


class Opponent:
    def __init__(self):
        self.WoodCutterEnemySurface = pygame.image.load('assets/sprites/character_anim/EnemyIdle/Woodcutter2.png')
        self.attack_sprite = pygame.sprite.Sprite()
        self.attack_pic = pygame.image.load('assets/sprites/character_anim/EnemyIdle/WoodCutterAttac_5.png')
        self.body_pic = pygame.image.load('assets/sprites/character_anim/EnemyIdle/Woodcutter2.png')
        self.attack_sprite.image = pygame.image.load('assets/sprites/character_anim/EnemyIdle/WoodCutterAttac_6.png')
        self.WoodCutterEnemyBeatAnimation = [
            pygame.image.load('assets/sprites/character_anim/EnemyAttack/WoodCutterAttac_1.png'),
            pygame.image.load('assets/sprites/character_anim/EnemyAttack/WoodCutterAttac_2.png'),
            pygame.image.load('assets/sprites/character_anim/EnemyAttack/WoodCutterAttac_3.png'),
            pygame.image.load('assets/sprites/character_anim/EnemyAttack/WoodCutterAttac_4.png'),
            pygame.image.load('assets/sprites/character_anim/EnemyAttack/WoodCutterAttac_5.png'),
            pygame.image.load('assets/sprites/character_anim/EnemyAttack/WoodCutterAttac_6.png')]
        self.WoodCutterEnemyDeathAnimation = [
            pygame.image.load('assets/sprites/character_anim/EnemyDeath/new_type/WoodCutterDeath_1.png'),
            pygame.image.load('assets/sprites/character_anim/EnemyDeath/new_type/WoodCutterDeath_2.png'),
            pygame.image.load('assets/sprites/character_anim/EnemyDeath/new_type/WoodCutterDeath_3.png'),
            pygame.image.load('assets/sprites/character_anim/EnemyDeath/new_type/WoodCutterDeath_4.png'),
            pygame.image.load('assets/sprites/character_anim/EnemyDeath/new_type/WoodCutterDeath_5.png'),
            pygame.image.load('assets/sprites/character_anim/EnemyDeath/new_type/WoodCutterDeath_6.png')]

    def get_startattack_rect(self, coords):
        return self.attack_sprite.image.get_rect(topleft=coords)

    def get_attack_rect(self, coords):
        return self.attack_pic.get_rect(center=coords)

    def get_body_rect(self, coords):
        return self.body_pic.get_rect(center=coords)

    def get_frame(self, attack, death=False):
        if death:
            return self.WoodCutterEnemyDeathAnimation
        if attack:
            return self.WoodCutterEnemyBeatAnimation
        return [self.WoodCutterEnemySurface for _ in range(6)]
