import pygame
import math


class Alavanca(pygame.sprite.Sprite):
    """
        Classe da Alavanca

        Args:
            x (float): posição x que a alavanca será colocada
            y (float): posição y que a alavanca será colocada
            grupo_colisao (pygame.sprite.Group): grupo que pode ativar a alavanca
        """

    def __init__(self, x, y, tile_size, grupo_colisao):
        """

        Args:
            x (float): posição x que a alavanca será colocada
            y (float): posição y que a alavanca será colocada
            tile_size (float): tamanho da tile
            grupo_colisao (pygame.sprite.Group): grupo que pode ativar a alavanca
        """
        super().__init__()
        self.x = x
        self.y = y
        self.on = False
        self.alavanca_off = pygame.image.load(
            "img/alavanca1.png").convert_alpha()
        self.alavanca_off = pygame.transform.smoothscale(
            self.alavanca_off, (tile_size, tile_size))
        self.alavanca_on = pygame.transform.flip(
            self.alavanca_off, True, False)
        self.image = self.alavanca_off
        self.rect = self.image.get_rect(
            midbottom=(x + tile_size / 2, y + tile_size * 1.20))
        self.grupo_colisao = grupo_colisao
        self.iscolliding = False

    def mudar_direcao(self):
        """
            Função que altera muda a imagem da alavanca: ativada ou desativada
        """
        self.on = not self.on

        if self.on == False:
            self.image = self.alavanca_off
        else:
            self.image = self.alavanca_on

    def update(self):
        collision = bool(pygame.sprite.spritecollideany(
            self, self.grupo_colisao))
        if collision and not self.iscolliding:
            self.mudar_direcao()

        self.iscolliding = collision


class Chave(pygame.sprite.Sprite):
    """
        Classe da Chave

        Args:
            x (float): posição x que a chave será colocada
            y (float): posição y que a chave será colocada
            tile_size (float): tamanho da tile
            grupo_colisao (pygame.sprite.Group): grupo que pode pegar a chave
    """

    def __init__(self, x, y, tile_size, grupo_colisao):
        """

        Args:
            x (float): posição x que a chave será colocada
            y (float): posição y que a chave será colocada
            tile_size (float): tamanho da tile
            grupo_colisao (pygame.sprite.Group): grupo que pode pegar a chave
        """

        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.transform.smoothscale(
            pygame.image.load("img/chave.png"), (tile_size * 0.45, tile_size * 0.9)).convert_alpha()
        self.rect = self.image.get_rect(
            center=(x + tile_size / 2, y + tile_size / 2))
        self.grupo_colisao = grupo_colisao
        self.active = True

    def pegar_chave(self, grupo_colisao):
        """Função que apaga a chave da fase caso algum integrante do grupo_colisao toque na chave

        Args:
            grupo_colisao (pygame.sprite.Group): Grupo que pode pegar a chave
        """
        for personagem in grupo_colisao.sprites():
            if personagem.collision_rect.colliderect(self.rect):
                self.active = False
                self.kill()

    def update(self):
        self.pegar_chave(self.grupo_colisao)


class Portao(pygame.sprite.Sprite):
    """
        Classe de Portão
            Args:
                x (float): posição x que o portão será colocado
                y (float): posição y que o portão será colocado
                grupo_colisao (pygame.sprite.Group): Grupo que colide com o portão
                chaves (pygame.sprite.Group, optional): Grupo de chaves que abre o portão
                portoes (pygame.sprite.Group, optional): Grupo de portões que podem ser abertos
    """

    def __init__(self, x, y, tile_size, grupo_colisao, chaves=None, portoes=None):
        """
        Classe de Portão
            Args:
                x (float): posição x que o portão será colocado
                y (float): posição y que o portão será colocado
                grupo_colisao (pygame.sprite.Group): Grupo que colide com o portão
                chaves (pygame.sprite.Group, optional): Grupo de chaves que abre o portão
                portoes (pygame.sprite.Group, optional): Grupo de portões que podem ser abertos
        """
        super().__init__()
        self.x = x
        self.y = y
        self.img_aberto = pygame.image.load(
            "img/portao_aberto.png").convert_alpha()
        self.img_fechado = pygame.image.load(
            "img/portao_fechado.png").convert_alpha()

        largura, altura = self.img_fechado.get_size()
        fator = 2 * tile_size / largura
        self.img_fechado = pygame.transform.smoothscale(self.img_fechado, (
            largura * fator, altura * fator))

        largura_aberto, altura_aberto = self.img_aberto.get_size()
        self.img_aberto = pygame.transform.smoothscale(self.img_aberto, (
            largura_aberto * fator, altura_aberto * fator))

        self.image = self.img_fechado
        self.rect = self.img_fechado.get_rect(
            midbottom=(x + tile_size, y + tile_size * 1.20))
        self.rect_aberto = self.img_aberto.get_rect(
            midbottom=(x + tile_size * 0.80, y + tile_size * 1.20))
        self.open = False
        self.grupo_colisao = grupo_colisao
        self.chaves = chaves
        self.portoes = portoes
        self.pers_no_portao = None
        self.liberar_fase = False

    def verificar_personagens_portao(self):
        if self.open == True:
            self.pers_no_portao = 0
            for personagem in self.grupo_colisao.sprites():
                if self.rect.contains(personagem.rect):
                    self.pers_no_portao += 1
            if self.pers_no_portao == len(self.grupo_colisao.sprites()):
                self.liberar_fase = True

    def abrir_portao(self):
        """
        Função que mostra a imagem do portão aberto
        """
        self.open = True
        self.image = self.img_aberto
        self.rect = self.rect_aberto

    def liberar_portao(self):
        """
            Função que libera o portão caso a chave tenha sido "pega"
        """
        if self.chaves != None and self.portoes != None:
            if len(self.chaves.sprites()) == 0:
                self.portoes.sprites()[0].abrir_portao()

    def update(self):
        self.liberar_portao()
        self.verificar_personagens_portao()


