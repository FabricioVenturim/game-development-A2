import pygame, sys
from time import sleep
from pygame import mixer
from pygame.locals import *

#para começar o pygame
pygame.init()

#criando a tela do jogo
tela = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
tela.fill((0,0,0))

#criando título e ícone
pygame.display.set_caption("Double Ninjas: Uma Missão Quase Possível")
icon = pygame.image.load("ying yang.png")
pygame.display.set_icon(icon)

#musica de fundo
mixer.music.load('trilha sonora.mp3')
mixer.music.play()

fonte = pygame.font.SysFont(None, 20)

def texto(texto, fonte, cor, superficie, x, y):
    textobj = fonte.render(texto, 1, cor)
    textoret = textobj.get_rect()
    superficie.blit(textobj, textoret)



def jogo():
    rodar = True
    while rodar:
        texto("Jogar", fonte, (255,255,255), tela, 50, 50)
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    rodar = False
        
        pygame.display.update()
        pygame.time.Clock().tick(60)

def opcoes():
    rodar = True
    while rodar:
        texto("Opções", fonte, (255,255,255), tela, 50, 50)
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    rodar = False
        pygame.display.update()
        pygame.time.Clock().tick(60)
        
def menu():
    while True:
        tela.fill((0,0,0))
        texto("Menu", fonte, (255,255,255), tela, 50, 50)

        mx, my = pygame.mouse.get_pos()

        botao1 = pygame.Rect(1500, 350, 200, 100)
        botao2 = pygame.Rect(280, 350, 200, 100)
        if botao1.collidepoint((mx, my)):
            if click:
                jogo()
        if botao2.collidepoint((mx, my)):
            if click:
                opcoes()

        pygame.draw.rect(tela, (51,25,0), botao1)
        pygame.draw.rect(tela, (51,25,0), botao2)

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit
            if evento.type == MOUSEBUTTONDOWN:
                if evento.button == 1:
                    click = True
        Background.__init__("fundo2.png", [0,0])
        
        pygame.display.update()
        pygame.time.Clock().tick(60)
    
class Background(pygame.sprite.Sprite):
    def __init__(self, imagem, coordenadas):
        pygame.sprite.Sprite.__init__(self)
        self.imagem = pygame.image.load(imagem)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = coordenadas

menu()
