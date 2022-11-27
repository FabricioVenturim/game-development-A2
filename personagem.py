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
            self.corta_sprite(
                sprite_sheet, posicao[0], posicao[1], posicao[2], posicao[3], posicao[4])

        self.__index_lista = 0
        self.image = self.imagens_ninja[self.index_lista]
        self.__rect = self.image.get_rect(midbottom=(x, y))

        self.__direita = True
        self.__correr = False
        # TODO: planar não deveria estar só na classe BoyNinja?
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

    def corta_sprite(self, sprite_sheet, posicao_inicial, largura, altura, quantidade, redirecionamento):
        for i in range(0, quantidade):
            largura_inicial = posicao_inicial
            img = sprite_sheet.subsurface(
                (largura_inicial + i*largura, 0), (largura, altura))
            img = pygame.transform.scale(
                img, (largura/redirecionamento, altura/redirecionamento))
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
        self.rect.y += self.aceleracao
        self.aceleracao += self.gravidade
        self.index_lista = 24
        self.image = self.imagens_ninja[int(self.index_lista)]
        if self.direita == False:
            self.image = pygame.transform.flip(self.image, True, False)

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
            # TODO: Ela precisa desse atributo?
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

    def read_input(self):
        keys = pygame.key.get_pressed()

        if not self.atirar:
            if self.state == 0:
                if keys[pygame.K_UP]:
                    self.fun_pular()
                elif keys[pygame.K_DOWN]:
                    # TODO: consertar deslizar
                    self.fun_deslizar()
                elif keys[pygame.K_RSHIFT]:
                    # TODO: consertar kunai
                    self.fun_atirar()

            if keys[pygame.K_RIGHT]:
                self.fun_correr_direita()
            elif keys[pygame.K_LEFT]:
                self.fun_correr_esquerda()


class Robo(Personagem):
    def __init__(self, x_inicial, y, temporizador_parado, temporizador_correndo, img, dict_animacoes):
        super().__init__(x_inicial, y, img, dict_animacoes)
        self.__temporizador_parado = temporizador_parado
        self.__temporizador_correndo = temporizador_correndo

        self.__vivo = True
        self.__temporizador = 0

    @property
    def temporizador_parado(self):
        return self.__temporizador_parado

    @temporizador_parado.setter
    def temporizador_parado(self, value):
        self.__temporizador_parado = value

    @property
    def temporizador_correndo(self):
        return self.__temporizador_correndo

    @temporizador_correndo.setter
    def temporizador_correndo(self, value):
        self.__temporizador_correndo = value

    @property
    def vivo(self):
        return self.__vivo

    @vivo.setter
    def vivo(self, value):
        self.__vivo = value

    @property
    def temporizador(self):
        return self.__temporizador

    @temporizador.setter
    def temporizador(self, value):
        self.__temporizador = value

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
        if self.vivo == False:
            self.animacao_morrer()

        # Controle de animação do personagem para correr
        elif self.temporizador >= self.temporizador_parado and self.temporizador <= self.temporizador_correndo:
            self.correr_animacao()
            if self.direita:
                self.fun_correr_direita()
            else:
                self.fun_correr_esquerda()
        # Controle de animação do personagem para parado após correr
        elif self.temporizador > self.temporizador_correndo + self.temporizador_parado:
            self.temporizador = self.temporizador_parado
            self.direita = not self.direita
        else:
            self.parado_animacao()
        self.temporizador += 1

    def update_vertical_pos(self):
        if self.state == 2:
            self.cair()


class Kunai(pygame.sprite.Sprite):
    gravidade = 1.5
    aceleracao_inicial = 25

    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        image = pygame.image.load("img/Kunai.png").convert_alpha()
        # redimensiona a imagem para o tamanho desejado
        self.__image = pygame.transform.scale(image, (160/2.4, 32/2.4))
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
            # posiciona o kunai na frente do personagem
            self.rect.midbottom = (x + 100, y)
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
            self.screen.blit(pygame.transform.flip(
                self.image, True, False), self.rect)

    def update(self):
        if self.atirar:
            self.trajetoria()
        else:
            self.aceleracao = self.aceleracao_inicial
