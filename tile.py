import pygame
from math import ceil

class Tile(pygame.sprite.Sprite):
    image = None
    size = 0

    def __init__(self, pos, size):
        super().__init__()
        rounded_up = ceil(size)
        
        if Tile.image is None or size != rounded_up:
            Tile.image = pygame.image.load("img/tile.png").convert()
            Tile.image = pygame.transform.scale(Tile.image, (rounded_up, rounded_up))
            Tile.size = rounded_up
        
        self.rect = Tile.image.get_rect(topleft=pos)
