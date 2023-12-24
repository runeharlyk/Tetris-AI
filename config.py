import pygame

config = {
    'cell_size':   20,
    'cols':        8,
    'rows':        16,
    'down_delay':  750,
    'delay_id':    1,
    'print_id':    2,
    'print_delay': 1000,
    'maxfps':       30
}

key_actions = {
    "quit":     [pygame.K_ESCAPE, pygame.QUIT],
    "left":     [pygame.K_a, pygame.K_LEFT],
    "right":    [pygame.K_d, pygame.K_RIGHT],
    "rotate_cw":[pygame.K_j, pygame.K_UP],
    "soft_drop":[pygame.K_s],
    "hard_drop":[pygame.K_w],
    "hold":     [pygame.K_SPACE],
    "pause":    [pygame.K_PAUSE],
    "down":     [pygame.USEREVENT+config['delay_id']],
    "reset":    [pygame.K_r],
    "render":   [pygame.K_m],
    "plot":     [pygame.K_n],
    "print":    [pygame.USEREVENT+config['print_id']],
}

colors = [
    (0,   0,   0  ),
    (255, 0,   0  ),
    (0,   150, 0  ),
    (0,   0,   255),
    (255, 120, 0  ),
    (255, 255, 0  ),
    (180, 0,   255),
    (0,   220, 220)
]