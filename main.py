import pygame
from level import Level
import config
import sys

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    level = Level(config.level_data[0], screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))

        level.update()
        level.draw()

        pygame.display.update()
        clock.tick(config.FPS)
