import pygame
from level import Level
import config
import sys

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    level = Level(config.level_data[0], screen)
    background = pygame.image.load("img/bg.png").convert()
    largura, altura = background.get_size()
    fator = screen.get_height() / altura
    background = pygame.transform.scale(background, (largura * fator, altura * fator))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background, (0, 0))

        level.update()
        level.draw()

        pygame.display.update()
        clock.tick(config.FPS)
