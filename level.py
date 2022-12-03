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
        self.visible_sprites = pygame.sprite.Group()
        self.active_sprites = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        self.personagens = pygame.sprite.Group()
        self.personagens_e_robos = pygame.sprite.Group()
        # TODO: Remover grupos desncecessários
        self.robos = pygame.sprite.Group()
        self.alavancas = pygame.sprite.Group()
        self.chaves = pygame.sprite.Group()
        self.portoes = pygame.sprite.Group()
        self.botoes = pygame.sprite.GroupSingle()
        self.plataformas = pygame.sprite.Group()
        self.plataformas_condicionais = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = self.inicio_x + col_index * self.tile_size
                y = row_index * self.tile_size
                match(col):
                    case 'X':
                        tile = Tile((x, y), self.tile_size)
                        self.tiles.add(tile)
                        self.visible_sprites.add(tile)
                    case 'B':
                        altura = self.tile_size
                        self.boy = personagem.BoyNinja(
                            x, y, altura, self.tiles)
                        self.personagens.add(self.boy)
                        self.personagens_e_robos.add(self.boy)
                        self.visible_sprites.add(self.boy)
                        self.active_sprites.add(self.boy)
                    case 'G':
                        altura = self.tile_size
                        self.girl = personagem.GirlNinja(
                            x, y, altura, self.screen, self.tiles)
                        self.personagens.add(self.girl)
                        self.personagens_e_robos.add(self.girl)
                        self.visible_sprites.add(self.girl)
                        self.active_sprites.add(self.girl)
                    case 'R':
                        altura = self.tile_size
                        robo = personagem.Robo(
                            x, 120, y, altura, 20, self.tiles)
                        self.robos.add(robo)
                        self.personagens_e_robos.add(robo)
                        self.visible_sprites.add(robo)
                        self.active_sprites.add(robo)
                    case 'C':
                        chave = objetos.Chave(
                            x, y, self.tile_size, self.personagens)
                        self.chaves.add(chave)
                        self.visible_sprites.add(chave)
                        self.active_sprites.add(chave)
                    case 'P':
                        portao = objetos.Portao(
                            x, y, self.tile_size, self.personagens, self.chaves, self.portoes)
                        self.portoes.add(portao)
                        self.visible_sprites.add(portao)
                        self.active_sprites.add(portao)
                    case 'H':
                        plataforma = objetos.Plataforma(x, y, variacao_x=(
                            x-100, x+100), grupo_colisao=self.personagens_e_robos)
                        self.plataformas.add(plataforma)
                        self.visible_sprites.add(plataforma)
                        self.active_sprites.add(plataforma)
                    case 'V':
                        plataforma = objetos.Plataforma(x, y, variacao_y=(
                            y-100, y+100), grupo_colisao=self.personagens_e_robos, horizontal=False)
                        self.plataformas.add(plataforma)
                        self.visible_sprites.add(plataforma)
                        self.active_sprites.add(plataforma)
                    case 'A':
                        alavanca = objetos.Alavanca(
                            x, y, self.tile_size, self.personagens)
                        self.alavancas.add(alavanca)
                        self.visible_sprites.add(alavanca)
                        self.active_sprites.add(alavanca)
                    case 'T':
                        botao = objetos.Botao(
                            x+20, y+50, self.botoes, self.personagens)
                        self.botoes.add(botao)
                        self.visible_sprites.add(botao)
                        self.active_sprites.add(botao)
                    case 'M':
                        alavancas = self.alavancas.sprites()

                        plataforma_condicional = objetos.Plataforma_com_alavanca(
                            x, y, alavanca=alavancas[0], variacao_x=(x-100, x+100), grupo_colisao=self.personagens_e_robos)
                        self.plataformas_condicionais.add(
                            plataforma_condicional)
                        self.visible_sprites.add(plataforma_condicional)
                        self.active_sprites.add(plataforma_condicional)

    def draw(self):
        self.visible_sprites.draw(self.screen)

    def update(self):
        self.active_sprites.update()