class Plataforma(pygame.sprite.Sprite):
    """
    Classe das plataformas
        Args:
            x (float): posição x que a plataforma será colocada
            y (float): posição y que a plataforma será colocada
            tile_size (float): tamanho da tile
            variacao_x (tuple, optional): Variação na horizontal que a plataforma se movimenta. Defaults to None.
            variacao_y (tuple, optional): Variação na vertical que a plataforma se movimenta. Defaults to None.
            platform_vel (float, optional): Velocidade da plataforma. Defaults to 0.02.
            grupo_colisao (pygame.sprite.Group, optional): Grupo que pode colide com a plataforma. Defaults to None.
            horizontal (bool, optional): Movimentação horizontal da plataforma. Defaults to True.
        """
    # variacao_x e variacao_y são uma tupla com dois valores: máximos e mínimos de x e y
    # Se o movimento for horizontal=True colocar True, se for vertical colocar horizontal = False

    def __init__(self, x, y, tile_size, variacao_x=(0,), variacao_y=(0,), platform_vel=0.02, grupo_colisao=None, horizontal=True):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load("img/plataforma.png").convert_alpha()
        self.image = pygame.transform.smoothscale(
            self.image, (tile_size, tile_size / 2))
        self.rect = self.image.get_rect(topleft=(x, y))
        padding_x = tile_size * 0.1
        padding_y = tile_size * 0.13
        self.rect_collision = pygame.Rect(
            x + padding_x,
            y + padding_y,
            tile_size - padding_x,
            tile_size / 2 - padding_y
        )
        self.rect_over = self.rect.copy()
        self.rect_test = pygame.Rect(0, 0, 0, 0)
        self.grupo_colisao = grupo_colisao
        self.platform_vel = math.ceil(platform_vel * tile_size)
        self.variacao_x = tuple(x + tile_size * lim for lim in variacao_x)
        self.variacao_y = tuple(y + tile_size * lim for lim in variacao_y)
        self.horizontal = horizontal

    def movimentar_plataforma(self, horizontal):
        """Função que movimenta a plataforma

        Args:
            horizontal (bool): Movimentação horizontal da plataforma
        """
        self.horizontal = horizontal
        if self.horizontal == True:
            x_min, x_max = self.variacao_x
            if self.rect.left >= x_max or self.rect.left <= x_min:
                self.platform_vel *= -1
            self.rect.left += self.platform_vel
            self.rect_collision.center = self.rect.center
            self.rect_over.update(self.rect_collision)
            self.rect_over.y -= 1
            for personagens in self.grupo_colisao.sprites():
                if personagens.collision_rect.colliderect(self.rect_over) and not personagens.collision_rect.colliderect(self.rect_collision):
                    personagens.collision_rect.x += self.platform_vel
                    direita = personagens.direita
                    personagens.direita = self.platform_vel > 0
                    personagens.check_horizontal_collisions(2)
                    personagens.direita = direita
        else:
            y_min, y_max = self.variacao_y
            if self.rect.top >= y_max or self.rect.top <= y_min:
                self.platform_vel *= -1
            self.rect.bottom += self.platform_vel
            self.rect_collision.center = self.rect.center
            if self.platform_vel > 0:
                self.rect_over.update(self.rect_collision)
                self.rect_over.y -= 1 + 2*self.platform_vel
                for personagens in self.grupo_colisao.sprites():
                    if personagens.collision_rect.colliderect(self.rect_over) and not personagens.collision_rect.colliderect(self.rect_collision) and personagens.state != 1:
                        personagens.collision_rect.bottom = self.rect_collision.top
                        personagens.check_vertical_collisions()

    def colisao(self):
        """
        Função que cria a colisão dos personagens com a plataforma
        """
        for personagem in self.grupo_colisao.sprites():
            aceleracao = -personagem.aceleracao

            if not self.horizontal:
                aceleracao_relativa = aceleracao - self.platform_vel
            else:
                aceleracao_relativa = aceleracao

            if (
                personagem.collision_rect.left < self.rect_collision.right and
                personagem.collision_rect.right > self.rect_collision.left and
                personagem.collision_rect.bottom > self.rect_collision.top and
                personagem.collision_rect.bottom < self.rect_collision.bottom and
                (aceleracao_relativa >= 0 or personagem.state == 2)
            ):
                self.rect_test.update(personagem.collision_rect)
                self.rect_test.bottom = self.rect_collision.top
                posicao_valida = True
                for sprite in personagem.collision_sprites.sprites():
                    if sprite.rect.colliderect(self.rect_test):
                        posicao_valida = False
                        break

                if posicao_valida:
                    personagem.state = 0
                    personagem.aceleracao = 0
                    personagem.collision_rect.bottom = self.rect_collision.top

    def update(self):
        self.colisao()
        self.movimentar_plataforma(self.horizontal)


