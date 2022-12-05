import pygame
from tile import Tile
import personagem
import objetos


class Level:
    def __init__(self, level_data, surface):
        level_map = level_data['level_map']
        self.screen = surface
        width, height = surface.get_size()
        self.tile_size = height / (len(level_map) - 1)
        largura_level = len(max(level_map, key=len)) * self.tile_size
        self.inicio_x = (width - largura_level) / 2
        self.inicio_y = -self.tile_size
        self.setup_level(level_data)
        self.perdeu = False
        self.venceu = False

        fonte = pygame.font.Font("font/Pixeltype.ttf", int(height / 10))
        self.texto = fonte.render("Pegue a chave!", True, (255, 255, 255))
        self.texto_saida = fonte.render("Saia pela porta!", True, (255, 255, 255))

        padding = int(height / 100)
        self.texto_pos = (self.inicio_x + self.tile_size + padding, padding)
        
        background = pygame.image.load("img/bg.png").convert()
        largura, altura = background.get_size()
        bg_width = largura * height / altura
        self.background = pygame.transform.scale(background, (bg_width, height))
        
        right_wall = pygame.image.load("img/wall.png").convert()
        largura, altura = right_wall.get_size()
        fator = height / altura
        wall_width = largura * fator
        self.right_wall = pygame.transform.scale(right_wall, (wall_width, height))
        self.left_wall = pygame.transform.flip(self.right_wall, True, True)
        self.left_wall_x = self.inicio_x - wall_width + self.tile_size
        self.right_wall_x = self.inicio_x + largura_level - self.tile_size

        ground = pygame.image.load("img/ground.png").convert_alpha()
        largura_ground, altura_ground = ground.get_size()
        self.ground = pygame.transform.scale(ground, (largura_ground * fator, altura_ground * fator))
        self.ground_y = height - int(self.tile_size * 1.4)

    def setup_level(self, level_data):
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

        level_map = level_data['level_map']
        sprite_settings = level_data['sprite_settings']
        counter = {
            'R': 0,
            'H': 0,
            'V': 0,
            'M': 0
        }

        for row_index, row in enumerate(level_map):
            for col_index, col in enumerate(row):
                x = self.inicio_x + col_index * self.tile_size
                y = self.inicio_y + row_index * self.tile_size
                match(col):
                    case 'X':
                        tile = Tile((x, y), self.tile_size)
                        self.tiles.add(tile)
                        self.visible_sprites.add(tile)
                    case 'B':
                        altura = self.tile_size
                        self.boy = personagem.BoyNinja(
                            x, y, altura, self.tiles, self.robos)
                        self.personagens.add(self.boy)
                        self.personagens_e_robos.add(self.boy)
                        self.visible_sprites.add(self.boy)
                        self.active_sprites.add(self.boy)
                    case 'G':
                        altura = self.tile_size
                        self.girl = personagem.GirlNinja(
                            x, y, altura, self.screen, self.tiles, self.robos, self.alavancas)
                        self.personagens.add(self.girl)
                        self.personagens_e_robos.add(self.girl)
                        self.visible_sprites.add(self.girl)
                        self.active_sprites.add(self.girl)
                        self.visible_sprites.add(self.girl.kunai)
                    case 'R':
                        settings = sprite_settings[col][counter[col]]
                        counter[col] += 1
                        robo = personagem.Robo(x=x, y=y, tile_size=self.tile_size, collision_sprites=self.tiles, **settings)
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
                        settings = sprite_settings[col][counter[col]]
                        counter[col] += 1
                        plataforma = objetos.Plataforma(x, y, self.tile_size, grupo_colisao=self.personagens_e_robos, **settings)
                        self.plataformas.add(plataforma)
                        self.visible_sprites.add(plataforma)
                        self.active_sprites.add(plataforma)
                    case 'V':
                        settings = sprite_settings[col][counter[col]]
                        counter[col] += 1
                        plataforma = objetos.Plataforma(x, y, self.tile_size, grupo_colisao=self.personagens_e_robos, horizontal=False, **settings)
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
                            x, y, self.tile_size, self.botoes, self.personagens)
                        self.botoes.add(botao)
                        self.visible_sprites.add(botao)
                        self.active_sprites.add(botao)
                    case 'M':
                        settings = sprite_settings[col][counter[col]]
                        counter[col] += 1

                        plataforma_condicional = objetos.Plataforma_com_alavanca(
                            x, y, self.tile_size, grupo_colisao=self.personagens_e_robos, **settings)
                        self.plataformas_condicionais.add(
                            plataforma_condicional)
                        self.visible_sprites.add(plataforma_condicional)
                        self.active_sprites.add(plataforma_condicional)

        connections = level_data['connections']
        for plataforma_index, connection in enumerate(connections):
            alavancas_index = connection['A']
            botoes_index = connection['T']
            alavancas = []
            botoes = []

            for index in alavancas_index:
                alavancas.append(self.alavancas.sprites()[index])

            for index in botoes_index:
                botoes.append(self.botoes.sprites()[index])
            
            self.plataformas_condicionais.sprites()[plataforma_index].ativadores = alavancas + botoes
            
    def checa_derrota(self):
        for robo in self.robos:
            for personagem in self.personagens:
                if robo.verifica_player(personagem):
                    self.perdeu = True
                    return
    
    def checa_vitoria(self):
        for portao in self.portoes:
            portao.verificar_personagens_portao()
            if portao.liberar_fase:
                self.venceu = True
                return
    
    def checa_chaves(self):
        if len(self.chaves) == 0:
            self.texto = self.texto_saida

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.visible_sprites.draw(self.screen)
        self.screen.blit(self.ground, (0, self.ground_y))
        self.screen.blit(self.left_wall, (self.left_wall_x, 0))
        self.screen.blit(self.right_wall, (self.right_wall_x, 0))
        self.screen.blit(self.texto, self.texto_pos)

    def update(self):
        self.active_sprites.update()
        self.checa_vitoria()
        self.checa_derrota()
        self.checa_chaves()