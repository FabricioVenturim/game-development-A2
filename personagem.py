from calendar import c
import pygame
from pygame.locals import *



class Personagem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        sprite_sheet = pygame.image.load("img/spritesheet.png").convert_alpha()
        pygame.sprite.Sprite.__init__(self)
        self.imagens_ninja = []
        # parado
        for i in range(0, 9):
            largura_inicial = 10412
            img = sprite_sheet.subsurface((largura_inicial + i*232,0), (232,455))
            img = pygame.transform.scale(img, (232/3, 455/3))
            self.imagens_ninja.append(img)

        # correndo
        for i in range(0,10):
            largura_inicial = 21160
            img = sprite_sheet.subsurface((largura_inicial + i*363,0), (363,455))
            img = pygame.transform.scale(img, (363/3, 455/3))
            self.imagens_ninja.append(img) # 9 a 18

        self.index_lista = 0
        self.image = self.imagens_ninja[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.direita = True
        self.correr = False

    def correr_direita(self): 
        self.direita = True
        self.correr = True
        if self.index_lista < 9:
            self.index_lista = 9
        self.rect.x += 8

    def correr_esquerda(self):
        self.direita = False
        self.correr = True
        if self.index_lista < 9:
            self.index_lista = 9
        self.rect.x -= 8

    def update(self):
        if self.correr:
            if self.index_lista > 18:   
                self.index_lista = 9
            self.index_lista += 0.5
            self.image = self.imagens_ninja[int(self.index_lista)]
            
            # vira a imagem se o personagem estiver olhando para o outro lado
            if self.direita == False:
                self.image = pygame.transform.flip(self.image, True, False)
            self.correr = False
            
        else: 
            if self.index_lista > 8:
                self.index_lista = 0
            self.index_lista += 0.5
            self.image = self.imagens_ninja[int(self.index_lista)]
            # vira a imagem se o personagem estiver olhando para o outro lado
            if self.direita == False:
                self.image = pygame.transform.flip(self.image, True, False)
    