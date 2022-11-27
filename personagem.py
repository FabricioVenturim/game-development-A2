import pygame
from pygame.locals import *


class Personagem(pygame.sprite.Sprite):
    # Define estados possíveis do jogador
    # parado = 0 
    # pulando = 1
    # caindo = 2

    # Define a aceleração da gravidade
    gravidade = 2
    # Define a velocidade inicial no pulo
    aceleracao_pulo_inicial = 30

    def __init__(self, x, y, img, dict_animacoes):
        pygame.sprite.Sprite.__init__(self)
        self.aceleracao = self.aceleracao_pulo_inicial
        self.__state = 2
        
        sprite_sheet = pygame.image.load(img).convert_alpha()
        self.imagens_ninja = []
        
        for posicao in dict_animacoes.values():
            self.corta_sprite(sprite_sheet, posicao[0], posicao[1], posicao[2], posicao[3], posicao[4]) 

        self.__index_lista = 0
        self.image = self.imagens_ninja[self.index_lista]
        self.__rect = self.image.get_rect()
        self.__rect.x = x
        self.__rect.y = y

        self.__direita = True
        self.__correr = False
        self.__planar = False

    @property
    def index_lista(self):
        return self.__index_lista

    @index_lista.setter
    def index_lista(self, value):
        self.__index_lista = value

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, value):
        self.__rect = value

    @property
    def state(self):
        return self.__state
    
    @state.setter
    def state(self, state):
        self.__state = state

    @property
    def direita(self):
        return self.__direita

    @direita.setter
    def direita(self, value):
        self.__direita = value

    @property
    def correr(self):
        return self.__correr

    @correr.setter
    def correr(self, value):
        self.__correr = value

    @property
    def planar(self):
        return self.__planar

    @planar.setter
    def planar(self, value):
        self.__planar = value

    def corta_sprite(self,sprite_sheet, posicao_inicial, largura, altura, quantidade, redirecionamento):        
        for i in range(0, quantidade):
            largura_inicial = posicao_inicial
            img = sprite_sheet.subsurface((largura_inicial + i*largura,0), (largura,altura))
            img = pygame.transform.scale(img, (largura/redirecionamento, altura/redirecionamento))
            self.imagens_ninja.append(img)
    
    def parado_animacao(self):
        if self.index_lista > 9:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image= self.imagens_ninja[int(self.index_lista)]
        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image= pygame.transform.flip(self.image, True, False)


    def fun_correr_direita(self): 
        self.direita = True
        self.correr = True
        if self.index_lista < 10:
            self.index_lista = 10
        if self.state == 1 or self.planar:
            self.rect.x += 9
        else:
            self.rect.x += 6
    
    def fun_correr_esquerda(self):
        self.direita = False
        self.correr = True
        if self.index_lista < 10:
            self.index_lista = 10
        if self.state == 1 or self.planar:
            self.rect.x -= 9
        else:
            self.rect.x -= 6

    def correr_animacao(self):
        if self.index_lista > 19:   
            self.index_lista = 10
        self.index_lista += 0.25
        self.image= self.imagens_ninja[int(self.index_lista)]
        
        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image= pygame.transform.flip(self.image, True, False)
        self.correr = False
        
    def fun_cair(self):
        self.correr = False
        self.planar = False
        self.state = 2

    def cair(self):
        self.rect.y += self.aceleracao
        self.aceleracao += self.gravidade
        self.index_lista = 24
        self.image = self.imagens_ninja[int(self.index_lista)]
        if self.direita == False:
            self.image= pygame.transform.flip(self.image, True, False)

        # Aceleração máxima
        if self.aceleracao > 18:
            self.aceleracao = 18

    def fun_pular(self):
        self.correr = False
        self.state = 1
        if self.index_lista < 20:
            self.index_lista = 20

    def pular_animacao(self):
        ####### animação #######
        if self.index_lista > 29:   
            self.index_lista = 20
        self.index_lista += 0.25
        self.image = self.imagens_ninja[int(self.index_lista)]
        
        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image = pygame.transform.flip(self.image, True, False)
        self.correr = False

        # Atualiza o estado para caindo
        if self.aceleracao < 0:
            self.state = 2
        
        if self.state == 1: 
            self.rect.y -= self.aceleracao
            self.aceleracao -= self.gravidade
        
        if self.state == 2: 
            self.rect.y += self.aceleracao
            self.aceleracao += self.gravidade
            

