import pygame
from tile import Tile
import personagem
import objetos

PERSONAGEM_ALTURA_EM_BLOCOS = 2


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
                        self.tiles.add(Tile((x, y), self.tile_size))
                    case 'B':
                        altura = PERSONAGEM_ALTURA_EM_BLOCOS * self.tile_size
                        self.boy = personagem.BoyNinja(
                            x, y, altura, self.tiles)
                        self.personagens.add(self.boy)
                    case 'G':
                        altura = PERSONAGEM_ALTURA_EM_BLOCOS * self.tile_size
                        self.girl = personagem.GirlNinja(
                            x, y, altura, self.screen, self.tiles)
                        self.personagens.add(self.girl)
                    case 'R':
                        altura = PERSONAGEM_ALTURA_EM_BLOCOS * self.tile_size
                        self.robo = personagem.Robo(
                            x, 120, y, altura, 20, self.tiles)
                        self.robos.add(self.robo)
                    case 'C':
                        self.chave = objetos.Chave(x, y, self.personagens)
                        self.chaves.add(self.chave)
                    case 'P':
                        self.portao = objetos.Portao(x, y, self.personagens, self.chaves, self.portoes)
                        self.portoes.add(self.portao)
                    case 'H':
                        self.plataforma = objetos.Plataforma(x, y,variacao_x=(x-100, x+100), grupo_colisao = self.personagens)
                        self.plataformas.add(self.plataforma)
                    case 'V':
                        self.plataforma = objetos.Plataforma(x, y,variacao_y=(y-100, y+100), grupo_colisao = self.personagens, horizontal=False)
                        self.plataformas.add(self.plataforma)
                    case 'A':
                        self.alavanca = objetos.Alavanca(x, y, self.personagens)
                        self.alavancas.add(self.alavanca)
                    case 'T':
                        self.botao = objetos.Botao(x+20,y+50, self.botoes, self.personagens)
                        self.botoes.add(self.botao)
                    case 'M':
                        alavancas = self.alavancas.sprites()
                        
                        self.plataforma_condicional = objetos.Plataforma_com_alavanca(x, y, alavanca=alavancas[0],variacao_x=(x-100, x+100), grupo_colisao = self.personagens)
                        self.plataformas_condicionais.add(self.plataforma_condicional)

    def draw(self):
        self.tiles.draw(self.screen)
        self.personagens.draw(self.screen)
        self.robos.draw(self.screen)
        self.alavancas.draw(self.screen)
        self.chaves.draw(self.screen)
        self.portoes.draw(self.screen)
        self.botoes.draw(self.screen)
        self.plataformas.draw(self.screen)
        self.plataformas_condicionais.draw(self.screen)





    def update(self):
        self.personagens.update()
        self.robos.update()
        self.alavancas.update()
        self.chaves.update()
        self.portoes.update()
        self.plataformas.update()
        self.botoes.update()
        self.plataformas_condicionais.update()