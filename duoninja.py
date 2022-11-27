import pygame
from pygame.locals import *
import personagem

class DuoNinja:
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        #definindo os personagens
        dict_animacoes_boy = {"parado": [0, 232, 455, 10, 3.1], "correndo": [5940, 363, 455, 10, 3.1], "pulando": [2325, 362, 483, 10, 3.1], "batendo": [19410, 536, 495, 10, 3.1], "voando": [24787,443, 454, 10, 3.1]}
        self.sprites_boy = pygame.sprite.Group()
        self.boy = personagem.BoyNinja(500, 200, "img/spritesheet_boy.png", dict_animacoes_boy)
        self.sprites_boy.add(self.boy)
                                        
        dict_animacoes_girl = {"parado": [0, 290, 500, 10, 3.5], "correndo": [6906, 372, 500, 10, 3.5], "pulando": [2910, 399, 500, 10, 3.5], "deslizando": [16425, 397, 401, 10, 3.5], "ataque": [20400, 383, 514, 10, 3.5]}
        self.sprites_girl = pygame.sprite.Group()
        self.girl = personagem.GirlNinja(300, 200, "img/spritesheet_girl.png", dict_animacoes_girl, self.screen)
        self.sprites_girl.add(self.girl)

        dict_animacoes_robo= {"parado": [0, 567, 555, 10, 3.5], "correndo": [5670, 567, 550, 8, 3.5], "morrendo": [10190 , 562, 519, 10,3.5]}
        self.sprites_robo = pygame.sprite.Group()
        self.robo = personagem.Robo(870, 450, 100, 200, "img/spritesheet_robo.png", dict_animacoes_robo, direita_movimentacao = True)
        self.sprites_robo.add(self.robo)

        ##### Teste de objetos para colisão, no futuro isso será um objeto #####
        self.chao1 = pygame.Rect(200, 600, 1920, 25)
        self.chao2 = pygame.Rect(900, 400, 1920, 25)
        self.list_chao = [self.chao1, self.chao2]

        self.relogio = pygame.time.Clock()

    def main_loop(self):
        while True:
            self._eventos()
            self._game_logica()
            self._draw()

    def _init_pygame(self):
        pygame.init()

    def _eventos(self):
        #Eventos de segurar a tecla
        if pygame.key.get_pressed()[K_d] and self.boy.bater == False:
            self.boy.fun_correr_direita()

        elif pygame.key.get_pressed()[K_a] and self.boy.bater == False:
            self.boy.fun_correr_esquerda()     

        if pygame.key.get_pressed()[K_DOWN] and self.girl.state == 0:
            self.girl.fun_deslizar()

        elif pygame.key.get_pressed()[K_RIGHT] and self.girl.atirar == False:
            self.girl.fun_correr_direita()

        elif pygame.key.get_pressed()[K_LEFT] and self.girl.atirar == False:
            self.girl.fun_correr_esquerda()
        
        #Evetos sem segurar a tecla
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
                
            if event.type == pygame.KEYDOWN:
                
                if event.key == K_w and self.boy.state == 0 and self.boy.bater == False:
                    self.boy.fun_pular()
                elif pygame.key.get_pressed()[K_w] and self.boy.state != 0:
                    self.boy.fun_planar()

                if event.key == K_f and self.boy.state == 0:        
                    self.boy.fun_bater()
                
                if event.key == K_RSHIFT and self.girl.state == 0:
                    self.girl.fun_atirar()
                
                if event.key == K_UP and self.girl.state == 0 and self.girl.atirar == False:
                    self.girl.fun_pular()
                
                #teste 
                if event.key == K_g:
                    self.robo.fun_morrer()

            if event.type == pygame.KEYUP:
                if event.key == K_w and self.boy.state != 1 and self.boy.state != 0:
                    self.boy.fun_cair()

    def _game_logica(self):
        ###### TUDO TESTE PARA COLISÃO, QUEM FICOU COM O CENÁRIO VER COMO ISSO FUNCIONA CERTINHO######
        ###### COMO AINDA NÃO SEI COMO VAI FUNCIONAR O CENÁRIO, NÃO SEI COMO FAZER A COLISÃO ######

        # Colisão entre personagens são aqui ou no arquivo de personagem?
        col1= self.boy.rect.colliderect(self.robo.rect) 
        col2= self.girl.kunai.rect.colliderect(self.robo.rect)
        if ((col1 and self.boy.bater == True) or col2) and self.robo.vivo == True:
            self.robo.fun_morrer()


        #Colisão entre personagens e chão 
        #OBS: Não está ficando certinho com o chão, mas não sei resolver
        
        #boy
        for chao in self.list_chao:
            col_boy = self.boy.rect.colliderect(chao)
            if col_boy and self.boy.state != 1:
                self.boy.state = 0
                break
            elif self.boy.state != 1:
                self.boy.state = 2
        #girl
        for chao in self.list_chao:
            col_girl = self.girl.rect.colliderect(chao)
            if col_girl and self.girl.state != 1:
                self.girl.state = 0
                break
            elif self.girl.state != 1:
                self.girl.state = 2
        #robo
        for chao in self.list_chao:
            col_robo = self.robo.rect.colliderect(chao)
            if col_robo and self.robo.state != 1:
                self.robo.state = 0
                break
            elif self.robo.state != 1:
                self.robo.state = 2

        #kunai
        for chao in self.list_chao:
            col_kunai = self.girl.kunai.rect.colliderect(chao)
            if col_kunai:
                self.girl.kunai.atirar = False
                break
        
        #Verifica campo de visão do robo
        if self.robo.vivo:
            self.robo.verifica_player(self.boy)
            self.robo.verifica_player(self.girl)

    def _draw(self):
        self.screen.fill((255, 255, 255))

        pygame.draw.rect(self.screen, (0, 0, 0), self.chao1)
        pygame.draw.rect(self.screen, (0, 0, 0), self.chao2)

        self.sprites_boy.draw(self.screen)
        self.sprites_boy.update()
        self.sprites_girl.draw(self.screen)
        self.sprites_girl.update()

        self.sprites_robo.draw(self.screen)
        self.sprites_robo.update()
        pygame.display.flip()
        self.relogio.tick(60)