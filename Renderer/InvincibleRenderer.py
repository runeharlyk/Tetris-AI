from Renderer.RendererBase import RendererBase


class InvincibleRenderer(RendererBase):
    def __init__(self) -> None:
        super().__init__()

    def render(self, board, score):
        return super().render(board, score)

    def wait(self, ms):
        pass