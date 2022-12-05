import pygame
class Alavanca(pygame.sprite.Sprite):
    """
        Classe da Alavanca

        Args:
            x (float): posição x que a alavanca será colocada
            y (float): posição y que a alavanca será colocada
            grupo_colisao (pygame.sprite.Group): grupo que pode ativar a alavanca
        """
    def __init__(self, x:float, y:float, grupo_colisao:pygame.sprite.Group):
        """

        Args:
            x (float): posição x que a alavanca será colocada
            y (float): posição y que a alavanca será colocada
            grupo_colisao (pygame.sprite.Group): grupo que pode ativar a alavanca
        """
        super().__init__()
        self.x = x
        self.y = y
        self.on = False
        self.alavanca_off = pygame.image.load("alavanca1.png")
        self.alavanca_on = pygame.transform.flip(self.alavanca_off, True, False)
        self.image = self.alavanca_off
        self.rect = self.image.get_rect(topleft = (x,y))
        self.grupo_colisao = grupo_colisao
        self.iscolliding = False

    def colisao(self):
        """
            Função que cria a colisão com a alavanca
        """
        for personagem in self.grupo_colisao:
            if personagem.rect.colliderect(self.rect):
                if personagem.direita == True:
                    personagem.rect.right = self.rect.left
                    #persongagem.rect.left = self.rect.right
                    
                else:
                    personagem.rect.left = self.rect.right


    def mudar_direcao(self):
        """
            Função que altera muda a imagem da alavanca: ativada ou desativada
        """
        if self.on == False:
            self.image = self.alavanca_off
        else:
            self.image = self.alavanca_on

    

    def update(self):
        collision = bool(pygame.sprite.spritecollideany(self, self.grupo_colisao))
        if collision and not self.iscolliding:
            self.on = not self.on
            self.mudar_direcao()

        self.iscolliding = collision
        self.colisao()
        


            
class Chave(pygame.sprite.Sprite):
    """
        Classe da Chave

        Args:
            x (float): posição x que a chave será colocada
            y (float): posição y que a chave será colocada
            grupo_colisao (pygame.sprite.Group): grupo que pode pegar a chave
    """

    def __init__(self, x, y, grupo_colisao):
        """

        Args:
            x (float): posição x que a chave será colocada
            y (float): posição y que a chave será colocada
            grupo_colisao (pygame.sprite.Group): grupo que pode pegar a chave
        """
        
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load("chave.png"), (30,50)) 
        self.rect = self.image.get_rect(center = (x,y))
        self.grupo_colisao = grupo_colisao
        self.active = True

    def pegar_chave(self, grupo_colisao):
        """Função que apaga a chave da fase caso algum integrante do grupo_colisao toque na chave

        Args:
            grupo_colisao (pygame.sprite.Group): Grupo que pode pegar a chave
        """
        for personagem in grupo_colisao.sprites():
            if personagem.rect.colliderect(self.rect):
                self.active = False
                self.kill()
            

    def update(self):
        self.pegar_chave(self.grupo_colisao)
    

class Portao(pygame.sprite.Sprite):
    
    """
        Classe de Portão
            Args:
                x (float): posição x que a chave será colocada
                y (float): posição y que a chave será colocada
                grupo_colisao (pygame.sprite.Group): Grupo que colide com o portão
                chaves (pygame.sprite.Group, optional): Grupo de chaves que abre o portão
                portoes (pygame.sprite.Group, optional): Grupo de portões que podem ser abertos
    """

    def __init__(self, x:float, y:float, grupo_colisao:pygame.sprite.Group, chaves:pygame.sprite.Group=None, portoes:pygame.sprite.Group=None):
        """
        Args:
            x (float): posição x que a chave será colocada
            y (float): posição y que a chave será colocada
            grupo_colisao (pygame.sprite.Group): Grupo que colide com o portão
            chaves (pygame.sprite.Group, optional): Grupo de chaves que abre o portão. Defaults to None.
            portoes (pygame.sprite.Group, optional): Grupo de portões que podem ser abertos. Defaults to None.
        """
        super().__init__()
        self.x = x
        self.y = y
        self.img_aberto = pygame.image.load("portao_aberto.png")
        self.img_fechado = pygame.image.load("portao_fechado.png")
        self.image = self.img_fechado
        self.rect = self.image.get_rect(center = (x,y))
        self.open = False
        self.grupo_colisao = grupo_colisao
        self.chaves = chaves
        self.portoes = portoes

    def abrir_portao(self):
        """
        Função que mostra a imagem do portão aberto
        """
        self.open = True
        self.image = self.img_aberto
        
    
    def liberar_portao(self):
        """
            Função que libera o portão caso a chave tenha sido "pega"
        """
        if self.chaves != None and self.portoes != None:
            if len(self.chaves.sprites()) == 0:
                self.portoes.sprites()[0].abrir_portao()


    def update(self):
        self.liberar_portao()

