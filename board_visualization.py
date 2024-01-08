from environment.config import *
from environment.controls import Controller
from environment.tetris import Tetris
from environment.renderer import PyGameRenderer, PAPER_Tetris_Config
from copy import copy

board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

env = Tetris(10, 20)

render_config = copy(PAPER_Tetris_Config)
render_config.render_holes = True
render_config.render_bumpiness = False
render_config.render_max_height = False
render_config.show_ghost_piece = False

renderer = PyGameRenderer(30, render_config)

key_actions = {
    "left":     lambda: env.move(-1),
    "right":    lambda: env.move(1),
    "rotate_cw":env.rotate,
    "soft_drop":env.soft_drop,
    "hard_drop":env.hard_drop,
    "hold":     env.hold,
    "reset":    env.reset,
    "down":     env.down,
}

if __name__ == '__main__':
    try:
        while True:
            renderer.render(env)
            controller = Controller(key_actions)
            controller.handleEvents()
            renderer.wait(1)
    finally:
        pass
