import pygame
from pygame.locals import *
import math

ALTURA_BLC = 2
ALTURA_PULO_BLC = 3.2
GRAVIDADE_BLC = 0.02
VELOCIDADE_PULO_BLC = GRAVIDADE_BLC * \
    (math.sqrt(1 + 8 * ALTURA_PULO_BLC / GRAVIDADE_BLC) - 1) / 2
# Correr pra esquerda pode ser mais rápido devido a problemas de arredondamento
# Possível solução: manusear coordenadas próprias e depois atribuí-las ao rect
VELOCIDADE_BLC = 0.1
MOD_VELOCIDADE_CAINDO = 1.5
MOD_VELOCIDADE_DESLIZANDO = 1.25
VELOCIDADE_KUNAI_BLC = 0.2


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
    #gravidade = 2

    def __init__(self, x:int, y:int, tile_size:int, img:str, dict_animacoes:dict, collision_sprites:pygame.sprite.Group):
        """Funções construtoras do objeto

        :param x: Posição x do personagem
        :type x: int or float
        :param y: Posição y do personagem
        :param tile_size: Tamanho do tile
        :type tile_size: int
        :type y: int or float
        :param img: Caminho da imagem do personagem
        :type img: str
        :param dict_animacoes: Dicionário com as posições de cada animação
        :type dict_animacoes: dict
        :param collision_sprites: Grupo de sprites que o personagem pode colidir
        :type collision_sprites: pygame.sprite.Group
        """        

        pygame.sprite.Sprite.__init__(self)
        self.state = 2
        self.collision_sprites = collision_sprites

        self.tile_size = tile_size
        sprite_sheet = pygame.image.load(img).convert_alpha()
        self.imagens_ninja = []
        fator = tile_size * ALTURA_BLC / sprite_sheet.get_height()
        self.gravidade = tile_size * GRAVIDADE_BLC
        # Define a velocidade inicial no pulo
        self.aceleracao_pulo_inicial = tile_size * VELOCIDADE_PULO_BLC
        self.aceleracao = self.aceleracao_pulo_inicial


        self.velocidade = tile_size * VELOCIDADE_BLC
        self.velocidade_caindo = self.velocidade * MOD_VELOCIDADE_CAINDO


        for posicao in dict_animacoes.values():
            self.corta_sprite(
                sprite_sheet, posicao[0], posicao[1], posicao[2], posicao[3], fator)

        self.index_lista = 0
        self.image = self.imagens_ninja[self.index_lista]

        self.rect = self.image.get_rect(
            midbottom=(x + tile_size / 2, y + tile_size))

        self.direita = True
        self.correr = False
        self.mask = pygame.mask.from_surface(self.image)


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
            img = sprite_sheet.subsurface(
                (largura_inicial + i*largura, 0), (largura, altura))
            img = pygame.transform.scale(
                img, (largura * redirecionamento, altura * redirecionamento))
            self.imagens_ninja.append(img)

    def parado_animacao(self):
        """_summary_: Função que define a animação do personagem quando parado
        """        
        if self.index_lista > 9:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.imagens_ninja[int(self.index_lista)]
        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image = pygame.transform.flip(self.image, True, False)


    def fun_correr_direita(self): 
        """_summary_: Função que muda a posição do personagem correndo para a direita
        """      
        self.direita = True
        self.correr = True
        if self.index_lista < 10:
            self.index_lista = 10
        if self.state == 1:
            self.rect.x += self.velocidade_caindo
        else:
            self.rect.x += self.velocidade

    def fun_correr_esquerda(self):
        """_summary_: Função que muda a posição do personagem correndo para a esquerda
        """        
        self.direita = False
        self.correr = True
        if self.index_lista < 10:
            self.index_lista = 10
        if self.state == 1:
            self.rect.x -= self.velocidade_caindo
        else:
            self.rect.x -= self.velocidade

    def correr_animacao(self):
        """_summary_: Função que define a animação do personagem quando correndo
        """        
        if self.index_lista > 19:   

            self.index_lista = 10
        self.index_lista += 0.25
        self.image = self.imagens_ninja[int(self.index_lista)]

        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image = pygame.transform.flip(self.image, True, False)
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
        self.apply_gravity()
        self.index_lista = 24
        self.image = self.imagens_ninja[int(self.index_lista)]
        if self.direita == False:
            self.image = pygame.transform.flip(self.image, True, False)

    def apply_gravity(self):
        """_summary_: Função que define a gravidade do personagem
        """        
        self.aceleracao += self.gravidade
        self.rect.y += self.aceleracao

        # Aceleração máxima
        if self.aceleracao > 18:
            self.aceleracao = 18

    def fun_pular(self):
        """_summary_: Função que muda a posição do personagem pulando
        """        
        self.correr = False
        self.state = 1
        self.aceleracao = self.aceleracao_pulo_inicial
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
            self.rect.y -= self.aceleracao
            self.aceleracao += self.gravidade

    def check_horizontal_collisions(self, dimensao:float):
        """_summary_: Função que verifica as colisões horizontais do personagem

        :param dimensao: Dimensão do personagem
        :type dimensao: float
        """        
        rect_img = self.rect.copy()
        if self.direita:
            rect_img.x += self.tile_size/dimensao
        for sprite in self.collision_sprites.sprites():
            if rect_img.colliderect(sprite.rect):
                if self.direita:
                    self.rect.right = sprite.rect.left - self.tile_size/dimensao
                else:
                    self.rect.left = sprite.rect.right

    def check_vertical_collisions(self):
        """_summary_: Função que verifica as colisões verticais do personagem
        """        
        for sprite in self.collision_sprites.sprites():
            if self.rect.colliderect(sprite.rect):
                if self.state == 1:
                    self.rect.top = sprite.rect.bottom + 1
                    self.aceleracao = -1
                else:
                    self.rect.bottom = sprite.rect.top
                    self.aceleracao = 0
                    self.state = 0


