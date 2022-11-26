import pygame
from pygame.locals import *

class Interface:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        pygame.display.set_caption("Double Ninjas: Uma Missão Quase Possível")
        icon = pygame.image.load("img/ying yang.png")
        pygame.display.set_icon(icon)
        self.tela = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        self.fonte = pygame.font.SysFont("Arial", 36)
        self.tempo = pygame.time.Clock()
        self.rodando = True
        fundo = pygame.image.load("img/fundo2.jpg")
        fundo = pygame.transform.scale(fundo,(1920,1080))
        self.tela.blit(fundo,(0,0))

    def novo_jogo(self):
        self.todas_sprites = pygame.sprite.Group()
        self.rodar()

    def rodar(self):
        self.jogando = True
        while self.jogando:
            self.tempo.tick(60)
            self.eventos()
    
    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                if self.jogando:
                    self.jogando = False
                self.rodando = False


    def mostrar_texto(self, texto, tamanho, cor, x, y):
        fonte = pygame.font.SysFont("Arial", tamanho)
        texto = fonte.render(texto, True, cor)
        texto_ret = texto.get_rect()
        #para posicionar o texto de acordo com o centro
        texto_ret.midtop = (x, y)
        self.tela.blit(texto, texto_ret)

    def tela_start(self):
        pygame.mixer.music.load("audio/trilha sonora2.mp3")
        pygame.mixer.music.play()
        self.mostrar_texto(
            "- Pressione uma tecla para jogar", 
            45, 
            #(94, 66, 39),
            (255,255,255), 
            self.tela.get_width()/2, 
            self.tela.get_height()*4/5
            )
        self.mostrar_texto(
            "- Desenvolvido por Fabrício Venturin, Lucas Cuan, Pedro Thomaz Martins e Yonathan Rabinovici", 
            12, 
            (255, 255, 255), 
            self.tela.get_width()/2, 
            self.tela.get_height()/100
            )
        
        #para atualizar a tela enquanto aparece o texto
        pygame.display.flip()
        self.esperar()

    def esperar(self):
        esperando = True
        while esperando:
            self.tempo.tick(60)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    esperando = False
                    self.rodar = False
                if evento.type == pygame.KEYUP:
                    esperando = False
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound("audio/trilha sonora.mp3").play()

    def tela_quit(self):
        pygame.quit()
        pass

jogo = Interface()
jogo.tela_start()

while jogo.rodar:
    jogo.novo_jogo()
    jogo.tela_quit()