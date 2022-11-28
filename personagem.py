import pygame
from pygame.locals import *


class Personagem(pygame.sprite.Sprite):
    """Objeto com funções básicas de todos os personagens

    :param x: Posição x do personagem
    :type x: int or float
    :param y: Posição y do personagem
    :type y: int or float
    :param img: Caminho da imagem do personagem
    :type img: str
    :param dict_animacoes: Dicionário com as posições de cada animação
    :type dict_animacoes: dict
    """    

    # Define estados possíveis do jogador
    # parado = 0 
    # pulando = 1
    # caindo = 2

    # Define a aceleração da gravidade
    gravidade = 2
    # Define a velocidade inicial no pulo
    aceleracao_pulo_inicial = 30

    def __init__(self, x:int, y:int, img:str, dict_animacoes:dict):
        """Funções construtoras do objeto

        :param x: Posição x do personagem
        :type x: int or float
        :param y: Posição y do personagem
        :type y: int or float
        :param img: Caminho da imagem do personagem
        :type img: str
        :param dict_animacoes: Dicionário com as posições de cada animação
        :type dict_animacoes: dict
        """        
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

    def corta_sprite(self,sprite_sheet:str, posicao_inicial:float, largura:float, altura:float, quantidade:int, redirecionamento:float):
        """Função que corta a sprite sheet e adiciona as imagens em uma lista

        :param sprite_sheet: Caminho da imagem do personagem
        :type sprite_sheet: str
        :param posicao_inicial: Posição inicial da sprite sheet
        :type posicao_inicial: float
        :param largura: Largura da imagem
        :type largura: float
        :param altura: Altura da imagem
        :type altura: float
        :param quantidade: Quantidade de imagens
        :type quantidade: int
        :param redirecionamento: Redirecionamento da imagem
        :type redirecionamento: float
        """                
        for i in range(0, quantidade):
            largura_inicial = posicao_inicial
            img = sprite_sheet.subsurface((largura_inicial + i*largura,0), (largura,altura))
            img = pygame.transform.scale(img, (largura/redirecionamento, altura/redirecionamento))
            self.imagens_ninja.append(img)
    
    def parado_animacao(self):
        """_summary_: Função que define a animação do personagem quando parado
        """        
        if self.index_lista > 9:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image= self.imagens_ninja[int(self.index_lista)]
        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image= pygame.transform.flip(self.image, True, False)


    def fun_correr_direita(self): 
        """_summary_: Função que muda a posição do personagem correndo para a direita
        """        
        self.direita = True
        self.correr = True
        if self.index_lista < 10:
            self.index_lista = 10
        if self.state == 1 or self.planar:
            self.rect.x += 9
        else:
            self.rect.x += 6
    
    def fun_correr_esquerda(self):
        """_summary_: Função que muda a posição do personagem correndo para a esquerda
        """        
        self.direita = False
        self.correr = True
        if self.index_lista < 10:
            self.index_lista = 10
        if self.state == 1 or self.planar:
            self.rect.x -= 9
        else:
            self.rect.x -= 6

    def correr_animacao(self):
        """_summary_: Função que define a animação do personagem quando correndo
        """        
        if self.index_lista > 19:   
            self.index_lista = 10
        self.index_lista += 0.25
        self.image= self.imagens_ninja[int(self.index_lista)]
        
        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image= pygame.transform.flip(self.image, True, False)
        self.correr = False
        
    def fun_cair(self):
        """_summary_: Função que muda a posição do personagem caindo
        """        
        self.correr = False
        self.planar = False
        self.state = 2

    def cair(self):
        """_summary_: Função que define a animação do personagem quando caindo
        """        
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
        """_summary_: Função que muda a posição do personagem pulando
        """        
        self.correr = False
        self.state = 1
        if self.index_lista < 20:
            self.index_lista = 20

    def pular_animacao(self):
        """_summary_: Função que define a animação do personagem quando pulando
        """        
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
    """_summary_: Classe que define o personagem ninja menino

    :param x: Posição x do personagem
    :type x: int or float
    :param y: Posição y do personagem
    :type y: int or float
    :param img: Caminho da imagem do personagem
    :type img: str
    :param dict_animacoes: Dicionário com as posições de cada animação
    :type dict_animacoes: dict
    """    
    def __init__(self, x, y, img, dict_animacoes):
        """_summary_: Construtor da classe

        :param x: Posição x do personagem
        :type x: int or float
        :param y: Posição y do personagem
        :type y: int or float
        :param img: Caminho da imagem do personagem
        :type img: str
        :param dict_animacoes: Dicionário com as posições de cada animação
        :type dict_animacoes: dict
        """        
        super().__init__(x, y, img, dict_animacoes)
        self.__bater = False

    @property
    def bater(self):
        return self.__bater

    @bater.setter
    def bater(self, value):
        self.__bater = value

    def fun_bater(self):
        """_summary_: Função que ativa o personagem batendo
        """        
        self.bater = True
        self.correr = False
        if self.index_lista < 30:
            self.index_lista = 30

    def bater_animacao(self):
        """_summary_: Função que define a animação do personagem quando bate
        """        
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
        """_summary_: Função que ativa a planagem do personagem
        """        
        self.correr = False
        self.planar = True
        self.state = 2
        if self.index_lista < 40:
            self.index_lista = 40
 

    def planar_animacao(self):
        """_summary_: Função que define a animação do personagem quando plana
        """        
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
        """_summary_: Função que atualiza a posição do personagem
        """        
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
    """_summary_: Classe que define o personagem ninja menina

        :param x: Posição x do personagem
        :type x: int or float
        :param y: Posição y do personagem
        :type y: int or float
        :param img: Caminho da imagem do personagem
        :type img: str
        :param dict_animacoes: Dicionário com as posições de cada animação
        :type dict_animacoes: dict
        """   
    def __init__(self, x, y, img, dict_animacoes, screen):
        """_summary_: Construtor da classe

        :param x: Posição x do personagem
        :type x: int or float
        :param y: Posição y do personagem
        :type y: int or float
        :param img: Caminho da imagem do personagem
        :type img: str
        :param dict_animacoes: Dicionário com as posições de cada animação
        :type dict_animacoes: dict
        """   
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
        """_summary_: Função que ativa o personagem deslizando
        """        
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
        """_summary_: Função que define a animação do personagem quando desliza
        """        
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
        """_summary_: Função que ativa o personagem atirando
        """        
        self.atirar = True
        self.correr = False

        if self.index_lista < 40:
            self.index_lista = 40
            
    def atirar_animacao(self):
        """_summary_: Função que define a animação do personagem quando atira
        """        
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
        """_summary_: Função que atualiza a posição do personagem
        """        
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
    temporizador = 0

    def __init__(self, x:int, x_distancia:int, y:int, campo_de_visao:int, img:str, dict_animacoes:dict, movimentacao: bool = True, direita_movimentacao: bool = True):
        """_summary_: Construtor da classe Robo

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
        """_summary_: Função que faz a animação do robo morrer
        """        
        self.vivo = False
        if self.index_lista < 18:
            self.index_lista = 18

    def correr_animacao(self):
        """_summary_: Função que faz a animação do robo correr
        """        
        if self.index_lista > 17:   
            self.index_lista = 10
        self.index_lista += 0.25
        self.image= self.imagens_ninja[int(self.index_lista)]
        
        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image= pygame.transform.flip(self.image, True, False)
        self.correr = False
    
    def verifica_player(self, player: object):
        """_summary_: Função que verifica se o player está dentro do campo de visão do robo

        :param player: Objeto do tipo Personagem
        :type player: object
        """        
        if self.direita:     # verifica se o player está no campo de visão x        # verifica se o player está no campo de visão y
            if self.rect.x < player.rect.x < self.rect.x + self.campo_de_visao and self.rect.y - 50 <= player.rect.y <= self.rect.y + 50:
                self.correr = False
                print("DIREITAA campo de visão")

        else: # verifica se o player está no campo de visão x        # verifica se o player está no campo de visão y
            if self.rect.x > player.rect.x > self.rect.x - self.campo_de_visao and self.rect.y - 50 <= player.rect.y <= self.rect.y + 50:
                self.correr = False
                print("ESQUERDA campo de visão") 

    def animacao_morrer(self):
        """_summary_: Função que faz a animação do robo morrer
        """        
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
        """_summary_: Função que atualiza a posição do robo
        """        
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
    """_summary_ : Classe que cria os objetos Kunai

    :param screen: tela do jogo que será exibido os objetos
    :type screen: str
    """    
    gravidade = 1.5
    aceleracao_inicial = 25

    def __init__(self, screen:str):  
        """_summary_: Função que inicializa os objetos Kunai

        :param screen: tela do jogo que será exibido os objetos
        :type screen: str
        """             
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

    def fun_atirar(self, x:int, y:int, bool_direita:bool):
        """_summary_: Função que faz o objeto Kunai atirar

        :param x: posição x do objeto
        :type x: int
        :param y: posição y do objeto
        :type y: int
        :param bool_direita: variável que verifica se o objeto está olhando para a direita
        :type bool_direita: bool
        """        
        self.atirar = True
        self.direita = bool_direita
        if self.direita:
            self.rect.midbottom = (x + 100, y) #posiciona o kunai na frente do personagem
        else:
            self.rect.midbottom = (x, y)

    def trajetoria(self):
        """_summary_: Função que faz o objeto Kunai seguir uma trajetória
        """        
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
        """_summary_: Função que atualiza a posição do objeto Kunai
        """        
        if self.atirar:
            self.trajetoria()
        else:
            self.aceleracao = self.aceleracao_inicial