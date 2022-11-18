from calendar import c
import pygame
from pygame.locals import *


class Personagem(pygame.sprite.Sprite):
    # Define estados possíveis do jogador
    parado = 0 
    pulando = 1
    caindo = 2
    # Define a aceleração da gravidade
    gravidade = 2
    # Define a velocidade inicial no pulo
    aceleracao_pulo_inicial = 30

    def __init__(self, x, y, img, dict_animacoes):
        pygame.sprite.Sprite.__init__(self)
        self.aceleracao = self.aceleracao_pulo_inicial
        self.state = 2
        
        sprite_sheet = pygame.image.load(img).convert_alpha()
        self.imagens_ninja = []
        
        for posicao in dict_animacoes.values():
            inicial = posicao[0]
            largura = posicao[1]
            altura = posicao[2]
            quantidade = posicao[3]
            redirecionamento = posicao[4]
            self.corta_sprite(sprite_sheet, inicial, largura, altura, quantidade, redirecionamento) 

        self.index_lista = 0
        self.image = self.imagens_ninja[self.index_lista]
        self.rect = self.image.get_rect(midbottom = (x,y))

        self.direita = True
        self.correr = False
        self.pular = False
        self.planar = False

    def corta_sprite(self,sprite_sheet, posicao_inicial, largura, altura, quantidade, redirecionamento):
        for i in range(0, quantidade):
            largura_inicial = posicao_inicial
            img = sprite_sheet.subsurface((largura_inicial + i*largura,0), (largura,altura))
            img = pygame.transform.scale(img, (largura/redirecionamento, altura/redirecionamento))
            self.imagens_ninja.append(img)
    
    def parado_animacao(self):
        if self.index_lista > 9:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image= self.imagens_ninja[int(self.index_lista)]
        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image= pygame.transform.flip(self.image, True, False)


    def correr_direita(self): 
        self.direita = True
        self.correr = True
        if self.index_lista < 10:
            self.index_lista = 10
        if (self.pular or self.planar):
            self.rect.x += 9
        else:
            self.rect.x += 6
    
    def correr_esquerda(self):
        self.direita = False
        self.correr = True
        if self.index_lista < 10:
            self.index_lista = 10
        if self.pular or self.planar:
            self.rect.x -= 9
        else:
            self.rect.x -= 6

    def correr_animacao(self):
        if self.index_lista > 19:   
            self.index_lista = 10
        self.index_lista += 0.25
        self.image= self.imagens_ninja[int(self.index_lista)]
        
        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image= pygame.transform.flip(self.image, True, False)
        self.correr = False
        
    def fun_cair(self):
        self.correr = False
        self.planar = False
        self.state = 2

    def cair(self):
        self.rect.y += self.aceleracao
        self.aceleracao += self.gravidade
        self.index_lista = 24
        self.image = self.imagens_ninja[int(self.index_lista)]
        if self.direita == False:
            self.image= pygame.transform.flip(self.image, True, False)

        # Aceleração máxima
        if self.aceleracao > 18:
            self.aceleracao = 18


    def fun_pular(self):
        self.pular = True
        self.correr = False
        self.state = 1
        if self.index_lista < 20:
            self.index_lista = 20

    def pular_animacao(self):
        ####### animação #######
        if self.index_lista > 29:   
            self.index_lista = 20
        self.index_lista += 0.25
        self.image = self.imagens_ninja[int(self.index_lista)]
        
        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image = pygame.transform.flip(self.image, True, False)
        self.correr = False
        ########## 

        # Atualiza o estado para caindo
        if self.aceleracao < 0:
            self.state = 2
        
        if self.state == 1: 
            self.rect.y -= self.aceleracao
            self.aceleracao -= self.gravidade
        
        if self.state == 2: 
            self.rect.y += self.aceleracao
            self.aceleracao += self.gravidade
            

class BoyNinja(Personagem):
    def __init__(self, x, y, img, dict_animacoes):
        super().__init__(x, y, img, dict_animacoes)
        self.bater = False

    def fun_bater(self):
        self.bater = True
        self.correr = False
        if self.index_lista < 30:
            self.index_lista = 30

    def bater_animacao(self):
        #Deixar a animação mais suave
        if self.index_lista == 30:
            if self.direita:
                self.rect.x -= 15 
            else:
                self.rect.x -= 80 

        if self.index_lista > 39: 
            self.index_lista = 0
            self.bater = False
            # Voltar para o local inicial
            if self.direita:
                self.rect.x += 15
            else:
                self.rect.x += 80

        self.index_lista += 0.25
        self.image = self.imagens_ninja[int(self.index_lista)]
        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image = pygame.transform.flip(self.image, True, False)
       

    def fun_planar(self):
        self.pular = False
        self.correr = False
        self.planar = True
        self.state = 2
        if self.index_lista < 40:
            self.index_lista = 40
 

    def planar_animacao(self):
        if self.index_lista > 49:   
            self.index_lista = 40
        self.index_lista += 0.5
        self.image = self.imagens_ninja[int(self.index_lista)]

        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image = pygame.transform.flip(self.image, True, False)
        # Atualiza o estado para caindo

        self.aceleracao = 3
        self.rect.y += self.aceleracao
    

    def update(self):

        if self.state == 0:
            self.aceleracao = self.aceleracao_pulo_inicial
            self.pular = False
            self.planar = False
        
        if self.state == 2 and self.planar == False:
            self.cair()
        # Controle de animação do personagem para correr
        elif self.correr and self.pular == False and self.planar == False:
            self.correr_animacao()
        # Controle de animação do personagem para pular
        elif self.pular:
            self.pular_animacao()
        # Controle de animação do personagem para bater
        elif self.bater and self.pular == False:
            self.bater_animacao()
        # Controle de animação do personagem para planar
        elif self.planar:
            self.planar_animacao()
        # Controle de animação do personagem para parado
        else: 
            self.parado_animacao()
            
