  
import pygame
from pygame.locals import *
import personagem

##
## Aqui eu só fiz o básico para testar as classes de personagem, quando tiver um arquivo main eu arrumo
##

pygame.init()
w = 1152
h = 648
screen = pygame.display.set_mode((w, h))
game = True

#############
#Personagens#
#############
                                  
dict_animacoes_boy = {"parado": [0, 232, 455, 10, 2.65], "correndo": [5940, 363, 455, 10, 2.65], "pulando": [2325, 362, 483, 10, 2.65], "batendo": [19410, 536, 495, 10, 2.65], "voando": [24787,443, 454, 10, 2.65]}
sprites_boy = pygame.sprite.Group()
boy = personagem.BoyNinja(500, 500, "img/spritesheet_boy.png", dict_animacoes_boy)
sprites_boy.add(boy)
                                
dict_animacoes_girl = {"parado": [0, 290, 500, 10, 3], "correndo": [6906, 372, 500, 10, 3], "pulando": [2910, 399, 500, 10, 3], "deslizando": [16425, 397, 401, 10, 3], "ataque": [20400, 383, 514, 10, 3]}
sprites_girl = pygame.sprite.Group()
girl = personagem.GirlNinja(100, 500, "img/spritesheet_girl.png", dict_animacoes_girl, screen)
sprites_girl.add(girl)

dict_animacoes_robo= {"parado": [0, 567, 555, 10, 3], "correndo": [5670, 567, 550, 8, 3], "morrendo": [10190 , 562, 519, 10, 3]}
sprites_robo = pygame.sprite.Group()
robo = personagem.Robo(100, 600, 200, "img/spritesheet_robo.png", dict_animacoes_robo)
sprites_robo.add(robo)


relogio = pygame.time.Clock()

while game:
    relogio.tick(30)
    screen.fill((255, 255, 255))

    
    #Eventos de segurar a tecla
    if pygame.key.get_pressed()[K_d] and boy.bater == False:
        boy.correr_direita()

    elif pygame.key.get_pressed()[K_a] and boy.bater == False:
        boy.correr_esquerda()     

    if pygame.key.get_pressed()[K_DOWN] and girl.pular == False:
        girl.fun_deslizar()

    elif pygame.key.get_pressed()[K_RIGHT] and girl.atirar == False:
        girl.correr_direita()

    elif pygame.key.get_pressed()[K_LEFT] and girl.atirar == False:
        girl.correr_esquerda()
    
    #Evetos sem segurar a tecla
    for event in pygame.event.get():
        if event.type == QUIT:
            game = False
            
        if event.type == pygame.KEYDOWN:
            
            if event.key == K_w and boy.state == 0 and boy.bater == False:
                boy.fun_pular()
            elif pygame.key.get_pressed()[K_w] and boy.state != 0:
                boy.fun_planar()

            if event.key == K_f and boy.state == 0:         #criar get para state
                boy.fun_bater()
            
            if event.key == K_RSHIFT and girl.state == 0:
                girl.fun_atirar()
            
            if event.key == K_UP and girl.pular == False and girl.atirar == False:
                girl.fun_pular()
            
            #teste 
            if event.key == K_g:
                robo.test_morte()

        if event.type == pygame.KEYUP:
            if event.key == K_w and boy.pular == False and boy.state != 0:
                boy.fun_cair()

    sprites_boy.draw(screen)
    sprites_boy.update()
    sprites_girl.draw(screen)
    sprites_girl.update()

    sprites_robo.draw(screen)
    sprites_robo.update()

    pygame.display.flip()
