import pygame
from tile import Tile
import personagem


class Level:
    def __init__(self, level_data, surface):
        self.screen = surface
        width, height = surface.get_size()
        self.tile_size = height / len(level_data)
        largura_level = len(max(level_data, key=len)) * self.tile_size
        self.inicio_x = (width - largura_level) / 2
        self.setup_level(level_data)

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.personagens = pygame.sprite.Group()
        self.robos = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = self.inicio_x + col_index * self.tile_size
                y = row_index * self.tile_size
                match(col):
                    case 'X':
                        self.tiles.add(Tile((x, y), self.tile_size))
                    case 'B':
                        self.boy = personagem.BoyNinja(x, y, self.tiles)
                        self.personagens.add(self.boy)
                    case 'G':
                        # TODO: implementar escalabilidade de tamanho dos personagens
                        self.girl = personagem.GirlNinja(x, y, self.screen, self.tiles)
                        self.personagens.add(self.girl)
                    case 'R':
                        self.robo = personagem.Robo(x, 100, y, 20, self.tiles)
                        self.robos.add(self.robo)

    def draw(self):
        self.tiles.draw(self.screen)
        self.personagens.draw(self.screen)
        self.robos.draw(self.screen)

    def update(self):
        self.personagens.update()
        self.robos.update()
