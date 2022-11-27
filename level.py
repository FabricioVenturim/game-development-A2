import pygame
from tile import Tile
import personagem
import objetos


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
        self.alavancas = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = self.inicio_x + col_index * self.tile_size
                y = row_index * self.tile_size
                match(col):
                    case 'X':
                        self.tiles.add(Tile((x, y), self.tile_size))
                    case 'B':
                        self.boy = personagem.BoyNinja(x, y)
                        self.personagens.add(self.boy)
                    case 'G':
                        # TODO: implementar escalabilidade de tamanho dos personagens
                        self.girl = personagem.GirlNinja(x, y, self.screen)
                        self.personagens.add(self.girl)
                    case 'R':
                        self.robo = personagem.Robo(x, y, 200, 280)
                        self.robos.add(self.robo)
                    case 'A':
                        self.alavanca = objetos.Alavanca(x, y)
                        self.alavancas.add(self.alavanca)

    def horizontal_movement_collision(self, pers):
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(pers.rect):
                if pers.direita:
                    pers.rect.right = sprite.rect.left
                else:
                    pers.rect.left = sprite.rect.right

    def vertical_movement_collision(self, pers):
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(pers.rect):
                if pers.state == 1:
                    pers.rect.top = sprite.rect.bottom + 1
                    pers.aceleracao = -1
                else:
                    pers.rect.bottom = sprite.rect.top
                    pers.state = 0
                    pers.aceleracao = pers.aceleracao_pulo_inicial
                    pers.planar = False

    def draw(self):
        self.tiles.draw(self.screen)
        self.personagens.draw(self.screen)
        self.robos.draw(self.screen)
        self.alavancas.draw(self.screen)

    def read_input(self):
        self.boy.read_input()
        self.girl.read_input()

    def sprites_collisions_horizontal(self, group):
        for sprite in group.sprites():
            self.horizontal_movement_collision(sprite)

    def sprites_collisions_vertical(self, group):
        for sprite in group.sprites():
            self.vertical_movement_collision(sprite)

    def ativar_alavanca(self, pers):
        for alavanca in self.alavancas.sprites():
            if alavanca.rect.colliderect(pers.rect):
                self.alavanca.on = True
                self.alavanca.image = self.alavanca.alavanca_on
    
    def colisao_alavanca(self, group):
        for sprite in group.sprites():
            self.ativar_alavanca(sprite)


    def update(self):
        self.read_input()
        self.sprites_collisions_horizontal(self.personagens)
        self.personagens.update()
        self.robos.update()
        self.alavancas.update()
        self.sprites_collisions_horizontal(self.robos)
        for robo in self.robos.sprites():
            robo.update_vertical_pos()
        self.sprites_collisions_vertical(self.robos)
        self.sprites_collisions_vertical(self.personagens)
        self.colisao_alavanca(self.personagens)
