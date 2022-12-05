import pygame
from pygame.locals import *
import sys
from level import Level
import config

#criando a classe interface
class Interface:
    def __init__(self):
        """Função utilizada para iniciar a interface
        """

        #definindo as propriedades iniciais, além de iniciar algumas ações
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        #definindo nome e icon
        pygame.display.set_caption("Double Ninjas: Uma Missão Quase Possível")
        icon = pygame.image.load("img/ying yang.png")
        pygame.display.set_icon(icon)

        #definindo as propriedades da tela
        self.tela = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
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
        """Função utilizada para gerar rodar o jogo
        """
        pausa = Botao_Clicavel("II",75,75,(10,10),2, self.fonte)
        
        self.level_index = 0
        self.level = Level(config.level_data[self.level_index], self.tela)
        self.jogando = True
        
        while self.jogando:
            self.level.update()
            self.level.draw()

            if self.level.perdeu:
                self.tela_derrota()

            pausa.desenhar(self.tela)
            if pausa.clicado == True:
                self.tela_pausa()

            pygame.display.update()
            self.tempo.tick(60)
            self.eventos()

    #possibilitando que as pessoas fechem o jogo 
        """Função utilizada para promover os eventos básicos
        """
    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                if self.jogando:
                    self.jogando = False
                self.rodando = False

    #criando uma função para o texto
    def mostrar_texto(self, texto, tamanho, cor, x, y):
        """Função para aparecer o texto na interface

        :param texto: texto que aparece
        :type texto: str
        :param tamanho: número do tamanho da fonte
        :type tamanho: int
        :param cor: a cor da escrita em RGB
        :type cor: tuple
        :param x: a coordenada x da escrita
        :type x: float
        :param y: a coordenada y da escrita
        :type y: float
        """
        fonte = pygame.font.SysFont("Arial", tamanho)
        texto = fonte.render(texto, True, cor)
        texto_ret = texto.get_rect()

        #para posicionar o texto de acordo com o centro
        texto_ret.midtop = (x, y)
        self.tela.blit(texto, texto_ret)

    #começar a trilha sonora de inicio e iniciar a tela de esperar
    def tela_start(self):
        """Cria a interface inicial, com música e sala de espera
        """
        pygame.mixer.music.load("audio/trilha sonora2.mp3")
        pygame.mixer.music.play()
        pygame.display.flip()
        self.esperar()