class BoyNinja(Personagem):
    def __init__(self, x, y, img, dict_animacoes):
        super().__init__(x, y, img, dict_animacoes)
        self.__bater = False

    @property
    def bater(self):
        return self.__bater

    @bater.setter
    def bater(self, value):
        self.__bater = value

    def fun_bater(self):
        self.bater = True
        self.correr = False
        if self.index_lista < 30:
            self.index_lista = 30

    def bater_animacao(self):
        #Deixar a animação mais suave
        if self.index_lista == 30:
            if self.direita:
                self.rect.x -= 15 
            else:
                self.rect.x -= 80 

        if self.index_lista > 39: 
            self.index_lista = 0
            self.bater = False
            # Voltar para o local inicial
            if self.direita:
                self.rect.x += 15
            else:
                self.rect.x += 80

        self.index_lista += 0.25
        self.image = self.imagens_ninja[int(self.index_lista)]
        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image = pygame.transform.flip(self.image, True, False)
       

    def fun_planar(self):
        self.correr = False
        self.planar = True
        self.state = 2
        if self.index_lista < 40:
            self.index_lista = 40
 

    def planar_animacao(self):
        if self.index_lista > 49:   
            self.index_lista = 40
        self.index_lista += 0.5
        self.image = self.imagens_ninja[int(self.index_lista)]

        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image = pygame.transform.flip(self.image, True, False)
        # Atualiza o estado para caindo

        self.aceleracao = 3
        self.rect.y += self.aceleracao
    

    def update(self):
        if self.state == 0:
            self.aceleracao = self.aceleracao_pulo_inicial
            self.planar = False
        
        if self.state == 2 and self.planar == False:
            self.cair()
        # Controle de animação do personagem para correr
        elif self.correr and self.state != 1 and self.planar == False:
            self.correr_animacao()
        # Controle de animação do personagem para pular
        elif self.state == 1:
            self.pular_animacao()
        # Controle de animação do personagem para bater
        elif self.bater and self.state != 1:
            self.bater_animacao()
        # Controle de animação do personagem para planar
        elif self.planar:
            self.planar_animacao()
        # Controle de animação do personagem para parado
        else: 
            self.parado_animacao()
            
class GirlNinja(Personagem):
    def __init__(self, x, y, img, dict_animacoes, screen):
        super().__init__(x, y, img, dict_animacoes)
        self.screen = screen
        self.__deslizar = False
        self.__atirar = False
        self.kunai = Kunai(self.screen)
    
    @property
    def deslizar(self):
        return self.__deslizar
    
    @deslizar.setter
    def deslizar(self, value):
        self.__deslizar = value
    
    @property
    def atirar(self):
        return self.__atirar
    
    @atirar.setter
    def atirar(self, value):
        self.__atirar = value

    def fun_deslizar(self):
        self.deslizar = True
        self.correr = False
        self.rect.y += 37

        if self.index_lista < 30:
            self.index_lista = 30
        if self.direita == False:
            self.rect.x -= 7.5
        else:
            self.rect.x += 7.5

    def deslizar_animacao(self):
        if self.index_lista > 39:   
            self.index_lista = 30
        self.index_lista += 0.25
        self.image = self.imagens_ninja[int(self.index_lista)]

        # vira a imagem se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image = pygame.transform.flip(self.image, True, False)
        self.deslizar = False
        self.rect.y -= 37

    def fun_atirar(self):
        self.atirar = True
        self.correr = False

        if self.index_lista < 40:
            self.index_lista = 40
            
    def atirar_animacao(self):
        if self.index_lista > 49:   
            self.index_lista = 40
            self.atirar = False

        if self.index_lista == 43:
            self.kunai.fun_atirar(self.rect.x, self.rect.y, self.direita) 

        self.index_lista += 0.25
        self.image = self.imagens_ninja[int(self.index_lista)]

        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        # Atualiza a posição do kunai
        self.kunai.update()

        # Atualiza o estado quando caindo 
        if self.state == 0:
            self.aceleracao = self.aceleracao_pulo_inicial
            self.planar = False
        
        # controle de animação do personagem para cair
        if self.state == 2:
            self.cair()
        # controle de animação do personagem para deslizar
        elif self.deslizar:
            self.deslizar_animacao()
        # Controle de animação do personagem para correr
        elif self.correr and self.state != 1:
            self.correr_animacao()
        # Controle de animação do personagem para pular
        elif self.state == 1:
            self.pular_animacao()
        # Controle de animação do personagem para atirar
        elif self.atirar:
            self.atirar_animacao()
        # Controle de animação do personagem para parado
        else: 
            self.parado_animacao()


