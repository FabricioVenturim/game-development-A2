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

            #aparecendo o texto de teclar para começar
            botao_jogar = Botao("CONTROLES", 300, 120, ( self.tela.get_width()*2.2/12, self.tela.get_height()*2/5), 0)
            botao_jogar.desenhar()
            if botao_jogar.clicado == True:
                self.tela_controles()
                #INTERFACE DA TELA DE OPÇÕES
                # BLA BLA BLA                

            self.mostrar_texto("PRESSIONE ESPAÇO PARA COMEÇAR", 36, (0,0,0), self.tela.get_width()*1/4, self.tela.get_height()*2.9/5)
            self.mostrar_texto("- Desenvolvido por Fabrício Venturin, Lucas Cuan, Pedro Thomaz Martins e Yonathan Rabinovici", 18, (255, 255, 255), self.tela.get_width()/5.5, self.tela.get_height()*9.7/10)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return
                if evento.type == pygame.KEYUP and evento.key == K_ESCAPE:
                    self.rodar = False
                    pygame.quit()
                    sys.exit
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
                pass

    #criando uma função para a tela de controles
    def tela_controles(self):

        transicao = pygame.Surface((0,0), pygame.FULLSCREEN)
        transicao.fill((0,0,0))
        for i in range (0, 300):
            transicao.set_alpha(i)
            self.tela.fill((105, 81, 31))

            #comando de opcoes bla bla bla
            #aparece a interface com os controles

            self.tela.blit(transicao, (0,0))
            botao_w = Botao("W", 75,75, (200,200), 5)
            botao_w.desenhar()
            botao_a = Botao("A", 75,75, (250,100), 5)
            botao_a.desenhar()
            botao_s = Botao("D", 75,75, (300,200), 5)
            botao_s.desenhar()

            #comando de tempo com a interface aberta
            pygame.time.delay(10000)
            boy_ninja = pygame.image.load("img/player_1/Idle__000.png")
            girl_ninja = pygame.image.load("img/player_2/Idle__000.png")
            self.tela.blit(boy_ninja, (self.tela.get_width()*2/5,self.tela.get_height()*5/6))
            self.tela.blit(girl_ninja,(self.tela.get_width()*4/5,self.tela.get_height()*5/6))
            pygame.display.update()


class Botao:
    def __init__ (self, texto, x, y, posicao, elevacao):
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
        self.texto_sup = Interface().fonte.render(texto, True, (255,255,255))
        self.texto_ret = self.texto_sup.get_rect(center = self.topo_ret.center)
        
    def desenhar(self):
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
