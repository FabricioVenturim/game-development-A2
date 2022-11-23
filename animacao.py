  
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
                            # 0 - 9 parado        # 10 - 19 correr                # 20 - 29 pular                # 30 - 39 atacar           # 40 - 49 voar      
dict_animacoes_boy = {"parado": [0, 232, 455], "correndo": [5940, 363, 455], "pulando": [2325, 362, 483], "batendo": [19400, 536, 495], "voando": [24787,443, 454]}
sprites_boy = pygame.sprite.Group()
boy = personagem.BoyNinja(500, 500, "img/spritesheet_boy.png", dict_animacoes_boy)
sprites_boy.add(boy)
                                # 0 - 9 parado        # 10 - 19 correr                # 20 - 29 pular                # 30 - 39 deslizar
dict_animacoes_girl = {"parado": [0, 290, 500], "correndo": [6906, 372, 500], "pulando": [2910, 399, 500], "deslizando": [16425, 397, 401], "ataque": [20400, 383, 514]}
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

    elif pygame.key.get_pressed()[K_a]:
        boy.correr_esquerda()     

    if pygame.key.get_pressed()[K_DOWN]:
        girl.fun_deslizar()

    elif pygame.key.get_pressed()[K_RIGHT] and girl.deslizar == False:
        girl.correr_direita()

    elif pygame.key.get_pressed()[K_LEFT] and girl.deslizar == False:
        girl.correr_esquerda()

    

    #Evetos sem segurar a tecla
    for event in pygame.event.get():
        if event.type == QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == K_w and boy.state == 0:
                boy.fun_pular()
            elif pygame.key.get_pressed()[K_w] and boy.state != 0:
                boy.fun_planar()

            if event.key == K_UP and girl.pular == False:
                girl.fun_pular()

            if event.key == K_f:
                boy.fun_bater()

            if event.key == K_RSHIFT:
                girl.fun_atirar()

        if event.type == pygame.KEYUP:
            if event.key == K_w and boy.pular == False and boy.state != 0:
                boy.fun_cair()

    sprites_boy.draw(screen)
    sprites_boy.update()
    sprites_girl.draw(screen)
    sprites_girl.update()

    pygame.display.flip()