#função da interface de espera
    def esperar(self):
        """Função da sala de espera, enquanto o jogador não inicia a fase
        """
        esperando = True
        while esperando:
            #criando um botão de pausa
            self.tempo.tick(60)

            #aparecendo o texto de teclar para começar
            botao_jogar = Botao_Clicavel("CONTROLES", 300, 120, (self.tela.get_width()*2.1/12, self.tela.get_height()*3/5), 0, self.fonte)
            botao_jogar.desenhar(self.tela)
            if botao_jogar.clicado == True:
                self.tela_controles()     

            #criando os textos da interface     
            try:
                self.mostrar_texto("PRESSIONE ESPAÇO PARA COMEÇAR", 36, (0,0,0), self.tela.get_width()*1/4, self.tela.get_height()*3.75/5)
                self.mostrar_texto("- Desenvolvido por Fabrício Venturin, Lucas Cuan, Pedro Thomaz Martins e Yonathan Rabinovici", 20, (255, 255, 255), self.tela.get_width()/3.8, self.tela.get_height()*9.3/10)

            #caso o processo de rodar da interface seja interrompido
            except:
                print("o usuário saiu pelo X da tela de controles")
                sys.exit()

            #permitindo a saída do usuário
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodar = False
                    pygame.quit()
                    sys.exit()

                #definindo a tecla de saída
                if evento.type == pygame.KEYUP and evento.key == K_ESCAPE:
                    self.rodar = False
                    pygame.quit()
       
                #defininido a tecla para COMEÇAR O JOGO -------------------------------- ATENCAO
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
            
            #criando um botão de pausa
            pausa = Botao_Clicavel("II",75,75,(10,10),2, self.fonte)
            pausa.desenhar(self.tela)

            #definindo a função do botão
            if pausa.clicado == True:
                self.tela_pausa()
                pygame.display.update()

    #criando uma função para a tela de controles
    def tela_controles(self):
        """
        Função utilizada para criar a tela que exibe controles
        """
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
                    voltar = Botao_Clicavel("VOLTAR",200,100,(15,15), 3, self.fonte)
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
        fundo = pygame.transform.scale(fundo,(self.tela.get_width(),self.tela.get_height()))
        logo = pygame.image.load("img/logo.png")
        logo = pygame.transform.scale(logo,(960,600))
        self.tela.blits([(fundo, (0,0)),(logo, (self.tela.get_width()/15, self.tela.get_height()/100))])

    #criando uma função para interface de pausa
    def tela_pausa(self):
        """
        Função para criar uma interface de pausado       
        """

        #definindo as funcionalidades
        pausado = True
        while pausado:
        
            #permitindo a saída do usuário
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if evento.type == pygame.KEYUP:

                    #definindo o Q para saída
                    if evento.key == K_q:
                        pausado = False

                    #definindo R para reiniciar o jogo
                    if evento.key == K_r:
                        pausado = False
                        self.definir_level(self.level_index)

                    #definindo o ESC para encerramento
                    elif evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
            
            #definindo as cores
            self.tela.fill((66, 47, 7))
            
            #criando um botão de controles para a interface de pausa
            controles = Botao_Clicavel("CONTROLES", 300, 120, (self.tela.get_width()*5/12, self.tela.get_height()*2.7/5), 0, self.fonte)
            controles.desenhar(self.tela)

            if controles.clicado == True:
                self.tela_controles()

            #texto que aparece na interface de pausa
            Interface.mostrar_texto(self, "PAUSADO", 150, (255,255,255), self.tela.get_width()/2, self.tela.get_height()*1/9)
            Interface.mostrar_texto(self, "PRESSIONE Q PARA CONTINUAR E R PARA REINICIAR", 36, (255,255,255), self.tela.get_width()/2, self.tela.get_height()*2.5/3)
            pygame.display.update()


        #caso pare de pausar, voltar ao normal
        pausado = False

        #imagem de fundo
        fundo = pygame.image.load("img/fundo2.jpg")
        fundo = pygame.transform.scale(fundo,(self.tela.get_width(),self.tela.get_height()))

        #logo do jogo
        logo = pygame.image.load("img/logo.png")
        logo = pygame.transform.scale(logo,(960,600))
        self.tela.blits([(fundo, (0,0)),(logo, (self.tela.get_width()/15, self.tela.get_height()/100))])

    #criando uma funcao para a tela de derrota do jogo
    def tela_derrota(self):
        self.tela.fill((66, 47, 7))
        self.mostrar_texto("DERROTA", 100, (0,0,0), self.tela.get_width()/2.3, self.tela.get_height()/9)
        reiniciar = Botao_Clicavel("TENTE NOVAMENTE", 300, 120, (self.tela.get_width()/2.3, self.tela.get_height()*3.5/5), 6, self.fonte)
        
        while self.jogando:
            reiniciar.desenhar(self.tela)

            if reiniciar.clicado == True:
                self.definir_level(self.level_index)
                return
            
            self.eventos()
            pygame.display.update()
            self.tempo.tick(60)
    
    def definir_level(self, level_index):
        self.level = Level(config.level_data[level_index], self.tela)
            
#criando uma classe para botão
class Botao_Clicavel:
    def __init__ (self, texto, comprimento, altura, posicao, elevacao, fonte):
        """Função utilizada para criar o botão e suas propriedades

        :param texto: texto do botão
        :type texto: str
        :param comprimento: comprimento do botão
        :type comprimento: float
        :param altura: altura do botão
        :type altura: float
        :param posicao: as coordenadas da tela que o botão aparece
        :type posicao: tuple
        :param elevacao: a elevação do botão
        :type elevacao: int
        :param fonte: a fonte das escrita do botão
        :type fonte: str
        """

        #determinando as propriedades do botao como posicao e cor
        self.pressionado = False

        #determinando a elevacao do botao
        self.elevacao = elevacao
        self.elevacao_dinamica = elevacao
        self.original_posicao_y = posicao[1]
        self.clicado = False

        #retangulo de cima do botao
        self.topo_ret = pygame.Rect(posicao, (comprimento, altura))
        self.topo_cor = (105, 81, 31)

        #retangulo de baixo
        self.baixo_ret = pygame.Rect(posicao, (comprimento, altura))
        self.baixo_cor = (56, 43, 16)

        #o texto do botao
        self.texto_sup = fonte.render(texto, True, (255,255,255))
        self.texto_ret = self.texto_sup.get_rect(center = self.topo_ret.center)

    #função para gerar o botão
    def desenhar(self, tela):
        """gerando o botão na interface da tela

        :param tela: a interface que o botão vai ser gerado
        :type tela: pygame.Surface
        """
        pos = pygame.mouse.get_pos()

        self.clicado = False
        #deixando o botao vermelho com o mouse em cima
        if self.topo_ret.collidepoint(pos):
            self.topo_cor = (227, 53, 41)
            self.clicado = pygame.mouse.get_pressed()[0]
        else:
            self.topo_cor = (105, 81, 31)

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

      
#rodando o jogo
jogo = Interface()
jogo.tela_start()
