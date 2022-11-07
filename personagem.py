from calendar import c
import pygame
from pygame.locals import *

class Personagem(pygame.sprite.Sprite):
    # Define estados possíveis do jogador
    parado = 0 
    pulando = 1
    caindo = 2
    # Define a aceleração da gravidade
    gravidade = 6
    # Define a velocidade inicial no pulo
    aceleracao_pulo_inicial = 50

    def __init__(self, x, y, img, dict_animacoes):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.chao = 425
        self.aceleracao = self.aceleracao_pulo_inicial
        self.state = 0
        
        sprite_sheet = pygame.image.load(img).convert_alpha()
        self.imagens_ninja = []
        #self.sprite_sheet = pygame.image.load(img).convert_alpha()
        
        for posicao in dict_animacoes.values():
            print(posicao)
            inicial = posicao[0]
            largura = posicao[1]
            altura = posicao[2]
            self.corta_sprite(sprite_sheet, inicial, largura, altura) 

        self.index_lista = 0
        self.image = self.imagens_ninja[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.direita = True
        self.correr = False
        self.pular = False
        self.bater = False

    def corta_sprite(self,sprite_sheet, posicao_inicial, largura, altura):
        for i in range(0, 10):
            largura_inicial = posicao_inicial
            img = sprite_sheet.subsurface((largura_inicial + i*largura,0), (largura,altura))
            img = pygame.transform.scale(img, (largura/3, altura/3))
            self.imagens_ninja.append(img)
         
    def correr_direita(self): 
        self.direita = True
        self.correr = True
        if self.index_lista < 10:
            self.index_lista = 10
        if self.pular:
            self.rect.x += 12.5
        else:
            self.rect.x += 10

    def correr_esquerda(self):
        self.direita = False
        self.correr = True
        if self.index_lista < 10:
            self.index_lista = 10
        if self.pular:
            self.rect.x -= 12.5
        else:
            self.rect.x -= 10

    def fun_pular(self):
        self.pular = True
        self.correr = False
        self.state = 1
        if self.index_lista < 20:
            self.index_lista = 20

    def update(self):
        # Controle de animação do personagem para correr
        if self.correr and self.pular == False:
            if self.index_lista > 19:   
                self.index_lista = 10
            self.index_lista += 0.5
            self.image = self.imagens_ninja[int(self.index_lista)]
            
            # vira a imagem se o personagem estiver olhando para o outro lado
            if self.direita == False:
                self.image = pygame.transform.flip(self.image, True, False)
            self.correr = False

        # Controle de animação do personagem para pular
        elif self.pular:
            
            ####### animação #######
            if self.index_lista > 29:   
                self.index_lista = 20
            self.index_lista += 0.5
            self.image = self.imagens_ninja[int(self.index_lista)]
            
            # vira a imagem se o personagem estiver olhando para o outro lado
            if self.direita == False:
                self.image = pygame.transform.flip(self.image, True, False)
            self.correr = False
            ########## 

            # Atualiza o estado para caindo
            if self.aceleracao < 0:
                self.state = 2
           
            if self.state == 1: 
                self.rect.y -= self.aceleracao
                self.aceleracao -= self.gravidade
            if self.state == 2: 
                self.rect.y += self.aceleracao
                self.aceleracao += self.gravidade

            # Se bater no chão, para de cair
            if self.rect.y > self.chao:
                self.rect.y = self.chao
                # Para de cair
                self.aceleracao = self.aceleracao_pulo_inicial
                # Atualiza o estado para parado
                self.pular = False
                self.state = 0
                
        # Controle de animação do personagem para parado
        else: 
            if self.index_lista > 9:
                self.index_lista = 0
            self.index_lista += 0.5
            self.image = self.imagens_ninja[int(self.index_lista)]
            # vira a imagem se o personagem estiver olhando para o outro lado
            if self.direita == False:
                self.image = pygame.transform.flip(self.image, True, False)

class BoyNinja(Personagem):
    def __init__(self, x, y, img, dict_animacoes):
        super().__init__(x, y, img, dict_animacoes)

    # #batendo
    #     for i in range(0,10): 
    #         largura_inicial = 0
    #         img = sprite_sheet.subsurface((largura_inicial + i*536,0), (536,495))
    #         img = pygame.transform.scale(img, (536/3, 495/3))
    #         self.imagens_ninja.append(img) 
    
    def fun_bater(self):
        self.bater = True
        if self.index_lista < 30:
            self.index_lista = 30
        
    # def update(self):
    #     #############
    #     ### Bater ###
    #     #############
    #     if self.bater:
    #         if self.index_lista > 39:   
    #             self.index_lista = 30
    #             self.bater = False
    #         self.index_lista += 0.5
    #         self.image = self.imagens_ninja[int(self.index_lista)]
            
    #         # vira a imagem se o personagem estiver olhando para o outro lado
    #         if self.direita == False:
    #             self.image = pygame.transform.flip(self.image, True, False)


class GirlNinja(Personagem):
    def __init__(self, x, y, img, dict_animacoes):
        super().__init__(x, y, img, dict_animacoes)