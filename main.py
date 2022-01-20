import pygame
import sys


class logic():
    def __init__(self, screen):
        self.screen = screen
        self.floor_x_pos = 0
        self.road_pos = 0

        self.animCount = 0

    def DrawCharacter(self):
        runAnimation = [pygame.image.load('assets/sprites/character_anim/RunAnim_1.png'),
               pygame.image.load('assets/sprites/character_anim/RunAnim_2.png'),
               pygame.image.load('assets/sprites/character_anim/RunAnim_3.png'),
               pygame.image.load('assets/sprites/character_anim/RunAnim_4.png'),
               pygame.image.load('assets/sprites/character_anim/RunAnim_5.png'),
               pygame.image.load('assets/sprites/character_anim/RunAnim_6.png')]

        if self.animCount >= 6:
            self.animCount = 0
        self.screen.blit(runAnimation[self.animCount // 2], (100, 500))
        self.animCount += 1

    def DrawFloor(self):
        floor_surface = pygame.image.load('assets/sprites/City4.png').convert()

        self.floor_x_pos -= 5
        self.screen.blit(floor_surface, (self.floor_x_pos, 0))
        self.screen.blit(floor_surface, (self.floor_x_pos + 1280, 0))

    def DrawRoad(self):
        road_surface = pygame.image.load('assets/sprites/road.png')

        self.road_pos -= 15
        self.screen.blit(road_surface, (self.road_pos, 0))
        self.screen.blit(road_surface, (self.road_pos + 1280, 0))


if __name__ == '__main__':
    pygame.init()
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

        game.DrawFloor()
        game.DrawRoad()
        game.DrawCharacter()

        if game.floor_x_pos <= -1280:
            game.floor_x_pos = 0
        if game.road_pos <= -1280:
            game.road_pos = 0
        pygame.display.update()
        clock.tick(120)