class Plataforma(pygame.sprite.Sprite):
    # variacao_x e variacao_y são uma tupla com dois valores: máximos e mínimos de x e y
    # Se o movimento for horizontal=True colocar True, se for vertical colocar horizontal = False
    def __init__(self, x:float, y:float, variacao_x:tuple=None, variacao_y:tuple=None, platform_vel:int=3, grupo_colisao:pygame.sprite.Group = None, horizontal:bool = True):
        """_summary_

        Args:
            x (float): posição x que a plataforma será colocada
            y (float): posição y que a plataforma será colocada
            variacao_x (tuple, optional): Variação na horizontal que a plataforma se movimenta. Defaults to None.
            variacao_y (tuple, optional): Variação na vertical que a plataforma se movimenta. Defaults to None.
            platform_vel (int, optional): Velocidade da plataforma. Defaults to 3.
            grupo_colisao (pygame.sprite.Group, optional): Grupo que pode colide com a plataforma. Defaults to None.
            horizontal (bool, optional): Movimentação horizontal da plataforma. Defaults to True.
        """

        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load("plataforma.png")
        self.rect = self.image.get_rect(center = (x,y))
        self.grupo_colisao = grupo_colisao
        self.platform_vel = platform_vel
        self.variacao_x = variacao_x
        self.variacao_y = variacao_y
        self.horizontal = horizontal
        
    
    def movimentar_plataforma(self, horizontal):
        """Função que movimenta a plataforma

        Args:
            horizontal (bool): Movimentação horizontal da plataforma
        """
        self.horizontal = horizontal
        if self.horizontal == True:
            x_min, x_max = self.variacao_x 
            if self.rect.left >=x_max or self.rect.left <= x_min:
                self.platform_vel*= -1
            self.rect.left += self.platform_vel
            rect_over = self.rect.copy()
            rect_over.y -= 1
            for personagens in self.grupo_colisao.sprites():
                if personagens.rect.colliderect(rect_over) and not personagens.rect.colliderect(self.rect):
                    personagens.rect.x += self.platform_vel
                    direita = personagens.direita
                    personagens.direita = self.platform_vel > 0
                    personagens.check_horizontal_collisions()
                    personagens.direita = direita
        else:
            y_min, y_max = self.variacao_y
            if self.rect.top >=y_max or self.rect.top <= y_min:
                self.platform_vel*= -1
            self.rect.bottom += self.platform_vel
            if self.platform_vel > 0:
                rect_over = self.rect.copy()
                rect_over.y -= 1 + 2*self.platform_vel
                for personagens in self.grupo_colisao.sprites():
                    if personagens.rect.colliderect(rect_over) and not personagens.rect.colliderect(self.rect):
                        personagens.rect.bottom = self.rect.top
                        personagens.check_vertical_collisions()
    
    def colisao(self):
        """
        Função que cria a colisão dos personagens com a plataforma
        """
        for personagem in self.grupo_colisao.sprites():
            if personagem.rect.left < self.rect.right and  personagem.rect.right > self.rect.left and personagem.rect.bottom > self.rect.top and personagem.rect.bottom < self.rect.bottom:
                if personagem.state != 1:
                    personagem.state = 0
                    print(self.rect.top)
                    personagem.rect.bottom = self.rect.top
    
        
    def update(self):
        self.colisao()
        self.movimentar_plataforma(self.horizontal)

        

class Plataforma_com_alavanca(Plataforma):
    def __init__(self, x:float, y:float, alavanca:Alavanca, variacao_x:tuple=None, variacao_y:tuple=None, platform_vel:int=3, grupo_colisao:pygame.sprite.Group=None, horizontal:bool=True):
        """_summary_

        Args:
            x (float): posição x que a plataforma será colocada
            y (float): posição y que a plataforma será colocada
            alavanca (Alavanca): Alavanca que caso ativada movimentará a plataforma
            variacao_x (tuple, optional): Variação na horizontal que a plataforma se movimenta. Defaults to None.
            variacao_y (tuple, optional): Variação na vertical que a plataforma se movimenta. Defaults to None.
            platform_vel (int, optional): Velocidade da plataforma. Defaults to 3.
            grupo_colisao (pygame.sprite.Group, optional): Grupo que pode colide com a plataforma. Defaults to None.
            horizontal (bool, optional): Movimentação horizontal da plataforma. Defaults to True.
        """
        super().__init__(x, y, variacao_x, variacao_y, platform_vel, grupo_colisao, horizontal)
        self.alavanca = alavanca


    def movimentar_condicional(self):
        """
            Função que movimenta a plataforma caso a alavanca ligada à ela esteja ativada
        """
        if self.alavanca.on == True:
            self.movimentar_plataforma(True)
    
    def update(self):
        self.colisao()
        self.movimentar_condicional()

class Botao(pygame.sprite.Sprite):
    def __init__(self, x:float, y:float, grupo_colisao: pygame.sprite.Group):
        """_summary_

        Args:
            x (float): posição x que a plataforma será colocada
            y (float): posição y que a plataforma será colocada
            grupo_colisao (pygame.sprite.Group): Grupo que colide com o botão
        """
        
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load("botao.png")
        self.rect = self.image.get_rect(midbottom = (x,y))
        self.ativo = False
        self.grupo_colisao = grupo_colisao
        self.rect_collision = self.rect


    
    def abaixar_botao(self):
        """
            Função que faz o botão ser abaixado
        """
        self.image = pygame.image.load("botao_apertado.png")
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))
        
        

    def apertar_botao(self):
        """
            Função que detecta a colisão com o grupo_colisao(personagens)
        """
        self.ativo = False
        for personagens in self.grupo_colisao.sprites():
            if personagens.rect.colliderect(self.rect_collision):
                self.abaixar_botao()
                self.ativo = True
        if not self.ativo:
            self.image = pygame.image.load("botao.png") 
            self.rect = self.image.get_rect(midbottom=(self.x, self.y))
    
    def update(self):
        self.apertar_botao(self)


    

