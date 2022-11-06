from calendar import c
import pygame
from pygame.locals import *

# Define estados possíveis do jogador

parado = 0 
pulando = 1
caindo = 2
# Define a aceleração da gravidade
gravidade = 6
# Define a velocidade inicial no pulo
velo_pulo = 50

class Personagem(pygame.sprite.Sprite):
    def __init__(self, x, y, img, dict_animacoes):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.chao = 425
        self.speedy = velo_pulo
        self.state = 0

        sprite_sheet = pygame.image.load(img).convert_alpha()
        self.imagens_ninja = []
        
        # parado
    
        for i in range(0, 10):
            largura_inicial = dict_animacoes["parado"][0]
            img = sprite_sheet.subsurface((largura_inicial + i*dict_animacoes["parado"][1],0), (dict_animacoes["parado"][1],dict_animacoes["parado"][2]))
            img = pygame.transform.scale(img, (dict_animacoes["parado"][1]/3, dict_animacoes["parado"][2]/3))
            self.imagens_ninja.append(img)

        # correndo
        for i in range(0,10):
            largura_inicial = dict_animacoes["correndo"][0]
            img = sprite_sheet.subsurface((largura_inicial + i*dict_animacoes["correndo"][1],0), (dict_animacoes["correndo"][1],dict_animacoes["correndo"][2]))
            img = pygame.transform.scale(img, (dict_animacoes["correndo"][1]/3, dict_animacoes["correndo"][2]/3))
            self.imagens_ninja.append(img) 

        # pulando
        for i in range(0,10): 
            largura_inicial = dict_animacoes["pulando"][0]
            img = sprite_sheet.subsurface((largura_inicial + i*dict_animacoes["pulando"][1],0), (dict_animacoes["pulando"][1],dict_animacoes["correndo"][2]))
            img = pygame.transform.scale(img, (dict_animacoes["pulando"][1]/3, dict_animacoes["pulando"][2]/3))
            self.imagens_ninja.append(img) 

        self.index_lista = 0
        self.image = self.imagens_ninja[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.direita = True
        self.correr = False
        self.pular = False
        self.bater = False

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
        #############
        ## Correr ###
        #############
        if self.correr and self.pular == False:
            if self.index_lista > 19:   
                self.index_lista = 10
            self.index_lista += 0.5
            self.image = self.imagens_ninja[int(self.index_lista)]
            
            # vira a imagem se o personagem estiver olhando para o outro lado
            if self.direita == False:
                self.image = pygame.transform.flip(self.image, True, False)
            self.correr = False

        #############
        ### Pular ###
        #############
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
            if self.speedy < 0:
                self.state = 2
           
            if self.state == 1: 
                self.rect.y -= self.speedy
                self.speedy -= gravidade
            if self.state == 2: 
                self.rect.y += self.speedy
                self.speedy += gravidade

            # Se bater no chão, para de cair
            if self.rect.y > self.chao:
                self.rect.y = self.chao
                # Para de cair
                self.speedy = velo_pulo
                # Atualiza o estado para parado
                self.pular = False
                self.state = 0

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