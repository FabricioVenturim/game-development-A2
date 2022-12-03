import pygame
from pygame.locals import *
import sys

#criando a classe interface
class Interface:
    def __init__(self):

        #definindo as propriedades iniciais, além de iniciar algumas ações
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        #definindo nome e icon
        pygame.display.set_caption("Double Ninjas: Uma Missão Quase Possível")
        icon = pygame.image.load("img/ying yang.png")
        pygame.display.set_icon(icon)

        #definindo as propriedades da tela
        self.tela = pygame.display.set_mode((0,0), pygame.RESIZABLE)
        self.fonte = pygame.font.SysFont("Arial", 36)
        self.tempo = pygame.time.Clock()
        self.rodando = True

        #aplicando o fundo
        logo = pygame.image.load("img/logo.png")
        logo = pygame.transform.scale(logo,(960,600))
        fundo = pygame.image.load("img/fundo2.jpg")
        #definindo as posições para que sejam as mais responsivas de acordo com o hardware
        fundo = pygame.transform.scale(fundo,(self.tela.get_width(),self.tela.get_height()))
        self.tela.blits([(fundo,(0,0)), (logo, (self.tela.get_width()/15, self.tela.get_height()/100))])

#função da interface da fase
    def rodar(self):
        self.jogando = True
        while self.jogando:
            self.tempo.tick(60)
            self.eventos()

    #possibilitando que as pessoas fechem o jogo 
    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                if self.jogando:
                    self.jogando = False
                self.rodando = False

    #criando uma função para o texto
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

            #aparecendo o texto de teclar para começar
            botao_jogar = Botao("CONTROLES", 300, 120, (self.tela.get_width()*2.1/12, self.tela.get_height()*3/5), 0, self.fonte)
            botao_jogar.desenhar(self.tela)
            if botao_jogar.clicado == True:
                self.tela_controles()
                #INTERFACE DA TELA DE OPÇÕES
                # BLA BLA BLA                
            try:
                self.mostrar_texto("PRESSIONE ESPAÇO PARA COMEÇAR", 36, (0,0,0), self.tela.get_width()*1/4, self.tela.get_height()*3.75/5)
                self.mostrar_texto("- Desenvolvido por Fabrício Venturin, Lucas Cuan, Pedro Thomaz Martins e Yonathan Rabinovici", 20, (255, 255, 255), self.tela.get_width()/3.8, self.tela.get_height()*9.3/10)

            except:
                print("o usuário saiu pelo X da tela de controles")
                sys.exit()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodar = False
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.KEYUP and evento.key == K_ESCAPE:
                    self.rodar = False
                    pygame.quit()
       
                  
                if evento.type == pygame.KEYUP and evento.key == K_SPACE:
                    esperando = False
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound("audio/trilha sonora.mp3").play()
                    self.rodar()
            try:
                pygame.display.update()
            except:
                print("Saiu do Jogo")
                break

    #criando uma função para a tela de controles
    def tela_controles(self):
        rodar = True
        while rodar:
            transicao = pygame.Surface((0,0), pygame.FULLSCREEN)
            transicao.fill((0,0,0))
            controles = pygame.image.load("img/Controles.png")
            controles = pygame.transform.scale(controles, (self.tela.get_width(),self.tela.get_height()))
            self.tela.blit(controles, (0,0))

            try:
                for evento in pygame.event.get():
                    #criando o botão para voltar da interface de controles
                    voltar = Botao("VOLTAR",200,100,(15,15), 3, self.fonte)
                    voltar.desenhar(self.tela)
                    pygame.display.update()

                    #garantindo que quando clicado a imagem suma
                    if voltar.clicado == True:
                        controles.fill(0,0,0)
                        pygame.display.update()
                        break

                    #possibilitando o fechamento do jogo
                    if evento.type == pygame.QUIT:
                        self.jogando = False
                        self.rodando = False
                        pygame.quit()
                        sys.exit()

                    #definindo ESC para sair do jogos
                    if evento.type == KEYUP and evento.key == K_ESCAPE:
                        rodar = False
                        pygame.quit()
                        sys.exit()
                
            #tratando a exceção de quando alguém sair na tela de controles
            except Exception:
                print("o usuário saiu da tela de controles")
                break

        #colocando de volta a imagem certa
        rodar = False
        fundo = pygame.image.load("img/fundo2.jpg")
        controles = pygame.transform.scale(fundo,(2112,1188))
        logo = pygame.image.load("img/logo.png")
        logo = pygame.transform.scale(logo,(960,600))
        self.tela.blits([(controles, (0,0)),(logo, (self.tela.get_width()/15, self.tela.get_height()/100))])
        

#criando uma classe para botão
class Botao:
    def __init__ (self, texto, x, y, posicao, elevacao, fonte):
        #determinando as propriedades do botao como posicao e cor
        self.pressionado = False
        self.elevacao = elevacao
        self.elevacao_dinamica = elevacao
        self.original_posicao_y = posicao[1]
        self.clicado = False

        #retangulo de cima do botao
        self.topo_ret = pygame.Rect(posicao, (x, y))
        self.topo_cor = (105, 81, 31)

        #retangulo de baixo
        self.baixo_ret = pygame.Rect(posicao, (x, y))
        self.baixo_cor = (56, 43, 16)

        #o texto do botao
        self.texto_sup = fonte.render(texto, True, (255,255,255))
        self.texto_ret = self.texto_sup.get_rect(center = self.topo_ret.center)
        
    #função para gerar o botão
    def desenhar(self, tela):
        pos = pygame.mouse.get_pos()
        if self.topo_ret.collidepoint(pos):
            self.topo_cor = (227, 53, 41)
            if pygame.mouse.get_pressed()[0] and not self.clicado:
                self.clicado = True
            if not pygame.mouse.get_pressed()[0]:
                self.clicado = False

        #aplicando a elevacao no botao
        self.topo_ret.y = self.original_posicao_y - self.elevacao_dinamica
        self.texto_ret.center = self.topo_ret.center
        self.baixo_ret.midtop = self.topo_ret.midtop
        self.baixo_ret.height = self.topo_ret.height + self.elevacao_dinamica
        
        #aplicando as características do botão
        pygame.draw.rect(tela, self.baixo_cor, self.baixo_ret, border_radius=15)
        pygame.draw.rect(tela, self.topo_cor, self.topo_ret, border_radius=15)
        
        #para aparecer o elemento
        tela.blit(self.texto_sup, self.texto_ret)
    
    def pausa(self):
        Interface.mostrar_texto("PRESSIONE ESPAÇO PARA CONTINUAR", 20, (255,255,255), (Interface().tela.get_width/2.5), (Interface().tela.get_height/5))
        Interface.blit
        pausado = True
        while pausado:
            for evento in pygame.event.get():
                if evento.type == pygame.KEYUP and evento.key == K_SPACE:
                    pausado = False
                
                elif evento.type == pygame.KEYUP and evento.key == K_ESCAPE:
                    pygame.quit()
                    quit() 
        return

#rodando o jogo
jogo = Interface()
jogo.tela_start()