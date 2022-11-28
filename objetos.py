import pygame
class Alavanca(pygame.sprite.Sprite):
    def __init__(self, x, y, grupo_colisao):
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



    def mudar_direcao(self):
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


            
class Chave(pygame.sprite.Sprite):
    def __init__(self, x, y, grupo_colisao):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load("chave.png"), (30,50)) 
        self.rect = self.image.get_rect(center = (x,y))
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
        self.rect = self.image.get_rect(center = (x,y))
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
class Botao():
    pass

class Plataforma(pygame.sprite.Sprite):
    # variacao_x e variacao_y são uma tupla com dois valores: máximos e mínimos de x e y
    # Se o movimento for horizontal=True colocar True, se for vertical colocar horizontal = False
    def __init__(self, x, y, variacao_x=None, variacao_y=None, platform_vel=3, grupo_colisao = None, horizontal = True):
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
        self.horizontal = horizontal
        if self.horizontal == True:
            x_min, x_max = self.variacao_x 
            if self.rect.left >=x_max or self.rect.left <= x_min:
                self.platform_vel*= -1
            self.rect.left += self.platform_vel
        else:
            y_min, y_max = self.variacao_y
            if self.rect.top >=y_max or self.rect.top <= y_min:
                self.platform_vel*= -1
            self.rect.bottom += self.platform_vel
    
        
    def update(self):
        self.movimentar_plataforma(self.horizontal)