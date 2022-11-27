import pygame
from pygame.locals import *
import sys

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
        fundo = pygame.transform.scale(fundo,(2112,1188))
        self.tela.blit(fundo,(0,0))

    def novo_jogo(self):
        self.todas_sprites = pygame.sprite.Group()
        self.rodar()
        pygame.display.update()
        pygame.time.Clock().tick(60)

#função da interface da fase
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

    #começar a trilha sonora de inicio e iniciar a tela de esperar
    def tela_start(self):
        pygame.mixer.music.load("audio/trilha sonora2.mp3")
        pygame.mixer.music.play()
        pygame.display.flip()
        self.esperar()

#função da interface de espera
    def esperar(self):
        esperando = True
        while esperando:
            #criando um botão de pausa
            self.tempo.tick(60)
            botao_pausa = Botao("||", 75, 75, (1, 1), 5)
            botao_pausa.desenhar()

            #aparecendo o texto de teclar para começar
            botao_jogar = Botao("Pressione uma tecla para jogar", 500, 120, ( self.tela.get_width()*1.2/3, self.tela.get_height()*3.5/5), 0)
            botao_jogar.desenhar()
            self.mostrar_texto("- Desenvolvido por Fabrício Venturin, Lucas Cuan, Pedro Thomaz Martins e Yonathan Rabinovici", 18, (255, 255, 255), self.tela.get_width()/5.5, self.tela.get_height()*9.7/10)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit 
                    esperando = False
                    self.rodar = False
                if evento.type == pygame.KEYUP:
                    esperando = False
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound("audio/trilha sonora.mp3").play()
                    self.rodar()
            pygame.display.update()
            

    def tela_quit(self):
        pygame.quit()
        pass

class Botao:
    def __init__ (self, texto, x, y, posicao, elevacao):
        #determinando as propriedades do botao como posicao e cor
        self.pressionado = False
        self.elevacao = elevacao
        self.elevacao_dinamica = elevacao
        self.original_posicao_y = posicao[1]

        #retangulo de cima do botao
        self.topo_ret = pygame.Rect(posicao, (x, y))
        self.topo_cor = (105, 81, 31)

        #retangulo de baixo
        self.baixo_ret = pygame.Rect(posicao, (x, y))
        self.baixo_cor = (56, 43, 16)

        #o texto do botao
        self.texto_sup = Interface().fonte.render(texto, True, (255,255,255))
        self.texto_ret = self.texto_sup.get_rect(center = self.topo_ret.center)
        
    def desenhar(self):
        #aplicando a elevacao no botao
        self.topo_ret.y = self.original_posicao_y - self.elevacao_dinamica
        self.texto_ret.center = self.topo_ret.center
        self.baixo_ret.midtop = self.topo_ret.midtop
        self.baixo_ret.height = self.topo_ret.height + self.elevacao_dinamica
        
        #definido a tela da interface
        tela = Interface().tela
        
        #aplicando as características do botão
        pygame.draw.rect(tela, self.baixo_cor, self.baixo_ret, border_radius=15)
        pygame.draw.rect(tela, self.topo_cor, self.topo_ret, border_radius=15)
        
        #para aparecer o elemento
        tela.blit(self.texto_sup, self.texto_ret)


jogo = Interface()
jogo.tela_start()

while jogo.rodar():
    jogo.novo_jogo()
    jogo.tela_quit()

#pygame.init()
#tela = pygame.display.set_mode((500,500))
#
#botao1 = Botao("Clique aqui", 200, 40, (200,250), 5)
#
#while True:
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            pygame.quit()
#            sys.exit 
#
#    tela.fill("#ffffff")
#    botao1.desenhar()
#    pygame.display.update()
#    pygame.time.Clock().tick(60)