class GirlNinja(Personagem):
    def __init__(self, x, y, img, dict_animacoes, screen):
        super().__init__(x, y, img, dict_animacoes)
        self.screen = screen
        self.deslizar = False
        self.atirar = False
        self.kunai = Kunai(self.screen)
        
    def fun_deslizar(self):
        self.deslizar = True
        self.correr = False
        self.rect.y += 37

        if self.index_lista < 30:
            self.index_lista = 30
        if self.direita == False:
            self.rect.x -= 7.5
        else:
            self.rect.x += 7.5

    def deslizar_animacao(self):
        if self.index_lista > 39:   
            self.index_lista = 30
        self.index_lista += 0.25
        self.image = self.imagens_ninja[int(self.index_lista)]

        # vira a imagem se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image = pygame.transform.flip(self.image, True, False)
        self.deslizar = False
        self.rect.y -= 37


    def fun_atirar(self):
        self.atirar = True
        self.correr = False

        if self.index_lista < 40:
            self.index_lista = 40
            

    def atirar_animacao(self):
        if self.index_lista > 49:   
            self.index_lista = 40
            self.atirar = False

        if self.index_lista == 43:
            self.kunai.fun_atirar(self.rect.x, self.rect.y, self.direita) 

        self.index_lista += 0.25
        self.image = self.imagens_ninja[int(self.index_lista)]

        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image = pygame.transform.flip(self.image, True, False)


    def update(self):
        # Atualiza a posição do kunai
        self.kunai.update()
            
        if self.state == 0:
            self.aceleracao = self.aceleracao_pulo_inicial
            self.pular = False
            self.planar = False
        
        # controle de animação do personagem para deslizar
        if self.deslizar:
            self.deslizar_animacao()
        # controle de animação do personagem para cair
        elif self.state == 2:
            self.cair()
        # Controle de animação do personagem para correr
        elif self.correr and self.pular == False:
            self.correr_animacao()
        # Controle de animação do personagem para pular
        elif self.pular:
            self.pular_animacao()
        # Controle de animação do personagem para atirar
        elif self.atirar:
            self.atirar_animacao()
        # Controle de animação do personagem para parado
        else: 
            self.parado_animacao()


class Robo(Personagem):
    def __init__(self, x_inicial, y, temporizador_parado, temporizador_correndo, img, dict_animacoes):
        super().__init__(x_inicial, y, img, dict_animacoes)
        self.temporizador_parado = temporizador_parado
        self.temporizador_correndo = temporizador_correndo

        self.vivo = True
        self.temporizador = 0

    def fun_morrer(self):
        self.vivo = False
        if self.index_lista < 18:
            self.index_lista = 18

    def correr_animacao(self):
        if self.index_lista > 17:   
            self.index_lista = 10
        self.index_lista += 0.25
        self.image= self.imagens_ninja[int(self.index_lista)]
        
        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image= pygame.transform.flip(self.image, True, False)
        self.correr = False

    def animacao_morrer(self):
        if self.index_lista > 27:   
            self.index_lista = 27
        self.index_lista += 0.25
        self.image= self.imagens_ninja[int(self.index_lista)]
        
        # vira a image se o personagem estiver olhando para o outro lado
        if self.direita == False:
            self.image= pygame.transform.flip(self.image, True, False)
        self.correr = False

    def update(self):
        if self.state == 2:
            self.cair()
        if self.vivo == False:
            self.animacao_morrer()
        # Controle de animação do personagem para correr
        elif self.temporizador >= self.temporizador_parado and self.temporizador <= self.temporizador_correndo:
            self.correr_animacao()
            if self.direita:
                self.correr_direita()
            else:
                self.correr_esquerda()
        # Controle de animação do personagem para parado após correr
        elif self.temporizador > self.temporizador_correndo + self.temporizador_parado:
            self.temporizador = self.temporizador_parado
            self.direita = not self.direita
        else: 
            self.parado_animacao()
        self.temporizador += 1
        

class Kunai(pygame.sprite.Sprite):
    gravidade = 1.5
    aceleracao_inicial = 25

    def __init__(self, screen):       
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        image = pygame.image.load("img/Kunai.png").convert_alpha()
        self.image = pygame.transform.scale(image, (160/2.4, 32/2.4)) #redimensiona a imagem para o tamanho desejado
        self.rect = self.image.get_rect()
        self.aceleracao = self.aceleracao_inicial
        self.direita = True
        self.atirar = False


    def fun_atirar(self, x, y, bool_direita):
        self.atirar = True
        self.direita = bool_direita
        if self.direita:
            self.rect.midbottom = (x + 100, y) #posiciona o kunai na frente do personagem
        else:
            self.rect.midbottom = (x, y)

    def trajetoria(self):
        if self.direita:
            self.rect.x += 15
        else:
            self.rect.x -= 15

        self.rect.y -= self.aceleracao
        self.aceleracao -= self.gravidade

        if self.direita:
            self.screen.blit(self.image, self.rect)
        else:
            self.screen.blit(pygame.transform.flip(self.image, True, False), self.rect)

    def update(self):
        if self.atirar:
            self.trajetoria()
        else:
            self.aceleracao = self.aceleracao_inicial