class BoyNinja(Personagem):
    """_summary_: Construtor da classe

        :param x: Posição x do personagem
        :type x: int or float
        :param y: Posição y do personagem
        :type y: int or float
        :param tile_size: Tamanho do tile
        :type tile_size: int
        :param collision_sprites: Sprites que o personagem pode colidir
        :type collision_sprites: pygame.sprite.Group
        :param robos: Sprites dos robôs
        :type robos: pygame.sprite.Group
        """        
    
   
    def __init__(self, x:int, y:int, tile_size:int, collision_sprites:pygame.sprite.Group, robos:pygame.sprite.Group):
        """_summary_: Construtor da classe

        :param x: Posição x do personagem
        :type x: int or float
        :param y: Posição y do personagem
        :type y: int or float
        :param tile_size: Tamanho do tile
        :type tile_size: int
        :param collision_sprites: Sprites que o personagem pode colidir
        :type collision_sprites: pygame.sprite.Group
        :param robos: Sprites dos robôs
        :type robos: pygame.sprite.Group
        """        
        dict_animacoes_boy = {
            "parado": [0, 232, 455, 10],
            "correndo": [5940, 363, 455, 10],
            "pulando": [2325, 362, 483, 10],
            "batendo": [19430, 536, 495, 10],
            "voando": [24787, 443, 454, 10]
        }
        img = "img/spritesheet_boy.png"
        super().__init__(x, y, tile_size, img, dict_animacoes_boy, collision_sprites)
        self.bater = False
        self.planar = False
        self.robos = robos

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
        if self.index_lista == 30:
            if self.direita:
                self.rect.x -= 15
            else:
                self.rect.x -= 70

        if self.index_lista > 39:
            self.index_lista = 0
            self.bater = False

            # Voltar para o local inicial
            if self.direita:
                self.rect.x += 15
            else:
                self.rect.x += 70

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

    def checar_colisao(self):
        """_summary_: Função que checa as colisões do personagem"""
        for robo in self.robos:
            if self.rect.colliderect(robo.rect):
                robo.fun_morrer()

    def update(self):
        """_summary_: Função que atualiza a posição do personagem
        """      

        if self.state == 0:
            self.planar = False

        self.read_input()

        if self.bater:
            self.state = 0
        else:
            self.check_horizontal_collisions(2)

        if self.state == 2 and self.planar == False:
            self.cair()
        # Controle de animação do personagem para bater
        elif self.bater and self.state != 1:
            self.bater_animacao()
            self.checar_colisao()
        # Controle de animação do personagem para correr
        elif self.correr and self.state != 1 and self.planar == False and self.bater == False:
            self.correr_animacao()
        # Controle de animação do personagem para pular
        elif self.state == 1:
            self.pular_animacao()
        # Controle de animação do personagem para planar
        elif self.planar:
            self.planar_animacao()
        # Controle de animação do personagem para parado
        else:
            self.parado_animacao()
        
        if self.bater:
            self.state = 0
        else:
            if self.state == 0:
                self.apply_gravity()
                self.state = 2
            self.check_vertical_collisions()

    def read_input(self):
        """_summary_: Função que lê as entradas do teclado
        """        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_f] and self.state == 0:
            self.fun_bater()

        if not self.bater:
            if keys[pygame.K_d]:
                self.fun_correr_direita()
            elif keys[pygame.K_a]:
                self.fun_correr_esquerda()

            if keys[pygame.K_w]:
                if self.state == 0:
                    self.fun_pular()
                elif self.state == 2:
                    self.fun_planar()

            elif self.planar:
                self.fun_cair()

        


