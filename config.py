FPS = 60

# Legenda:
# X: Bloco de chão
# B: BoyNinja
# G: GirlNinja
# C: Chave
# M: Plataforma condicional (precisa de alavanca ou botão para mexer)
# T: Botão
# P: Saída (ocupa o bloco da direita também)
# A: Alavanca
# H: Plataforma horizontal
# R: Robo
# V: Plataforma vertical

# Unidade de medidas dos parâmetros estão em blocos

level_data = [
    {
        'level_map': [
            'XXXXXXXXXXXXXXXXXX',
            'X                X',
            'X       R        X',
            'X  H             X',
            'X       V        X',
            'X        T       X',
            'X       XX       X',
            'X    A       P   X',
            'X   XX       XX  X',
            'X        M       X',
            'X       XX       X',
            'X B    C   G     X',
            'XXXXXXXXXXXXXXXXXX'
        ], 'sprite_settings': {
            'R': [
                {
                    'x_distancia': 2,
                    'campo_de_visao': 3,
                    'movimentacao': False,
                    'direita_movimentacao': True
                }
            ], 'H': [
                {
                    'variacao_x': (-1, 1),
                    'platform_vel': 0.03
                }
            ], 'V': [
                {
                    'variacao_y': (-1, 1)
                }
            ], 'M': [
                {
                    'variacao_x': (-1, 1),
                    'horizontal': True
                }
            ]
        }, 'connections': [
            {
                'A': [0],
                'T': [0]
            }
        ]
    }]

level_data2 = [
    {
        'level_map': [
            'XXXXXXXXXXXXXXXXXX',
            'X                X',
            'X       R        X',
            'X  H          P  X',
            'X       V     XXXX',
            'X                X',
            'X         M      X',
            'X                X',
            'X   XXXX     XX  X',
            'X      H         X',
            'X             XXXX',
            'X B        G   TCX',
            'XXXXXXXXXXXXXXXXXX'
        ], 'sprite_settings': {
            'R': [
                {
                    'x_distancia': 2,
                    'campo_de_visao': 1,
                    'movimentacao': False,
                    'direita_movimentacao': True
                }
            ], 'H': [
                {
                    'variacao_x': (-1, 1),
                    'platform_vel': 0.03
                },
                {
                    'variacao_x': (-1, 1),
                    'platform_vel': 0.03
                }
            ], 'V': [
                {
                    'variacao_y': (-1, 1)
                }
            ], 'M': [
                {
                    'variacao_x': (-1, 1),
                    'horizontal': True
                }
            ]
        }, 'connections': [
            {
                'A': [],
                'T': [0]
            }
        ]
    }]

level_data3 = [
    {
        'level_map': [
            'XXXXXXXXXXXXXXXXXX',
            'X                X',
            'X       R        X',
            'X    P  A        X',
            'X    XXXX        X',
            'X                X',
            'X   M          V X',
            'X                X',
            'X       XXX      X',
            'X   V            X',
            'X                X',
            'X B    C   G     X',
            'XXXXXXXXXXXXXXXXXX'
        ], 'sprite_settings': {
            'R': [
                {
                    'x_distancia': 2,
                    'campo_de_visao': 1,
                    'movimentacao': True,
                    'direita_movimentacao': True
                }
            ], 'H': [
                {
                    'variacao_x': (-1, 1),
                    'platform_vel': 0.03
                }
            ], 'V': [
                {
                    'variacao_y': (-1, 1)
                },
                {
                    'variacao_y': (-1, 2)
                }
            ], 'M': [
                {
                    'variacao_x': (-1, 6),
                    'horizontal': True
                }
            ]
        }, 'connections': [
            {
                'A': [0],
                'T': []
            }
        ]
    }]