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
    # Define estados possíveis do jogador
    # parado = 0
    # pulando = 1
    # caindo = 2

    # Define a aceleração da gravidade
    #gravidade = 2

    def __init__(self, x, y, tile_size, img, dict_animacoes, collision_sprites):
        pygame.sprite.Sprite.__init__(self)
        self.__state = 2
        self.collision_sprites = collision_sprites

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

        self.__index_lista = 0
        self.image = self.imagens_ninja[self.index_lista]
        self.__rect = self.image.get_rect(midbottom=(x + tile_size / 2, y + tile_size))

        self.__direita = True
        self.__correr = False
        # TODO: planar não deveria estar só na classe BoyNinja?
        self.__planar = False
        self.mask = pygame.mask.from_surface(self.image)

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

    def corta_sprite(self, sprite_sheet, posicao_inicial, largura, altura, quantidade, redirecionamento):
        for i in range(0, quantidade):
            largura_inicial = posicao_inicial
            img = sprite_sheet.subsurface(
                (largura_inicial + i*largura, 0), (largura, altura))
            img = pygame.transform.scale(
                img, (largura * redirecionamento, altura * redirecionamento))
            self.imagens_ninja.append(img)

    def parado_animacao(self):
        if self.index_lista > 9:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.imagens_ninja[int(self.index_lista)]
        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image = pygame.transform.flip(self.image, True, False)

    def fun_correr_direita(self):
        self.direita = True
        self.correr = True
        if self.index_lista < 10:
            self.index_lista = 10
        if self.state == 1 or self.planar:
            self.rect.x += self.velocidade_caindo
        else:
            self.rect.x += self.velocidade

    def fun_correr_esquerda(self):
        self.direita = False
        self.correr = True
        if self.index_lista < 10:
            self.index_lista = 10
        if self.state == 1 or self.planar:
            self.rect.x -= self.velocidade_caindo
        else:
            self.rect.x -= self.velocidade

    def correr_animacao(self):
        if self.index_lista > 19:
            self.index_lista = 10
        self.index_lista += 0.25
        self.image = self.imagens_ninja[int(self.index_lista)]

        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image = pygame.transform.flip(self.image, True, False)
        self.correr = False

    def fun_cair(self):
        self.correr = False
        self.planar = False
        self.state = 2

    def cair(self):
        self.apply_gravity()
        self.index_lista = 24
        self.image = self.imagens_ninja[int(self.index_lista)]
        if self.direita == False:
            self.image = pygame.transform.flip(self.image, True, False)

    def apply_gravity(self):
        self.aceleracao += self.gravidade
        self.rect.y += self.aceleracao

        # Aceleração máxima
        if self.aceleracao > 18:
            self.aceleracao = 18

    def fun_pular(self):
        self.correr = False
        self.state = 1
        self.aceleracao = self.aceleracao_pulo_inicial
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
            self.rect.y -= self.aceleracao
            self.aceleracao += self.gravidade

    def check_horizontal_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if self.rect.colliderect(sprite.rect):
                if self.direita:
                    self.rect.right = sprite.rect.left
                else:
                    self.rect.left = sprite.rect.right

    def check_vertical_collisions(self):
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
    def __init__(self, x, y, tile_size, collision_sprites):
        dict_animacoes_boy = {
            "parado": [0, 232, 455, 10],
            "correndo": [5940, 363, 455, 10],
            "pulando": [2325, 362, 483, 10],
            "batendo": [19410, 536, 495, 10],
            "voando": [24787, 443, 454, 10]
        }
        img = "img/spritesheet_boy.png"
        super().__init__(x, y, tile_size, img, dict_animacoes_boy, collision_sprites)
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
        # Deixar a animação mais suave
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
            self.planar = False

        self.read_input()
        self.check_horizontal_collisions()

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

        if self.state == 0:
            self.apply_gravity()
            self.state = 2
        self.check_vertical_collisions()

    def read_input(self):
        keys = pygame.key.get_pressed()

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

            if keys[pygame.K_f] and self.state == 0:
                self.fun_bater()