class Plataforma_com_alavanca(Plataforma):
    """Classe da plataforma que é ativada por alvanca
        Args:
            x (float): posição x que a plataforma será colocada
            y (float): posição y que a plataforma será colocada
            tile_size (float): tamanho da tile
            ativadores (list): Lista dos ativadores da plataforma
            variacao_x (tuple, optional): Variação na horizontal que a plataforma se movimenta. 
            variacao_y (tuple, optional): Variação na vertical que a plataforma se movimenta. 
            platform_vel (float, optional): Velocidade da plataforma. Defaults to 0.02.
            grupo_colisao (pygame.sprite.Group, optional): Grupo que pode colide com a plataforma. Defaults to None.
            horizontal (bool, optional): Movimentação horizontal da plataforma. Defaults to True.
        """

    def __init__(self, x, y, tile_size, ativadores=[], variacao_x=(0,), variacao_y=(0,), platform_vel=0.02, grupo_colisao=None, horizontal=True):
        super().__init__(x, y, tile_size, variacao_x, variacao_y,
                         platform_vel, grupo_colisao, horizontal)
        self.ativadores = ativadores

    def movimentar_condicional(self):
        """
            Função que movimenta a plataforma caso a alavanca ligada à ela esteja ativada
        """
        movimentar = False
        for ativador in self.ativadores:
            if ativador.on:
                movimentar = True
                break

        if movimentar:
            self.movimentar_plataforma(self.horizontal)

    def update(self):
        self.colisao()
        self.movimentar_condicional()


class Botao(pygame.sprite.Sprite):
    """
    Classe dos botões

        Args:
            x (float): posição x que o botao será colocado
            y (float): posição y que o botao será colocado
            tile_size (float): tamanho da tile
            grupo_colisao (pygame.sprite.Group, optional): Grupo que pode colide com o botão
        """

    def __init__(self, x, y, tile_size, botoes, grupo_colisao):
        super().__init__()
        self.x = x
        self.y = y

        self.img_solto = pygame.image.load("img/botao.png").convert_alpha()
        largura = self.img_solto.get_width()

        self.img_solto = pygame.transform.smoothscale(
            self.img_solto, (tile_size, tile_size * 0.6))
        largura_scaled, altura_scaled = self.img_solto.get_size()

        self.img_apertado = pygame.image.load(
            "img/botao_apertado.png").convert_alpha()
        largura_apertado = self.img_apertado.get_width()
        fator = largura_apertado / largura

        self.img_apertado = pygame.transform.smoothscale(
            self.img_apertado, (largura_scaled * fator, altura_scaled * fator))

        self.image = self.img_solto
        self.midbottom = (x + tile_size / 2, y + tile_size)
        self.rect = self.image.get_rect(
            midbottom=self.midbottom)
        self.on = False
        self.botoes = botoes
        self.grupo_colisao = grupo_colisao
        self.mask = pygame.mask.from_surface(self.image)
        self.rect_collision = self.rect

    def abaixar_botao(self):
        """
            Função que faz o botão ser abaixado
        """
        self.image = self.img_apertado
        self.rect = self.image.get_rect(midbottom=self.midbottom)

    def apertar_botao(self):
        """
            Função que detecta a colisão com o grupo_colisao(personagens)
        """
        self.on = False
        for personagens in self.grupo_colisao.sprites():
            if personagens.collision_rect.colliderect(self.rect_collision):
                self.abaixar_botao()
                self.on = True
        if not self.on:
            self.image = self.img_solto
            self.rect = self.image.get_rect(midbottom=self.midbottom)
        # print(self.on)

    def update(self):
        self.apertar_botao()
        # self.abaixar_botao()
