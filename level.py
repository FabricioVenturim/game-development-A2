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
                        # TODO: colocar inicializações dentro das classes de personagem
                        dict_animacoes_boy = {"parado": [0, 232, 455, 10, 3.1], "correndo": [5940, 363, 455, 10, 3.1], "pulando": [
                            2325, 362, 483, 10, 3.1], "batendo": [19410, 536, 495, 10, 3.1], "voando": [24787, 443, 454, 10, 3.1]}
                        self.boy = personagem.BoyNinja(
                            x, y, "img/spritesheet_boy.png", dict_animacoes_boy)
                        self.personagens.add(self.boy)
                    case 'G':
                        dict_animacoes_girl = {"parado": [0, 290, 500, 10, 3.5], "correndo": [6906, 372, 500, 10, 3.5], "pulando": [
                            2910, 399, 500, 10, 3.5], "deslizando": [16425, 397, 401, 10, 3.5], "ataque": [20400, 383, 514, 10, 3.5]}
                        # TODO: implementar escalabilidade de tamanho dos personagens
                        self.girl = personagem.GirlNinja(
                            x, y, "img/spritesheet_girl.png", dict_animacoes_girl, self.screen)
                        self.personagens.add(self.girl)
                    case 'R':
                        # TODO: separar movimento vertical e horizontal o robo
                        dict_animacoes_robo = {"parado": [0, 567, 555, 10, 3.5], "correndo": [
                            5670, 567, 550, 8, 3.5], "morrendo": [10190, 562, 519, 10, 3.5]}
                        self.robo = personagem.Robo(
                            x, y, 200, 280, "img/spritesheet_robo.png", dict_animacoes_robo)
                        self.robos.add(self.robo)

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
                    # TODO: alterar pulo de personagem
                    pers.rect.top = sprite.rect.bottom + 1
                    pers.aceleracao = -1
                else:
                    pers.rect.bottom = sprite.rect.top
                    pers.state = 0

    def draw(self):
        self.tiles.draw(self.screen)
        self.personagens.draw(self.screen)
        self.robos.draw(self.screen)

    def read_input(self):
        self.boy.read_input()
        self.girl.read_input()

    def sprites_collisions_horizontal(self, group):
        for sprite in group.sprites():
            self.horizontal_movement_collision(sprite)

    def sprites_collisions_vertical(self, group):
        for sprite in group.sprites():
            self.vertical_movement_collision(sprite)

    def update(self):
        self.read_input()
        self.sprites_collisions_horizontal(self.personagens)
        self.personagens.update()
        self.robos.update()
        self.sprites_collisions_horizontal(self.robos)
        self.sprites_collisions_vertical(self.robos)
        self.sprites_collisions_vertical(self.personagens)
