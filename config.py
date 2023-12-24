import pygame

key_actions = {
    "quit":     [pygame.K_ESCAPE],
    "left":     [pygame.K_a, pygame.K_LEFT],
    "right":    [pygame.K_d, pygame.K_RIGHT],
    "rotate_cw":[pygame.K_j, pygame.K_UP],
    "soft_drop":[pygame.K_s],
    "hard_drop":[pygame.K_w],
    "hold":     [pygame.K_SPACE],
    "pause":    [pygame.K_PAUSE],
    "down":     [pygame.USEREVENT],
    "reset":     [pygame.K_r],
    "render":     [pygame.K_m],
    "plot":     [pygame.K_n],
}

config = {
    'cell_size':    20,
    'cols':        8,
    'rows':        16,
    'delay':    750,
    'maxfps':    30
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