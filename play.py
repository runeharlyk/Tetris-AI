import logging
from game import Tetris
from agent import Agent
from Renderer.InvincibleRenderer import InvincibleRenderer
from Renderer.CVRenderer import CVRenderer
from Renderer.PyGameRenderer import PyGameRenderer

from controls import Controller

logging.basicConfig(level=logging.DEBUG)

height, width = 20, 10

env = Tetris(width, height)
controller = Controller()
renderer = PyGameRenderer()

def start():
    exit_program = False
    score = 0
    while not exit_program:
        renderer.render(env, score) 

        next_states = env.get_next_states()

        inputs = controller.input()
        exit_program = "quit" in inputs

        if inputs:
            print(inputs)
            print(next_states)

        # if not next_states: break

        best_action = None # next(action for action, state in next_states.items())

        _, score, _, done = env.step(best_action)

        renderer.wait(5)

    env.reset()

if __name__ == '__main__':
    start()