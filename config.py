FPS = 60

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
                    'campo_de_visao': 1,
                    'movimentacao': True,
                    'direita_movimentacao': True
                }
            ], 'H': [
                {
                    'variacao_x': (-1, 1),
                    'platform_vel': 3
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
        }
    }]