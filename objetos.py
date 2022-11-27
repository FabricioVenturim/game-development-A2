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

    def ativar(self, personagem):
        if personagem.image.get_rect().colliderect(self.image.get_rect()) and self.on == False:
            self.on = True

    def desativar(self, personagem):
        if personagem.image.get_rect().colliderect(self.image.get_rect()) and self.on == True:
            self.on = False
    

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
            print(self.active)

    def update(self):
        self.pegar_chave(self.grupo_colisao)
    
class Plataforma():
    pass

class Porta():
    pass