class GirlNinja(Personagem):
    def __init__(self, x:int, y:int, tile_size:int, screen:pygame.Surface, collision_sprites:pygame.sprite.Group, robos:pygame.sprite.Group, alavancas:pygame.sprite.Group):
        """_summary_: Construtor da classe GirlNinja

        :param x: Posição x do personagem
        :type x: int
        :param y: Posição y do personagem
        :type y: int
        :param tile_size: Tamanho do tile
        :type tile_size: int
        :param screen: Tela do jogo
        :type screen: pygame.Surface
        :param collision_sprites: Sprites que o personagem pode colidir
        :type collision_sprites: pygame.sprite.Group
        :param robos: Sprites dos robôs
        :type robos: pygame.sprite.Group
        :param alavancas: Sprites das alavancas
        :type alavancas: pygame.sprite.Group
        """        

        dict_animacoes_girl = {
            "parado": [0, 290, 500, 10],
            "correndo": [6906, 372, 500, 10],
            "pulando": [2910, 399, 500, 10],
            "deslizando": [16425, 397, 401, 10],
            "ataque": [20400, 383, 514, 10]
        }
        img = "img/spritesheet_girl.png"
        super().__init__(x, y, tile_size, img, dict_animacoes_girl, collision_sprites)
        self.screen = screen
        self.deslizar = False
        self.atirar = False
        self.kunai = Kunai(tile_size, self.screen,
                           collision_sprites, robos, alavancas)
        self.velocidade_deslizando = self.velocidade * MOD_VELOCIDADE_DESLIZANDO

    def fun_deslizar(self):
        """_summary_: Função que ativa o personagem deslizando
        """        
        self.deslizar = True
        self.correr = False

        if self.index_lista < 30:
            self.index_lista = 30
        if self.direita == False:
            self.rect.x -= self.velocidade_deslizando
        else:
            self.rect.x += self.velocidade_deslizando

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

        self.read_input()

        self.check_horizontal_collisions(4)

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

        if self.state == 0:
            self.apply_gravity()
            self.state = 2
        self.check_vertical_collisions()

    def read_input(self):
        """_summary_: Função que lê as entradas do teclado"""
        keys = pygame.key.get_pressed()

        if not self.atirar:
            if self.state == 0:
                if keys[pygame.K_UP]:
                    self.fun_pular()
                elif keys[pygame.K_DOWN]:
                    self.fun_deslizar()
                elif keys[pygame.K_RSHIFT]:
                    # TODO: consertar kunai
                    self.fun_atirar()

            if not self.deslizar and not self.atirar:
                if keys[pygame.K_RIGHT]:
                    self.fun_correr_direita()
                elif keys[pygame.K_LEFT]:
                    self.fun_correr_esquerda()


class Robo(Personagem):  
    temporizador = 0
    def __init__(self, x:int, x_distancia:int, y:int, tile_size:int, campo_de_visao:int, collision_sprites:pygame.sprite.Group, movimentacao:bool=True, direita_movimentacao:bool=True):
        """_summary_: Construtor da classe Robo
        :param x: posição x do robo
        :type x: int
        :param x_distancia: distancia que o robo irá se mover
        :type x_distancia: int   
        :param y: posição y do robo
        :type y: int
        :param tile_size: tamanho do tile
        :type tile_size: int
        :param campo_de_visao: distancia que o robo irá ver o personagem
        :type campo_de_visao: int
        :param collision_sprites: grupo de sprites que o robo irá colidir
        :type collision_sprites: pygame.sprite.Group
        :param movimentacao: Se o robô irá se mover ou ficará parado, defaults to True
        :type movimentacao: bool, optional
        :param direita_movimentacao: Qual direção o robô irá se mover de acordo com a posição inicial, defaults to True
        :type direita_movimentacao: bool, optional
        """
        
        dict_animacoes_robo = {
            "parado": [0, 567, 555, 10],
            "correndo": [5670, 567, 550, 8],
            "morrendo": [10190, 562, 519, 10]
        }
        img = "img/spritesheet_robo.png"
        super().__init__(x, y, tile_size, img, dict_animacoes_robo, collision_sprites)
        self.x = x
        self.campo_de_visao = campo_de_visao * tile_size
        self.x_distancia = x_distancia * tile_size
        if direita_movimentacao:
            self.direita = False
        self.vivo = True
        self.movimentacao = movimentacao

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
        self.image = self.imagens_ninja[int(self.index_lista)]

        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image = pygame.transform.flip(self.image, True, False)
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
                return True #Para fazer o test do player
            else:
                return False
        else: # verifica se o player está no campo de visão x        # verifica se o player está no campo de visão y
            if self.rect.x > player.rect.x > self.rect.x - self.campo_de_visao and self.rect.y - 50 <= player.rect.y <= self.rect.y + 50:
                self.correr = False
                print("ESQUERDA campo de visão") 
                return True #Para fazer o test do player
            else:
                return False

    def animacao_morrer(self):
        """_summary_: Função que faz a animação do robo morrer
        """  
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

        if self.vivo == False:
            self.state = 0

        if self.state == 2:
            self.cair()

        if self.state == 0:
            self.apply_gravity()
            self.state = 2
        self.check_vertical_collisions()

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
        self.temporizador += 1

        if self.vivo == False:
            self.state = 0
        else:
            if self.state == 0:
                self.apply_gravity()
                self.state = 2
            self.check_vertical_collisions()


