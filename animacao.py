  
import pygame
from pygame.locals import *
import personagem
import os
import sys

pygame.init()
w = 1152
h = 648
screen = pygame.display.set_mode((w, h))
game = True

### TESTE ###

todas_as_sprites = pygame.sprite.Group()
girl = personagem.Personagem(500, 200)
todas_as_sprites.add(girl)

########################

relogio = pygame.time.Clock()

while game:
    # control(boy_ninja)
    # maske_blit(screen, item, boy_ninja.wx, boy_ninja.wy, boy_ninja.x, boy_ninja.y, boy_ninja.w, boy_ninja.h)
    relogio.tick(30)
    screen.fill((255, 255, 255))


    if pygame.key.get_pressed()[K_d]:
        girl.correr_direita() 

    if pygame.key.get_pressed()[K_a]:
        girl.correr_esquerda() 

    for event in pygame.event.get():
        if event.type == QUIT:
            game = False

    todas_as_sprites.draw(screen)
    todas_as_sprites.update()
    pygame.display.flip()

