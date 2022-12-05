"""Esse módulo serve para testar as funcionalidades da classe Personagem."""

import sys
import os

sys.path.insert(0, './')

import pygame
import personagem
import unittest
from tile import Tile

pygame.init()
screen = pygame.display.set_mode((800, 600))

class MyTestCase(unittest.TestCase):
    def test_movimentacao_boy_direita(self):
        """Testa se o player boy se move para a esquerda"""
        self.robos = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        tile = Tile((20, 20), 2)
        self.tiles.add(tile)

        self.boy = personagem.BoyNinja(50, 50, 50, self.tiles, self.robos)

        self.boy.fun_correr_direita()

        #test
        expectativa = 50 + 8
        realidade = self.boy.rect.x

        # Assert
        self.assertAlmostEqual(expectativa, realidade)

    def test_movimentacao_girl_direita(self):
        """Testa se o player girl se move para a esquerda"""
        self.robos = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        tile = Tile((20, 20), 2)
        self.tiles.add(tile)
        self.alavancas = pygame.sprite.Group()

        self.girl = personagem.GirlNinja(50, 50, 50, screen, self.tiles, self.robos, self.alavancas)
        self.girl.fun_correr_direita()

        #test
        expectativa = 50 + 6
        realidade = self.girl.rect.x

        # Assert
        self.assertAlmostEqual(expectativa, realidade)

    def test_movimentacao_boy_esquerda(self):
        """Testa se o player boy se move para a esquerda"""
        self.robos = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        tile = Tile((20, 20), 2)
        self.tiles.add(tile)

        self.boy = personagem.BoyNinja(50, 50, 50, self.tiles, self.robos)

        self.boy.fun_correr_esquerda()

        #test
        expectativa = 50 - 2
        realidade = self.boy.rect.x

        # Assert
        self.assertAlmostEqual(expectativa, realidade)

    def test_fun_planar(self):
        """Testa se o boy ativa o planar"""
        self.robos = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        tile = Tile((20, 20), 2)
        self.tiles.add(tile)

        self.boy = personagem.BoyNinja(50, 50, 50, self.tiles, self.robos)

        self.boy.fun_planar()

        #test
        expectativa = True
        realidade = self.boy.planar

        # Assert
        self.assertAlmostEqual(expectativa, realidade)

    def test_fun_planar_gravidade(self):
        """Testa se o boy possui gravidade ao ativar o planar"""
        self.robos = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        tile = Tile((20, 20), 2)
        self.tiles.add(tile)

        self.boy = personagem.BoyNinja(50, 50, 50, self.tiles, self.robos)


        self.boy.fun_planar()

        #test
        expectativa = 2
        realidade = self.boy.state

        # Assert
        self.assertAlmostEqual(expectativa, realidade)

    def teste_fun_deslizar_ativa(self):
        """Testa se o player girl corre mais ao ativar o deslizar"""
        self.robos = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        tile = Tile((20, 20), 2)
        self.tiles.add(tile)
        self.alavancas = pygame.sprite.Group()

        self.girl = personagem.GirlNinja(50, 50, 50, screen, self.tiles, self.robos, self.alavancas)
        self.girl.fun_deslizar()

        #test
        expectativa = True
        realidade = self.girl.deslizar

        # Assert
        self.assertAlmostEqual(expectativa, realidade)

    def test_movimentacao_girl_esquerda(self):
        """Testa se o player girl se move para a esquerda"""
        self.robos = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        tile = Tile((20, 20), 2)
        self.tiles.add(tile)
        self.alavancas = pygame.sprite.Group()

        self.girl = personagem.GirlNinja(50, 50, 50, screen, self.tiles, self.robos, self.alavancas)

        self.girl.fun_correr_esquerda()

        #test
        expectativa = 50 - 4
        realidade = self.girl.rect.x

        # Assert
        self.assertAlmostEqual(expectativa, realidade)

    def test_bater_boy(self):
        """Testa se o player boy bate"""

        self.robos = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        tile = Tile((20, 20), 2)
        self.tiles.add(tile)

        self.boy = personagem.BoyNinja(50, 50, 50, self.tiles, self.robos)


        self.boy.fun_bater()

        #test
        expectativa = True
        realidade = self.boy.bater

        # Assert
        self.assertAlmostEqual(expectativa, realidade)

    def test_verifica_player_mesma_altura_fora_longe_direita(self):
        """Testa se o robo não vê o player se estiver na mesma altura a direita"""
        self.personagens = pygame.sprite.Group()
        self.robos = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        tile = Tile((20, 20), 2)
        self.tiles.add(tile)

        self.boy = personagem.BoyNinja(800, 200, 50, self.tiles, self.robos)

        self.robo = personagem.Robo(500, 100, 200, 1, 100, self.tiles, False, False)
        self.robos.add(self.robo)

        #test
        expectativa = False
        realidade = self.robo.verifica_player(self.boy)

        # Assert
        self.assertAlmostEqual(expectativa, realidade)

    def test_verifica_player_mesma_altura_fora_longe_esquerda(self):
        """Testa se o robo não vê o player se estiver na mesma altura a esquerda"""
        self.personagens = pygame.sprite.Group()
        self.robos = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        tile = Tile((20, 20), 2)
        self.tiles.add(tile)

        self.boy = personagem.BoyNinja(100, 200, 50, self.tiles, self.robos)

        self.robo = personagem.Robo(400, 100, 200, 1, 100, self.tiles, False, True)
        self.robos.add(self.robo)

        #test
        expectativa = False
        realidade = self.robo.verifica_player(self.boy)

        # Assert
        self.assertAlmostEqual(expectativa, realidade)

    def test_verifica_player_mesma_altura_fora_perto_direita(self):
        """Testa se o robo não vê o player se estiver na mesma altura a direita bem perto"""
        self.personagens = pygame.sprite.Group()
        self.robos = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        tile = Tile((20, 20), 2)
        self.tiles.add(tile)

        self.boy = personagem.BoyNinja(610, 200, 50, self.tiles, self.robos)

        self.robo = personagem.Robo(500, 100, 200, 1, 100, self.tiles, False, True)
        self.robos.add(self.robo)

        #test
        expectativa = False
        realidade = self.robo.verifica_player(self.boy)

        # Assert
        self.assertAlmostEqual(expectativa, realidade)

    def test_verifica_player_mesma_altura_fora_perto_esquerda(self):
        """Testa se o robo não vê o player se estiver na mesma altura a esquerda bem perto"""
        self.personagens = pygame.sprite.Group()
        self.robos = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        tile = Tile((20, 20), 2)
        self.tiles.add(tile)

        self.boy = personagem.BoyNinja(290, 200, 50, self.tiles, self.robos)

        self.robo = personagem.Robo(400, 100, 200, 2, 100, self.tiles, False, False)
        self.robos.add(self.robo)

        self.robo.verifica_player(self.boy)

        #test
        expectativa = False
        realidade = self.robo.verifica_player(self.boy)

        # Assert
        self.assertAlmostEqual(expectativa, realidade)

    def test_verifica_player_mesma_altura_fora_atrás_esquerda(self):
        """Testa se o robo não vê o player se ele estiver atrás do robô a esquerda"""
        self.personagens = pygame.sprite.Group()
        self.robos = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        tile = Tile((20, 20), 2)
        self.tiles.add(tile)

        self.boy = personagem.BoyNinja(350, 200, 50, self.tiles, self.robos)

        self.robo = personagem.Robo(400, 100, 200, 2, 100, self.tiles, False, False)
        self.robos.add(self.robo)

        self.robo.verifica_player(self.boy)

        #test
        expectativa = False
        realidade = self.robo.verifica_player(self.boy)

        # Assert
        self.assertAlmostEqual(expectativa, realidade)

    def test_verifica_player_mesma_altura_fora_atrás_direita(self):
        """Testa se o robo não vê o player se ele estiver atrás do robô a direita"""
        self.personagens = pygame.sprite.Group()
        self.robos = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        tile = Tile((20, 20), 2)
        self.tiles.add(tile)

        self.boy = personagem.BoyNinja(450, 200, 50, self.tiles, self.robos)

        self.robo = personagem.Robo(400, 100, 200, 2, 100, self.tiles, False, True)
        self.robos.add(self.robo)

        self.robo.verifica_player(self.boy)

        self.robo.verifica_player(self.boy)

        #test
        expectativa = False
        realidade = self.robo.verifica_player(self.boy)

        # Assert
        self.assertAlmostEqual(expectativa, realidade)
    
    def test_verifica_player_altura_diferente(self):
        """Testa se o robo não vê o player se ele estiver em uma altura diferente"""
        self.personagens = pygame.sprite.Group()
        self.robos = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        tile = Tile((20, 20), 2)
        self.tiles.add(tile)

        self.boy = personagem.BoyNinja(350, 500, 50, self.tiles, self.robos)

        self.robo = personagem.Robo(400, 100, 200, 2, 100, self.tiles, False, True)
        self.robos.add(self.robo)

        self.robo.verifica_player(self.boy)

        self.robo.verifica_player(self.boy)

        #test
        expectativa = False
        realidade = self.robo.verifica_player(self.boy)

        # Assert
        self.assertAlmostEqual(expectativa, realidade)

    def test_verifica_player_dentro_direita(self):
        """Testa se o robo vê player no campo de visão pela direita"""
        self.personagens = pygame.sprite.Group()
        self.robos = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        tile = Tile((20, 20), 2)
        self.tiles.add(tile)

        self.boy = personagem.BoyNinja(450, 200, 50, self.tiles, self.robos)

        self.robo = personagem.Robo(400, 100, 200, 2, 100, self.tiles, False, False)
        self.robos.add(self.robo)

        self.robo.verifica_player(self.boy)

        self.robo.verifica_player(self.boy)

        #test
        expectativa = True
        realidade = self.robo.verifica_player(self.boy)

        # Assert
        self.assertAlmostEqual(expectativa, realidade)

    def test_verifica_player_dentro_esquerda(self):
        """Testa se o robo vê player no campo de visão pela esquerda"""
        self.personagens = pygame.sprite.Group()
        self.robos = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        tile = Tile((20, 20), 2)
        self.tiles.add(tile)

        self.boy = personagem.BoyNinja(350, 200, 50, self.tiles, self.robos)

        self.robo = personagem.Robo(400, 100, 200, 2, 100, self.tiles, False, True)
        self.robos.add(self.robo)

        self.robo.verifica_player(self.boy)

        self.robo.verifica_player(self.boy)

        #test
        expectativa = True
        realidade = self.robo.verifica_player(self.boy)

        # Assert
        self.assertAlmostEqual(expectativa, realidade)


if __name__ == '__main__':
    unittest.main(verbosity=2)
