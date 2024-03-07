import pygame

from environment.config import Config


class Action:

    WAIT   = 0 # no move, just one tile down
    ROTATE = 1
    LEFT   = 2
    RIGHT  = 3
    DOWN   = 4

    ALL = [WAIT, ROTATE, LEFT, RIGHT, DOWN]

key_actions = {
    "quit":     [pygame.K_ESCAPE, pygame.QUIT],
    "left":     [pygame.K_a, pygame.K_LEFT],
    "right":    [pygame.K_d, pygame.K_RIGHT],
    "rotate_cw":[pygame.K_j, pygame.K_UP],
    "soft_drop":[pygame.K_s],
    "hard_drop":[pygame.K_SPACE],
    "hold":     [pygame.K_w],
    "pause":    [pygame.K_p],
    "down":     [pygame.USEREVENT+Config.delay_id],
    "reset":    [pygame.K_r],
    "render":   [pygame.K_m],
    "up":       [pygame.K_UP],
    "plot":     [pygame.K_n],
    "print":    [pygame.USEREVENT+Config.print_id],
}