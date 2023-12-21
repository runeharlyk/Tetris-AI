from config import *


class RendererBase:
    def __init__(self) -> None:
        pass

    def render(self, board, score):
        pass

    def wait(self, ms):
        pass