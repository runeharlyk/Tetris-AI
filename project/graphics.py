from config import *

import cv2 as cv
import numpy as np
from time import sleep

class Renderer:
    def __init__(self) -> None:
        pass

    def render(self, board, score):
        pass

    def wait(self, ms):
        sleep(ms / 100)


class CVRenderer(Renderer):
    def __init__(self) -> None:
        super().__init__()

    def render(self, env, score):
        env._set_piece(True)
        board = env.board[:].T
        board = [[green if board[i][j] else black for j in range(env.width)] for i in range(env.height)]
        env._set_piece(False)

        img = np.array(board).reshape((env.height, env.width, 3)).astype(np.uint8)
        img = cv.resize(img, (env.width * 25, env.height * 25), interpolation=cv.INTER_NEAREST)

        # To draw lines every 25 pixels
        img[[i * 25 for i in range(env.height)], :, :] = 0
        img[:, [i * 25 for i in range(env.width)], :] = 0

        # Add extra spaces on the top to display game score
        extra_spaces = np.zeros((2 * 25, env.width * 25, 3))
        cv.putText(extra_spaces, "Score: " + str(score), (15, 35), cv.FONT_HERSHEY_SIMPLEX, 1, white, 2, cv.LINE_AA)

        # Add extra spaces to the board image
        img = np.concatenate((extra_spaces, img), axis=0)

        # Draw horizontal line to separate board and extra space area
        img[50, :, :] = white

        cv.imshow('DQN Tetris', img)

    def wait(self, ms):
        cv.waitKey(ms)

class InvincibleRenderer(Renderer):
    def __init__(self) -> None:
        super().__init__()

    def render(self, board, score):
        return super().render(board, score)

    def wait(self, ms):
        pass