class Kunai(pygame.sprite.Sprite):
    def __init__(self, tile_size:int, screen:pygame.Surface, collision_sprites:pygame.sprite.Group, robos:pygame.sprite.Group, alavancas:pygame.sprite.Group):
        """_summary_: Classe que cria o objeto Kunai

        :param tile_size: Tamanho do tile
        :type tile_size: int
        :param screen: Tela do jogo
        :type screen: pygame.Surface
        :param collision_sprites: Grupo de sprites que colidem
        :type collision_sprites: pygame.sprite.Group
        :param robos: Grupo de sprites dos robos
        :type robos: pygame.sprite.Group
        :param alavancas: Grupo de sprites das alavancas
        :type alavancas: pygame.sprite.Group
        """        

        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        image = pygame.image.load("img/Kunai.png").convert_alpha()
        largura, altura = image.get_size()
        fator = tile_size / largura
        # redimensiona a imagem para o tamanho desejado
        self.kunai_direita = pygame.transform.scale(
            image, (fator * largura, fator * altura))
        self.kunai_esquerda = pygame.transform.flip(
            self.kunai_direita, True, False)
        self.rect = self.kunai_direita.get_rect()
        self.aceleracao_inicial = tile_size * VELOCIDADE_PULO_BLC
        self.aceleracao = self.aceleracao_inicial
        self.direita = True
        self.atirar = False
        self.gravidade = tile_size * GRAVIDADE_BLC
        self.velocidade = tile_size * VELOCIDADE_KUNAI_BLC
        self.collision_sprites = collision_sprites
        self.robos = robos
        self.alavancas = alavancas

    def fun_atirar(self, x:int, y:int, bool_direita:bool):
        """_summary_: Função que atira o kunai

        :param x: Posição x do kunai
        :type x: int
        :param y: Posição y do kunai
        :type y: int
        :param bool_direita: Direção do kunai
        :type bool_direita: bool
        """    
        self.aceleracao = self.aceleracao_inicial
        self.atirar = True
        self.direita = bool_direita
        if self.direita:
            # posiciona o kunai na frente do personagem
            self.rect.midbottom = (x + 100, y)
        else:
            self.rect.midbottom = (x, y)

    def trajetoria(self):
        """_summary_: Função que faz o objeto Kunai seguir uma trajetória
        """        
        if self.direita:
            self.rect.x += self.velocidade
        else:
            self.rect.x -= self.velocidade

        self.rect.y -= self.aceleracao
        self.aceleracao -= self.gravidade

        if self.direita:
            self.screen.blit(self.kunai_direita, self.rect)
        else:
            self.screen.blit(self.kunai_esquerda, self.rect)

    def checar_colisao(self):
        """_summary_: Função que checa se o kunai colidiu com algum objeto"""
        for alavanca in self.alavancas:
            if self.rect.colliderect(alavanca.rect):
                alavanca.mudar_direcao()

        for robo in self.robos:
            if self.rect.colliderect(robo.rect):
                robo.fun_morrer()

        for sprite in self.collision_sprites:
            if self.rect.colliderect(sprite.rect):
                self.atirar = False
                self.aceleracao = self.aceleracao_inicial

    def update(self):
        """_summary_: Função que atualiza a posição do objeto Kunai
        """        
        if self.atirar:
            self.trajetoria()
            self.checar_colisao()
        else:
            self.aceleracao = self.aceleracao_inicial
