import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        # Um bloco branco como placeholder
        self.image = pygame.Surface((size, size))
        self.image.fill((255, 255, 255))
        
        self.rect = self.image.get_rect(topleft=pos)