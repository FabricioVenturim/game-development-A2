  
import pygame
from pygame.locals import *
import personagem

##
## Aqui eu só fiz o básico para testar as classes de personagem, quando tiver um arquivo main eu arrumo
##

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
game = True

#############
#Personagens#
#############
                                  
dict_animacoes_boy = {"parado": [0, 232, 455, 10, 3.1], "correndo": [5940, 363, 455, 10, 3.1], "pulando": [2325, 362, 483, 10, 3.1], "batendo": [19410, 536, 495, 10, 3.1], "voando": [24787,443, 454, 10, 3.1]}
sprites_boy = pygame.sprite.Group()
boy = personagem.BoyNinja(500, 200, "img/spritesheet_boy.png", dict_animacoes_boy)
sprites_boy.add(boy)
                                
dict_animacoes_girl = {"parado": [0, 290, 500, 10, 3.5], "correndo": [6906, 372, 500, 10, 3.5], "pulando": [2910, 399, 500, 10, 3.5], "deslizando": [16425, 397, 401, 10, 3.5], "ataque": [20400, 383, 514, 10, 3.5]}
sprites_girl = pygame.sprite.Group()
girl = personagem.GirlNinja(300, 500, "img/spritesheet_girl.png", dict_animacoes_girl, screen)
sprites_girl.add(girl)

dict_animacoes_robo= {"parado": [0, 567, 555, 10, 3.5], "correndo": [5670, 567, 550, 8, 3.5], "morrendo": [10190 , 562, 519, 10,3.5]}
sprites_robo = pygame.sprite.Group()
robo = personagem.Robo(950, 250, 200, 280 , "img/spritesheet_robo.png", dict_animacoes_robo)
sprites_robo.add(robo)


relogio = pygame.time.Clock()

##### Teste de objetos para colisão #####
chao1 = pygame.Rect(200, 600, 1920, 25)
chao2 = pygame.Rect(900, 400, 1920, 25)
list_chao = [chao1,chao2]

while game:
    relogio.tick(60)
    screen.fill((255, 255, 255))

    pygame.draw.rect(screen, (0, 0, 0), chao1)
    pygame.draw.rect(screen, (0, 0, 0), chao2)
    
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
                robo.fun_morrer()

        if event.type == pygame.KEYUP:
            if event.key == K_w and boy.pular == False and boy.state != 0:
                boy.fun_cair()

    ###### TUDO TESTE PARA COLISÃO, QUEM FICOU COM O CENÁRIO VER COMO ISSO FUNCIONA CERTINHO######

    # Colisão entre personagens são aqui ou no arquivo de personagem?
    col1= boy.rect.colliderect(robo.rect) 
    col2= girl.kunai.rect.colliderect(robo.rect)
    if (col1 and boy.bater == True) or col2:
        robo.fun_morrer()


    #Colisão entre personagens e chão 
    #OBS: Não está ficando certinho com o chão, mas não sei resolver
    
    #boy
    for chao in list_chao:
        col_boy = boy.rect.colliderect(chao)
        if col_boy and boy.state != 1:
            boy.state = 0
            break
        elif boy.pular == False:
            boy.state = 2
    #girl
    for chao in list_chao:
        col_girl = girl.rect.colliderect(chao)
        if col_girl and girl.state != 1:
            girl.state = 0
            break
        elif girl.pular == False:
            girl.state = 2
    #robo
    for chao in list_chao:
        col_robo = robo.rect.colliderect(chao)
        if col_robo and robo.state != 1:
            robo.state = 0
            break
        elif robo.pular == False:
            robo.state = 2

    #kunai
    for chao in list_chao:
        col_kunai = girl.kunai.rect.colliderect(chao)
        if col_kunai:
           girl.kunai.atirar = False
           break

    # Parte importante: atualiza os sprites
    sprites_boy.draw(screen)
    sprites_boy.update()
    sprites_girl.draw(screen)
    sprites_girl.update()

    sprites_robo.draw(screen)
    sprites_robo.update()

    pygame.display.flip()
