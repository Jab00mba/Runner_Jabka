import pygame


class Character:
    def __init__(self):
        self.step = 0
        self.attack_pic = pygame.image.load('assets/sprites/character_anim/CharacterIdle/BeatAnim.png')
        self.body_pic = pygame.image.load('assets/sprites/character_anim/CharacterIdle/Character.png')
        self.BeatAnimation = [pygame.image.load('assets/sprites/character_anim/Beat/BeatAnim_1.png'),
                              pygame.image.load('assets/sprites/character_anim/Beat/BeatAnim_2.png'),
                              pygame.image.load('assets/sprites/character_anim/Beat/BeatAnim_3.png'),
                              pygame.image.load('assets/sprites/character_anim/Beat/BeatAnim_4.png'),
                              pygame.image.load('assets/sprites/character_anim/Beat/BeatAnim_5.png'),
                              pygame.image.load('assets/sprites/character_anim/Beat/BeatAnim_6.png')]
        self.runAnimation = [pygame.image.load('assets/sprites/character_anim/RunAnim_1.png'),
                             pygame.image.load('assets/sprites/character_anim/RunAnim_2.png'),
                             pygame.image.load('assets/sprites/character_anim/RunAnim_3.png'),
                             pygame.image.load('assets/sprites/character_anim/RunAnim_4.png'),
                             pygame.image.load('assets/sprites/character_anim/RunAnim_5.png'),
                             pygame.image.load('assets/sprites/character_anim/RunAnim_6.png')]
        self.deathAnimation = [pygame.image.load('assets/sprites/character_anim/CharacterDeath/Death_anim_1.png'),
                               pygame.image.load('assets/sprites/character_anim/CharacterDeath/Death_anim_2.png'),
                               pygame.image.load('assets/sprites/character_anim/CharacterDeath/Death_anim_3.png'),
                               pygame.image.load('assets/sprites/character_anim/CharacterDeath/Death_anim_4.png'),
                               pygame.image.load('assets/sprites/character_anim/CharacterDeath/Death_anim_5.png'),
                               pygame.image.load('assets/sprites/character_anim/CharacterDeath/Death_anim_6.png'), ]

    # Функция возвращает фрейм области аттаки персонажа
    def get_attack_rect(self):
        return self.attack_pic.get_rect(center=(420, 620))

    # Функция возвращает фрейм тела персонажа
    def get_body_rect(self):
        return self.body_pic.get_rect(center=(272, 620))

    def get_surface(self):
        return self.body_pic

    def get_frame(self, attack, Death):
        if Death:
            return self.deathAnimation
        elif attack:
            return self.BeatAnimation
        return self.runAnimation
