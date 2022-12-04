import pygame
from math import ceil

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        rounded_up = ceil(size)
        # Um bloco branco como placeholder
        self.image = pygame.Surface((rounded_up, rounded_up))
        self.image.fill((255, 255, 255))
        
        self.rect = self.image.get_rect(topleft=pos)