class Robo(Personagem):
    temporizador = 0

    def __init__(self, x, x_distancia, y, campo_de_visao, img, dict_animacoes, movimentacao = True, direita_movimentacao = True):
        """_summary_: Classe que representa o Robo 

        :param x: posição x do robo
        :type x: int
        :param x_distancia: distancia que o robo irá se mover
        :type x_distancia: int   
        :param y: posição y do robo
        :type y: int
        :param campo_de_visao: distancia que o robo irá ver o personagem
        :type campo_de_visao: int
        :param img: imagem do robo
        :type img: str
        :param dict_animacoes: dicionario com as animações do robo
        :type dict_animacoes: dict
        :param movimentacao: Se o robô irá se mover ou ficará parado, defaults to True
        :type movimentacao: bool, optional
        :param direita_movimentacao: Qual direção o robô irá se mover de acordo com a posição inicial, defaults to True
        :type direita_movimentacao: bool, optional
        """        
        super().__init__(x, y, img, dict_animacoes)
        self.__x = x
        self.__campo_de_visao = campo_de_visao
        self.__x_distancia = x_distancia
        if direita_movimentacao:
            self.direita = False
        self.__vivo = True
        self.__movimentacao = movimentacao

    @property
    def campo_de_visao(self):
        return self.__campo_de_visao
    
    @campo_de_visao.setter
    def campo_de_visao(self, value):
        self.__campo_de_visao = value

    @property
    def x(self):
        return self.__x
    
    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def x_distancia(self):
        return self.__x_distancia

    @x_distancia.setter
    def x_distancia(self, value):
        self.__x_distancia = value
    
    @property
    def movimentacao(self):
        return self.__movimentacao

    @movimentacao.setter
    def movimentacao(self, value):
        self.__movimentacao = value
    
    @property
    def vivo(self):
        return self.__vivo
    
    @vivo.setter
    def vivo(self, value):
        self.__vivo = value
    
    def fun_morrer(self):
        self.vivo = False
        if self.index_lista < 18:
            self.index_lista = 18

    def correr_animacao(self):
        if self.index_lista > 17:   
            self.index_lista = 10
        self.index_lista += 0.25
        self.image= self.imagens_ninja[int(self.index_lista)]
        
        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image= pygame.transform.flip(self.image, True, False)
        self.correr = False
    
    def verifica_player(self, player):
        if self.direita:     # verifica se o player está no campo de visão x        # verifica se o player está no campo de visão y
            if self.rect.x < player.rect.x < self.rect.x + self.campo_de_visao and self.rect.y - 50 <= player.rect.y <= self.rect.y + 50:
                self.correr = False
                print("DIREITAA campo de visão")

        else: # verifica se o player está no campo de visão x        # verifica se o player está no campo de visão y
            if self.rect.x > player.rect.x > self.rect.x - self.campo_de_visao and self.rect.y - 50 <= player.rect.y <= self.rect.y + 50:
                self.correr = False
                print("ESQUERDA campo de visão") 

    def animacao_morrer(self):
        if self.index_lista == 24: # quando a colisão tiver certa, aí isso vai sair
            self.rect.y += 10
        if self.index_lista > 27:   
            self.index_lista = 27
        self.index_lista += 0.25
        self.image= self.imagens_ninja[int(self.index_lista)]
        
        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image= pygame.transform.flip(self.image, True, False)
        self.correr = False

    def update(self):
        if self.state == 2:
            self.cair()

        if self.vivo == False:
            self.animacao_morrer()
        
        # Controle de animação do personagem para correr
        elif self.movimentacao:
            if self.temporizador == 300:
                self.direita = not self.direita
            elif self.temporizador > 300:
                self.correr_animacao()
                if self.direita:
                    self.fun_correr_direita()
                    if self.rect.x >= self.x + self.x_distancia:
                        self.rect.x = self.x + self.x_distancia
                        self.x = self.x + self.x_distancia
                        self.temporizador = 0
                else:
                    self.fun_correr_esquerda()
                    if self.rect.x <= self.x - self.x_distancia:
                        self.rect.x = self.x - self.x_distancia
                        self.x = self.x - self.x_distancia
                        self.temporizador = 0
            else: 
                self.parado_animacao()
            self.temporizador += 1
        else:
            self.parado_animacao()

        

class Kunai(pygame.sprite.Sprite):
    gravidade = 1.5
    aceleracao_inicial = 25

    def __init__(self, screen):       
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        image = pygame.image.load("img/Kunai.png").convert_alpha()
        self.__image = pygame.transform.scale(image, (160/2.4, 32/2.4)) #redimensiona a imagem para o tamanho desejado
        self.__rect = self.image.get_rect()
        self.__aceleracao = self.aceleracao_inicial
        self.__direita = True
        self.__atirar = False

    @property
    def image(self):
        return self.__image
    
    @image.setter
    def image(self, value):
        self.__image = value
    
    @property
    def rect(self):
        return self.__rect
    
    @rect.setter
    def rect(self, value):
        self.__rect = value
    
    @property
    def aceleracao(self):
        return self.__aceleracao
    
    @aceleracao.setter
    def aceleracao(self, value):
        self.__aceleracao = value
    
    @property
    def direita(self):
        return self.__direita
    
    @direita.setter
    def direita(self, value):
        self.__direita = value
    
    @property
    def atirar(self):
        return self.__atirar
    
    @atirar.setter
    def atirar(self, value):
        self.__atirar = value

    def fun_atirar(self, x, y, bool_direita):
        self.atirar = True
        self.direita = bool_direita
        if self.direita:
            self.rect.midbottom = (x + 100, y) #posiciona o kunai na frente do personagem
        else:
            self.rect.midbottom = (x, y)

    def trajetoria(self):
        if self.direita:
            self.rect.x += 15
        else:
            self.rect.x -= 15

        self.rect.y -= self.aceleracao
        self.aceleracao -= self.gravidade

        if self.direita:
            self.screen.blit(self.image, self.rect)
        else:
            self.screen.blit(pygame.transform.flip(self.image, True, False), self.rect)

    def update(self):
        if self.atirar:
            self.trajetoria()
        else:
            self.aceleracao = self.aceleracao_inicial