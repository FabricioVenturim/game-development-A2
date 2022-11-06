from calendar import c
import pygame
from pygame.locals import *

# Define estados possíveis do jogador

parado = 0 
pulando = 1
caindo = 2
# Define a aceleração da gravidade
gravidade = 5
# Define a velocidade inicial no pulo
velo_pulo = 40

class Personagem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.chao = 425
        self.speedy = velo_pulo
        self.state = 0

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

        # pulando
        for i in range(0,10): 
            largura_inicial = 12510
            img = sprite_sheet.subsurface((largura_inicial + i*362,0), (362,483))
            img = pygame.transform.scale(img, (362/3, 483/3))
            self.imagens_ninja.append(img) # 9 a 18


        self.index_lista = 0
        self.image = self.imagens_ninja[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.direita = True
        self.correr = False
        self.pular = False
    
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

    def fun_pular(self):
        self.pular = True
        self.state = 1
        if self.index_lista < 18:
            self.index_lista = 18

  
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

        if self.pular:
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
            if self.index_lista > 8:
                self.index_lista = 0
            self.index_lista += 0.5
            self.image = self.imagens_ninja[int(self.index_lista)]
            # vira a imagem se o personagem estiver olhando para o outro lado
            if self.direita == False:
                self.image = pygame.transform.flip(self.image, True, False)
    