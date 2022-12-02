import pygame


class Alavanca(pygame.sprite.Sprite):
    def __init__(self, x, y, grupo_colisao):
        super().__init__()
        self.x = x
        self.y = y
        self.on = False
        self.alavanca_off = pygame.image.load("alavanca1.png")
        self.alavanca_on = pygame.transform.flip(
            self.alavanca_off, True, False)
        self.image = self.alavanca_off
        self.rect = self.image.get_rect(topleft=(x, y))
        self.grupo_colisao = grupo_colisao
        self.iscolliding = False

    def colisao(self):
        for personagem in self.grupo_colisao:
            if personagem.rect.colliderect(self.rect):
                if personagem.direita == True:
                    personagem.rect.right = self.rect.left
                    #persongagem.rect.left = self.rect.right

                else:
                    personagem.rect.left = self.rect.right

    def mudar_direcao(self):
        if self.on == False:
            self.image = self.alavanca_off
        else:
            self.image = self.alavanca_on

    def update(self):
        collision = bool(pygame.sprite.spritecollideany(
            self, self.grupo_colisao))
        if collision and not self.iscolliding:
            self.on = not self.on
            self.mudar_direcao()

        self.iscolliding = collision
        self.colisao()
        



class Chave(pygame.sprite.Sprite):
    def __init__(self, x, y, grupo_colisao):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(
            pygame.image.load("chave.png"), (30, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.grupo_colisao = grupo_colisao
        self.active = True

    def pegar_chave(self, grupo_colisao):
        for personagem in grupo_colisao.sprites():
            if personagem.rect.colliderect(self.rect):
                self.active = False
                self.kill()

    def update(self):
        self.pegar_chave(self.grupo_colisao)


class Portao(pygame.sprite.Sprite):
    def __init__(self, x, y, grupo_colisao, chaves=None, portoes=None):
        super().__init__()
        self.x = x
        self.y = y
        self.img_aberto = pygame.image.load("portao_aberto.png")
        self.img_fechado = pygame.image.load("portao_fechado.png")
        self.image = self.img_fechado
        self.rect = self.image.get_rect(center=(x, y))
        self.open = False
        self.grupo_colisao = grupo_colisao
        self.chaves = chaves
        self.portoes = portoes

    def abrir_portao(self):
        self.open = True
        self.image = self.img_aberto

    def liberar_portao(self):
        if self.chaves != None and self.portoes != None:
            if len(self.chaves.sprites()) == 0:
                self.portoes.sprites()[0].abrir_portao()

    def update(self):
        self.liberar_portao()


class Plataforma(pygame.sprite.Sprite):
    # variacao_x e variacao_y são uma tupla com dois valores: máximos e mínimos de x e y
    # Se o movimento for horizontal=True colocar True, se for vertical colocar horizontal = False
    def __init__(self, x, y, variacao_x=None, variacao_y=None, platform_vel=3, grupo_colisao=None, horizontal=True):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load("plataforma.png")
        self.rect = self.image.get_rect(center=(x, y))
        self.rect_over = self.rect.copy()
        self.rect_test = pygame.Rect(0, 0, 0, 0)
        self.grupo_colisao = grupo_colisao
        self.platform_vel = platform_vel
        self.variacao_x = variacao_x
        self.variacao_y = variacao_y
        self.horizontal = horizontal

    def movimentar_plataforma(self, horizontal):
        self.horizontal = horizontal
        if self.horizontal == True:
            x_min, x_max = self.variacao_x
            if self.rect.left >= x_max or self.rect.left <= x_min:
                self.platform_vel *= -1
            self.rect.left += self.platform_vel
            self.rect_over.update(self.rect)
            self.rect_over.y -= 1
            for personagens in self.grupo_colisao.sprites():
                if personagens.rect.colliderect(self.rect_over) and not personagens.rect.colliderect(self.rect):
                    personagens.rect.x += self.platform_vel
                    direita = personagens.direita
                    personagens.direita = self.platform_vel > 0
                    personagens.check_horizontal_collisions()
                    personagens.direita = direita
        else:
            y_min, y_max = self.variacao_y
            if self.rect.top >= y_max or self.rect.top <= y_min:
                self.platform_vel *= -1
            self.rect.bottom += self.platform_vel
            if self.platform_vel > 0:
                self.rect_over.update(self.rect)
                self.rect_over.y -= 1 + 2*self.platform_vel
                for personagens in self.grupo_colisao.sprites():
                    if personagens.rect.colliderect(self.rect_over) and not personagens.rect.colliderect(self.rect) and personagens.state != 1:
                        personagens.rect.bottom = self.rect.top
                        personagens.check_vertical_collisions()

    def colisao(self):
        for personagem in self.grupo_colisao.sprites():
            aceleracao = -personagem.aceleracao
            
            if not self.horizontal:
                aceleracao_relativa = aceleracao - self.platform_vel
            else:
                aceleracao_relativa = aceleracao
            
            if (
                personagem.rect.left < self.rect.right and
                personagem.rect.right > self.rect.left and
                personagem.rect.bottom > self.rect.top and
                personagem.rect.bottom < self.rect.bottom and
                (aceleracao_relativa >= 0 or personagem.state == 2)
               ):
                self.rect_test.update(personagem.rect)
                self.rect_test.bottom = self.rect.top
                for sprite in personagem.collision_sprites.sprites():
                    if sprite.rect.colliderect(self.rect_test):
                        return
                personagem.state = 0
                personagem.aceleracao = 0
                personagem.rect.bottom = self.rect.top

    def update(self):
        self.colisao()
        self.movimentar_plataforma(self.horizontal)


class Plataforma_com_alavanca(Plataforma):
    def __init__(self, x, y, alavanca, variacao_x=None, variacao_y=None, platform_vel=3, grupo_colisao=None, horizontal=True):
        super().__init__(x, y, variacao_x, variacao_y,
                         platform_vel, grupo_colisao, horizontal)
        self.alavanca = alavanca

    def movimentar_condicional(self):
        if self.alavanca.on == True:
            self.movimentar_plataforma(True)

    def update(self):
        self.colisao()
        self.movimentar_condicional()


class Botao(pygame.sprite.Sprite):
    def __init__(self, x, y, botoes, grupo_colisao):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load("botao.png")
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.ativo = False
        self.botoes = botoes
        self.grupo_colisao = grupo_colisao
        self.mask = pygame.mask.from_surface(self.image)
        self.rect_collision = self.rect

    def abaixar_botao(self):
        self.image = pygame.image.load("botao_apertado.png")
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def apertar_botao(self):
        self.ativo = False
        for personagens in self.grupo_colisao.sprites():
            if personagens.rect.colliderect(self.rect_collision):
                self.abaixar_botao()
                self.ativo = True
        if not self.ativo:
            self.image = pygame.image.load("botao.png")
            self.rect = self.image.get_rect(midbottom=(self.x, self.y))
        # print(self.ativo)

    def update(self):
        self.apertar_botao()
        # self.abaixar_botao()
