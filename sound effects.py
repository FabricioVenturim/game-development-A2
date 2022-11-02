import pygame
from time import sleep
from pygame import mixer 

#para começar o pygame
pygame.init()

#criando a tela do jogo
tela = pygame.display.set_mode((1920, 1080))
fundo = pygame.image.load("fundo.jpg")
tela.fill((0,0,0))
tela.blit(fundo, (0, 0))

#musica de fundo
mixer.music.load('trilha sonora.mp3')
mixer.music.play()

sleep(10)