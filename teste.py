import pygame
from sys import exit
from objetos import Alavanca

pygame.init()
screen = pygame.display.set_mode((800,400))
clock = pygame.time.Clock()


#alavanca_surf = pygame.image.load("alavanca1.png").convert_alpha()
#alavanca_surf.get_rect(midbottom = (80,300))
alavanca = Alavanca(50,50)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    alavanca.desenhar(screen)


    pygame.display.update()
    clock.tick(60)