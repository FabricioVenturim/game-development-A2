  
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

dict_animacoes_boy = {"parado": [0, 232, 455], "correndo": [5940, 363, 455], "pulando": [2325, 362, 483]}
sprites_boy = pygame.sprite.Group()
boy = personagem.BoyNinja(500, 500, "img/spritesheet_boy.png", dict_animacoes_boy)
sprites_boy.add(boy)

dict_animacoes_girl = {"parado": [0, 290, 500], "correndo": [6906, 372, 500], "pulando": [2910, 399, 500]}
sprites_girl = pygame.sprite.Group()
girl = personagem.GirlNinja(100, 500, "img/spritesheet_girl.png", dict_animacoes_girl)
sprites_girl.add(girl)

relogio = pygame.time.Clock()

while game:
    # control(boy_ninja)
    # maske_blit(screen, item, boy_ninja.wx, boy_ninja.wy, boy_ninja.x, boy_ninja.y, boy_ninja.w, boy_ninja.h)
    relogio.tick(30)
    screen.fill((255, 255, 255))

    
    #Eventos de segurar a tecla
    if pygame.key.get_pressed()[K_d]:
        boy.correr_direita()

    if pygame.key.get_pressed()[K_RIGHT]:
        girl.correr_direita()

    if pygame.key.get_pressed()[K_a]:
        boy.correr_esquerda() 

    if pygame.key.get_pressed()[K_LEFT]:
        girl.correr_esquerda()

    #Evetos sem segurar a tecla
    for event in pygame.event.get():
        if event.type == QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == K_w and boy.pular == False:
                boy.fun_pular()
        if event.type == pygame.KEYDOWN:
            if event.key == K_UP and girl.pular == False:
                girl.fun_pular()

        if event.type == pygame.KEYDOWN:
            if event.key == K_f:
                boy.fun_bater()
    

    sprites_boy.draw(screen)
    sprites_boy.update()
    sprites_girl.draw(screen)
    sprites_girl.update()

    pygame.display.flip()

