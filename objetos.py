import pygame
class Alavanca(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.on = False
        self.image = pygame.image.load("alavanca1.png")
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.alavanca_off = pygame.image.load("alavanca1.png")
        self.alavanca_on = pygame.transform.flip(self.alavanca_off, True, False)


    
    def desenhar(self, screen):
        if self.on:
            screen.blit(self.alavanca_on,(self.x,self.y))
        else:
            screen.blit(self.alavanca_off,(self.x,self.y))




class Chave():
    pass

    

class Plataforma():
    pass

class Porta():
    pass