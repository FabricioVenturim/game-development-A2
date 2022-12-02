"""Esse módulo serve para testar as funcionalidades da classe Personagem."""

import sys
import os

sys.path.insert(0, './')

import pygame
import personagem
import unittest

pygame.init()
screen = pygame.display.set_mode((800, 600))

class MyTestCase(unittest.TestCase):
    def test_movimentacao_boy_direita(self):
        """Testa se o player boy se move para a esquerda"""
        dict_animacoes_boy = {"parado": [0, 232, 455, 10, 3.1], "correndo": [5940, 363, 455, 10, 3.1], "pulando": [2325, 362, 483, 10, 3.1], "batendo": [19410, 536, 495, 10, 3.1], "voando": [24787,443, 454, 10, 3.1]}
        self.sprites_boy = pygame.sprite.Group()
        self.boy = personagem.BoyNinja(50, 50, "img/spritesheet_boy.png", dict_animacoes_boy)
        self.sprites_boy.add(self.boy)

        self.boy.fun_correr_direita()

        #test
        espectativa = 50 + 6
        realidade = self.boy.rect.x

        # Assert
        self.assertAlmostEqual(espectativa, realidade)

    def test_movimentacao_girl_direita(self):
        """Testa se o player girl se move para a esquerda"""
        dict_animacoes_girl = {"parado": [0, 232, 455, 10, 3.1], "correndo": [5940, 363, 455, 10, 3.1], "pulando": [2325, 362, 483, 10, 3.1], "batendo": [19410, 536, 495, 10, 3.1], "voando": [24787,443, 454, 10, 3.1]}
        self.sprites_girl = pygame.sprite.Group()
        self.girl = personagem.GirlNinja(50, 50, "img/spritesheet_boy.png", dict_animacoes_girl, screen)
        self.sprites_girl.add(self.girl)

        self.girl.fun_correr_direita()

        #test
        espectativa = 50 + 6
        realidade = self.girl.rect.x

        # Assert
        self.assertAlmostEqual(espectativa, realidade)

    def test_movimentacao_boy_esquerda(self):
        """Testa se o player boy se move para a esquerda"""
        dict_animacoes_boy = {"parado": [0, 232, 455, 10, 3.1], "correndo": [5940, 363, 455, 10, 3.1], "pulando": [2325, 362, 483, 10, 3.1], "batendo": [19410, 536, 495, 10, 3.1], "voando": [24787,443, 454, 10, 3.1]}
        self.sprites_boy = pygame.sprite.Group()
        self.boy = personagem.BoyNinja(50, 50, "img/spritesheet_boy.png", dict_animacoes_boy)
        self.sprites_boy.add(self.boy)

        self.boy.fun_correr_esquerda()

        #test
        espectativa = 50 - 6
        realidade = self.boy.rect.x

        # Assert
        self.assertAlmostEqual(espectativa, realidade)

    def test_fun_planar(self):
        """Testa se o boy ativa o planar"""
        dict_animacoes_boy = {"parado": [0, 232, 455, 10, 3.1], "correndo": [5940, 363, 455, 10, 3.1], "pulando": [2325, 362, 483, 10, 3.1], "batendo": [19410, 536, 495, 10, 3.1], "voando": [24787,443, 454, 10, 3.1]}
        self.sprites_boy = pygame.sprite.Group()
        self.boy = personagem.BoyNinja(50, 50, "img/spritesheet_boy.png", dict_animacoes_boy)
        self.sprites_boy.add(self.boy)

        self.boy.fun_planar()

        #test
        espectativa = True
        realidade = self.boy.planar

        # Assert
        self.assertAlmostEqual(espectativa, realidade)

    def test_fun_planar_gravidade(self):
        """Testa se o boy possui gravidade ao ativar o planar"""
        dict_animacoes_boy = {"parado": [0, 232, 455, 10, 3.1], "correndo": [5940, 363, 455, 10, 3.1], "pulando": [2325, 362, 483, 10, 3.1], "batendo": [19410, 536, 495, 10, 3.1], "voando": [24787,443, 454, 10, 3.1]}
        self.sprites_boy = pygame.sprite.Group()
        self.boy = personagem.BoyNinja(50, 50, "img/spritesheet_boy.png", dict_animacoes_boy)
        self.sprites_boy.add(self.boy)

        self.boy.fun_planar()

        #test
        espectativa = 2
        realidade = self.boy.state

        # Assert
        self.assertAlmostEqual(espectativa, realidade)

    def teste_fun_deslizar_ativa(self):
        """Testa se o player girl corre mais ao ativar o deslizar"""
        dict_animacoes_girl = {"parado": [0, 232, 455, 10, 3.1], "correndo": [5940, 363, 455, 10, 3.1], "pulando": [2325, 362, 483, 10, 3.1], "batendo": [19410, 536, 495, 10, 3.1], "voando": [24787,443, 454, 10, 3.1]}
        self.sprites_girl = pygame.sprite.Group()
        self.girl = personagem.GirlNinja(50, 50, "img/spritesheet_boy.png", dict_animacoes_girl, screen)
        self.sprites_girl.add(self.girl)

        self.girl.fun_correr_esquerda()

        #test
        espectativa = 2
        realidade = self.girl.state

        # Assert
        self.assertAlmostEqual(espectativa, realidade)

    def test_movimentacao_girl_esquerda(self):
        """Testa se o player girl se move para a esquerda"""
        dict_animacoes_girl = {"parado": [0, 232, 455, 10, 3.1], "correndo": [5940, 363, 455, 10, 3.1], "pulando": [2325, 362, 483, 10, 3.1], "batendo": [19410, 536, 495, 10, 3.1], "voando": [24787,443, 454, 10, 3.1]}
        self.sprites_girl = pygame.sprite.Group()
        self.girl = personagem.BoyNinja(50, 50, "img/spritesheet_boy.png", dict_animacoes_girl)
        self.sprites_girl.add(self.girl)

        self.girl.fun_correr_esquerda()

        #test
        espectativa = 50 - 6
        realidade = self.girl.rect.x

        # Assert
        self.assertAlmostEqual(espectativa, realidade)

    def test_bater_boy(self):
        """Testa se o player boy bate"""

        dict_animacoes_boy = {"parado": [0, 232, 455, 10, 3.1], "correndo": [5940, 363, 455, 10, 3.1], "pulando": [2325, 362, 483, 10, 3.1], "batendo": [19410, 536, 495, 10, 3.1], "voando": [24787,443, 454, 10, 3.1]}
        self.sprites_boy = pygame.sprite.Group()
        self.boy = personagem.BoyNinja(50, 50, "img/spritesheet_boy.png", dict_animacoes_boy)
        self.sprites_boy.add(self.boy)

        self.boy.fun_bater()

        #test
        espectativa = True
        realidade = self.boy.bater

        # Assert
        self.assertAlmostEqual(espectativa, realidade)

    def test_verifica_player_mesma_altura_fora_longe_direita(self):
        """Testa se o robo não vê o player se estiver na mesma altura a direita"""
        x = 50
        y = 100
        dict_animacoes_boy = {"parado": [0, 232, 455, 10, 3.1], "correndo": [5940, 363, 455, 10, 3.1], "pulando": [2325, 362, 483, 10, 3.1], "batendo": [19410, 536, 495, 10, 3.1], "voando": [24787,443, 454, 10, 3.1]}
        self.sprites_boy = pygame.sprite.Group()
        self.boy = personagem.BoyNinja(x, y, "img/spritesheet_boy.png", dict_animacoes_boy)
        self.sprites_boy.add(self.boy)

        dict_animacoes_robo= {"parado": [0, 567, 555, 10, 3.5], "correndo": [5670, 567, 550, 8, 3.5], "morrendo": [10190 , 562, 519, 10,3.5]}
        self.sprites_robo = pygame.sprite.Group()
        self.robo = personagem.Robo(800, 450, 100, 100, "img/spritesheet_robo.png", dict_animacoes_robo, direita_movimentacao = False)
        self.sprites_robo.add(self.robo)

        self.robo.verifica_player(self.boy)

        #test
        espectativa = False
        realidade = self.robo.verifica_player(self.boy)

        # Assert
        self.assertAlmostEqual(espectativa, realidade)

    def test_verifica_player_mesma_altura_fora_longe_esquerda(self):
        """Testa se o robo não vê o player se estiver na mesma altura a esquerda"""
        x = 1200
        y = 100
        dict_animacoes_boy = {"parado": [0, 232, 455, 10, 3.1], "correndo": [5940, 363, 455, 10, 3.1], "pulando": [2325, 362, 483, 10, 3.1], "batendo": [19410, 536, 495, 10, 3.1], "voando": [24787,443, 454, 10, 3.1]}
        self.sprites_boy = pygame.sprite.Group()
        self.boy = personagem.BoyNinja(x, y, "img/spritesheet_boy.png", dict_animacoes_boy)
        self.sprites_boy.add(self.boy)

        dict_animacoes_robo= {"parado": [0, 567, 555, 10, 3.5], "correndo": [5670, 567, 550, 8, 3.5], "morrendo": [10190 , 562, 519, 10,3.5]}
        self.sprites_robo = pygame.sprite.Group()
        self.robo = personagem.Robo(800, 450, 100, 100, "img/spritesheet_robo.png", dict_animacoes_robo, direita_movimentacao = False)
        self.sprites_robo.add(self.robo)

        self.robo.verifica_player(self.boy)

        #test
        espectativa = False
        realidade = self.robo.verifica_player(self.boy)

        # Assert
        self.assertAlmostEqual(espectativa, realidade)

    def test_verifica_player_mesma_altura_fora_perto_direita(self):
        """Testa se o robo não vê o player se estiver na mesma altura a direita bem perto"""
        x = 700
        y = 100
        dict_animacoes_boy = {"parado": [0, 232, 455, 10, 3.1], "correndo": [5940, 363, 455, 10, 3.1], "pulando": [2325, 362, 483, 10, 3.1], "batendo": [19410, 536, 495, 10, 3.1], "voando": [24787,443, 454, 10, 3.1]}
        self.sprites_boy = pygame.sprite.Group()
        self.boy = personagem.BoyNinja(x, y, "img/spritesheet_boy.png", dict_animacoes_boy)
        self.sprites_boy.add(self.boy)

        dict_animacoes_robo= {"parado": [0, 567, 555, 10, 3.5], "correndo": [5670, 567, 550, 8, 3.5], "morrendo": [10190 , 562, 519, 10,3.5]}
        self.sprites_robo = pygame.sprite.Group()
        self.robo = personagem.Robo(800, 450, 100, 100, "img/spritesheet_robo.png", dict_animacoes_robo, direita_movimentacao = False)
        self.sprites_robo.add(self.robo)

        self.robo.verifica_player(self.boy)

        #test
        espectativa = False
        realidade = self.robo.verifica_player(self.boy)

        # Assert
        self.assertAlmostEqual(espectativa, realidade)

    def test_verifica_player_mesma_altura_fora_perto_esquerda(self):
        """Testa se o robo não vê o player se estiver na mesma altura a esquerda bem perto"""
        x = 900
        y = 100
        dict_animacoes_boy = {"parado": [0, 232, 455, 10, 3.1], "correndo": [5940, 363, 455, 10, 3.1], "pulando": [2325, 362, 483, 10, 3.1], "batendo": [19410, 536, 495, 10, 3.1], "voando": [24787,443, 454, 10, 3.1]}
        self.sprites_boy = pygame.sprite.Group()
        self.boy = personagem.BoyNinja(x, y, "img/spritesheet_boy.png", dict_animacoes_boy)
        self.sprites_boy.add(self.boy)

        dict_animacoes_robo= {"parado": [0, 567, 555, 10, 3.5], "correndo": [5670, 567, 550, 8, 3.5], "morrendo": [10190 , 562, 519, 10,3.5]}
        self.sprites_robo = pygame.sprite.Group()
        self.robo = personagem.Robo(800, 450, 100, 100, "img/spritesheet_robo.png", dict_animacoes_robo, direita_movimentacao = False)
        self.sprites_robo.add(self.robo)

        self.robo.verifica_player(self.boy)

        #test
        espectativa = False
        realidade = self.robo.verifica_player(self.boy)

        # Assert
        self.assertAlmostEqual(espectativa, realidade)

    def test_verifica_player_mesma_altura_fora_atrás_esquerda(self):
        """Testa se o robo não vê o player se ele estiver atrás do robô a esquerda"""
        x = 850
        y = 100
        dict_animacoes_boy = {"parado": [0, 232, 455, 10, 3.1], "correndo": [5940, 363, 455, 10, 3.1], "pulando": [2325, 362, 483, 10, 3.1], "batendo": [19410, 536, 495, 10, 3.1], "voando": [24787,443, 454, 10, 3.1]}
        self.sprites_boy = pygame.sprite.Group()
        self.boy = personagem.BoyNinja(x, y, "img/spritesheet_boy.png", dict_animacoes_boy)
        self.sprites_boy.add(self.boy)

        dict_animacoes_robo= {"parado": [0, 567, 555, 10, 3.5], "correndo": [5670, 567, 550, 8, 3.5], "morrendo": [10190 , 562, 519, 10,3.5]}
        self.sprites_robo = pygame.sprite.Group()
        self.robo = personagem.Robo(800, 450, 100, 100, "img/spritesheet_robo.png", dict_animacoes_robo, direita_movimentacao = True)
        self.sprites_robo.add(self.robo)

        self.robo.verifica_player(self.boy)

        #test
        espectativa = False
        realidade = self.robo.verifica_player(self.boy)

        # Assert
        self.assertAlmostEqual(espectativa, realidade)

    def test_verifica_player_mesma_altura_fora_atrás_direita(self):
        """Testa se o robo não vê o player se ele estiver atrás do robô a direita"""
        x = 750
        y = 100

        dict_animacoes_boy = {"parado": [0, 232, 455, 10, 3.1], "correndo": [5940, 363, 455, 10, 3.1], "pulando": [2325, 362, 483, 10, 3.1], "batendo": [19410, 536, 495, 10, 3.1], "voando": [24787,443, 454, 10, 3.1]}
        self.sprites_boy = pygame.sprite.Group()
        self.boy = personagem.BoyNinja(x, y, "img/spritesheet_boy.png", dict_animacoes_boy)
        self.sprites_boy.add(self.boy)

        dict_animacoes_robo= {"parado": [0, 567, 555, 10, 3.5], "correndo": [5670, 567, 550, 8, 3.5], "morrendo": [10190 , 562, 519, 10,3.5]}
        self.sprites_robo = pygame.sprite.Group()
        self.robo = personagem.Robo(800, 450, 100, 100, "img/spritesheet_robo.png", dict_animacoes_robo, direita_movimentacao = False)
        self.sprites_robo.add(self.robo)

        self.robo.verifica_player(self.boy)

        #test
        espectativa = False
        realidade = self.robo.verifica_player(self.boy)

        # Assert
        self.assertAlmostEqual(espectativa, realidade)
    
    def test_verifica_player_altura_diferente(self):
        """Testa se o robo não vê o player se ele estiver em uma altura diferente"""
        x = 800
        y = 200

        dict_animacoes_boy = {"parado": [0, 232, 455, 10, 3.1], "correndo": [5940, 363, 455, 10, 3.1], "pulando": [2325, 362, 483, 10, 3.1], "batendo": [19410, 536, 495, 10, 3.1], "voando": [24787,443, 454, 10, 3.1]}
        self.sprites_boy = pygame.sprite.Group()
        self.boy = personagem.BoyNinja(x, y, "img/spritesheet_boy.png", dict_animacoes_boy)
        self.sprites_boy.add(self.boy)

        dict_animacoes_robo= {"parado": [0, 567, 555, 10, 3.5], "correndo": [5670, 567, 550, 8, 3.5], "morrendo": [10190 , 562, 519, 10,3.5]}
        self.sprites_robo = pygame.sprite.Group()
        self.robo = personagem.Robo(800, 450, 100, 100, "img/spritesheet_robo.png", dict_animacoes_robo, direita_movimentacao = False)
        self.sprites_robo.add(self.robo)

        self.robo.verifica_player(self.boy)

        #test
        espectativa = False
        realidade = self.robo.verifica_player(self.boy)

        # Assert
        self.assertAlmostEqual(espectativa, realidade)

    def test_verifica_player_dentro_direita(self):
        """Testa se o robo vê player no campo de visão pela direita"""
        x = 750
        y = 100

        dict_animacoes_boy = {"parado": [0, 232, 455, 10, 3.1], "correndo": [5940, 363, 455, 10, 3.1], "pulando": [2325, 362, 483, 10, 3.1], "batendo": [19410, 536, 495, 10, 3.1], "voando": [24787,443, 454, 10, 3.1]}
        self.sprites_boy = pygame.sprite.Group()
        self.boy = personagem.BoyNinja(x, y, "img/spritesheet_boy.png", dict_animacoes_boy)
        self.sprites_boy.add(self.boy)

        dict_animacoes_robo= {"parado": [0, 567, 555, 10, 3.5], "correndo": [5670, 567, 550, 8, 3.5], "morrendo": [10190 , 562, 519, 10,3.5]}
        self.sprites_robo = pygame.sprite.Group()
        self.robo = personagem.Robo(800, 450, 100, 100, "img/spritesheet_robo.png", dict_animacoes_robo, direita_movimentacao = True)
        self.sprites_robo.add(self.robo)

        self.robo.verifica_player(self.boy)

        #test
        espectativa = True
        realidade = self.robo.verifica_player(self.boy)

        # Assert
        self.assertAlmostEqual(espectativa, realidade)

    def test_verifica_player_dentro_esquerda(self):
        """Testa se o robo vê player no campo de visão pela esquerda"""
        x = 850
        y = 100

        dict_animacoes_boy = {"parado": [0, 232, 455, 10, 3.1], "correndo": [5940, 363, 455, 10, 3.1], "pulando": [2325, 362, 483, 10, 3.1], "batendo": [19410, 536, 495, 10, 3.1], "voando": [24787,443, 454, 10, 3.1]}
        self.sprites_boy = pygame.sprite.Group()
        self.boy = personagem.BoyNinja(x, y, "img/spritesheet_boy.png", dict_animacoes_boy)
        self.sprites_boy.add(self.boy)

        dict_animacoes_robo= {"parado": [0, 567, 555, 10, 3.5], "correndo": [5670, 567, 550, 8, 3.5], "morrendo": [10190 , 562, 519, 10,3.5]}
        self.sprites_robo = pygame.sprite.Group()
        self.robo = personagem.Robo(800, 450, 100, 100, "img/spritesheet_robo.png", dict_animacoes_robo, direita_movimentacao = False)
        self.sprites_robo.add(self.robo)

        self.robo.verifica_player(self.boy)

        #test
        espectativa = True
        realidade = self.robo.verifica_player(self.boy)

        # Assert
        self.assertAlmostEqual(espectativa, realidade)


if __name__ == '__main__':
    unittest.main(verbosity=2)