class GirlNinja(Personagem):
    def __init__(self, x, y, tile_size, screen, collision_sprites, robos, alavancas):
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
        self.__deslizar = False
        self.__atirar = False
        self.kunai = Kunai(tile_size, self.screen, collision_sprites, robos, alavancas)
        self.velocidade_deslizando = self.velocidade * MOD_VELOCIDADE_DESLIZANDO

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

        if self.index_lista < 30:
            self.index_lista = 30
        if self.direita == False:
            self.rect.x -= self.velocidade_deslizando
        else:
            self.rect.x += self.velocidade_deslizando

    def deslizar_animacao(self):
        if self.index_lista > 39:
            self.index_lista = 30
        self.index_lista += 0.25
        self.image = self.imagens_ninja[int(self.index_lista)]

        # vira a imagem se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image = pygame.transform.flip(self.image, True, False)
        self.deslizar = False

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
            # TODO: Ela precisa desse atributo?
            self.planar = False

        self.read_input()
        self.check_horizontal_collisions()

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

    def __init__(self, x, x_distancia, y, tile_size, campo_de_visao, collision_sprites, movimentacao=True, direita_movimentacao=True):
        """_summary_: Classe que representa o Robo 

        :param x: posição x do robo
        :type x: int
        :param x_distancia: distancia que o robo irá se mover
        :type x_distancia: int   
        :param y: posição y do robo
        :type y: int
        :param campo_de_visao: distancia que o robo irá ver o personagem
        :type campo_de_visao: int
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
        self.__x = x
        self.__campo_de_visao = campo_de_visao * tile_size
        self.__x_distancia = x_distancia * tile_size
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
        self.image = self.imagens_ninja[int(self.index_lista)]

        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image = pygame.transform.flip(self.image, True, False)
        self.correr = False

    def verifica_player(self, player):
        if self.direita:     # verifica se o player está no campo de visão x        # verifica se o player está no campo de visão y
            if self.rect.x < player.rect.x < self.rect.x + self.campo_de_visao and self.rect.y - 50 <= player.rect.y <= self.rect.y + 50:
                self.correr = False
                print("DIREITAA campo de visão")

        else:  # verifica se o player está no campo de visão x        # verifica se o player está no campo de visão y
            if self.rect.x > player.rect.x > self.rect.x - self.campo_de_visao and self.rect.y - 50 <= player.rect.y <= self.rect.y + 50:
                self.correr = False
                print("ESQUERDA campo de visão")

    def animacao_morrer(self):
        if self.index_lista == 24:  # quando a colisão tiver certa, aí isso vai sair
            self.rect.y += 10
        if self.index_lista > 27:
            self.index_lista = 27
        self.index_lista += 0.25
        self.image = self.imagens_ninja[int(self.index_lista)]

        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image = pygame.transform.flip(self.image, True, False)
        self.correr = False

    def update(self):
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

        self.check_horizontal_collisions()


class Kunai(pygame.sprite.Sprite):
    def __init__(self, tile_size, screen, collision_sprites, robos, alavancas):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        image = pygame.image.load("img/Kunai.png").convert_alpha()
        largura, altura = image.get_size()
        fator = tile_size / largura
        # redimensiona a imagem para o tamanho desejado
        self.kunai_direita = pygame.transform.scale(image, (fator * largura, fator * altura))
        self.kunai_esquerda = pygame.transform.flip(self.kunai_direita, True, False)
        self.__rect = self.kunai_direita.get_rect()
        self.aceleracao_inicial = tile_size * VELOCIDADE_PULO_BLC
        self.__aceleracao = self.aceleracao_inicial
        self.__direita = True
        self.__atirar = False
        self.gravidade = tile_size * GRAVIDADE_BLC
        self.velocidade = tile_size * VELOCIDADE_KUNAI_BLC
        self.collision_sprites = collision_sprites
        self.robos = robos
        self.alavancas = alavancas

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
        self.aceleracao = self.aceleracao_inicial
        self.atirar = True
        self.direita = bool_direita
        if self.direita:
            # posiciona o kunai na frente do personagem
            self.rect.midbottom = (x + 100, y)
        else:
            self.rect.midbottom = (x, y)

    def trajetoria(self):
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
        if self.atirar:
            self.trajetoria()
            self.checar_colisao()
        else:
            self.aceleracao = self.aceleracao_inicial
