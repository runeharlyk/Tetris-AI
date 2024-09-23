import numpy as np
import pygame
from environment.colors import Color
from environment.tetris import Tetris
from utils.heuristics import Heuristics

class RenderConfig():
    def __init__(self, bg_color, grid_color, highlight_color, text_color, render_bumpiness=False, render_holes=False, render_max_height=False, show_ghost_piece=True) -> None:
        self.bg_color = bg_color
        self.grid_color = grid_color
        self.highlight_color = highlight_color
        self.render_bumpiness = render_bumpiness
        self.render_holes = render_holes
        self.render_max_height = render_max_height
        self.show_ghost_piece = show_ghost_piece
        self.text_color = text_color

NES_Tetris_Config = RenderConfig(Color.BLACK, Color.BLACK, Color.WHITE, Color.WHITE)
PAPER_Tetris_Config = RenderConfig(Color.GREYBLUE, Color.WHITE, Color.BLACK, Color.BLACK, True, False)

class PyGameRenderer:
    def __init__(self, cell_size, config=NES_Tetris_Config):
        self.clock = pygame.time.Clock()
        self.cell_size = cell_size
        self.heuristics = Heuristics()
        self.config = config

    def render(self, env: Tetris):
        if not pygame.get_init():
            pygame.init()
            self.width = env.cols * self.cell_size + self.cell_size * 10
            self.height = env.rows * self.cell_size + self.cell_size * 2
            self.screen = pygame.display.set_mode((self.width, self.height))
            self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.event.set_blocked(pygame.MOUSEMOTION)
            self.font = pygame.font.Font(None, 36)

        self.surface.set_alpha(255)
        self.screen.fill(self.config.bg_color)
        self.surface.fill(self.config.bg_color)

        self.draw_rect(Color.GRAY, 5, 1, env.cols, env.rows)

        self.top_msg(f"Score: {env.score}")
        # self.draw_rect((255, 0, 0), 5, 1, env.cols, env.rows)
        for i, shape in enumerate(env.held_shapes):
            self.draw_matrix(shape, (1, i * 3 + 1))
        self.draw_matrix(env.board, (5, 1))
        self.draw_matrix(env.shape, (env.shape_x + 5, env.shape_y + 1))
        if self.config.show_ghost_piece:
            self.draw_matrix(env.shape, (env.shape_x + 5, env._soft_drop(env.board, env.shape, (env.shape_x, env.shape_y)) + 1), 2)
        for i, shape in enumerate(env.next_shapes):
            self.draw_matrix(shape, (env.board.shape[1] + 6, i * 3 + 1))
        self.draw_grid(env)
        self.draw_stats(env)

        self.draw_heuristics(env)

        if env.done:
            self.add_backdrop()
            self.center_msg(f"Game Over!\nPress r to restart\nFinal score:{env.score}")

        if env.paused:
            self.add_backdrop()
            self.center_msg("Paused")

        self.screen.blit(self.surface, (0, 0))
        pygame.display.update()

    def add_backdrop(self):
        self.surface.set_alpha(100)
        self.surface.fill((0, 200, 0, 0))

    def draw_stats(self, env):
        stats = f"Lines:{env.lines} Pieces:{env.pieces}"
        if env.use_level:
            stats += f" Level:{env.level}"
        for i, line in enumerate(stats.split()):
            msg_image = self.font_img(line)
            text_offset_x = (env.board.shape[1] + 6) * self.cell_size
            text_offset_y = (i + len(env.next_shapes) * 3 + 1) * self.cell_size
            self.surface.blit(msg_image, (text_offset_x, text_offset_y))

    def draw_rect(self, color, left, top, width, height):
        cs = self.cell_size
        pygame.draw.rect(
            self.surface,
            color,
            pygame.Rect(left * cs, top * cs, width * cs, height * cs),
            2,
        )

    def draw_grid(self, env):
        cs = self.cell_size
        cols, rows = env.cols, env.rows
        off_y, off_x = 1, 5
        for col in range(cols + 1):
            pygame.draw.line(
                self.surface,
                self.config.grid_color,
                ((off_x + col) * cs, off_y * cs),
                ((off_x + col) * cs, (rows + off_y) * cs),
            )
        for row in range(rows + 1):
            pygame.draw.line(
                self.surface,
                self.config.grid_color,
                (off_x * cs, (off_y + row) * cs),
                ((cols + off_x) * cs, (off_y + row) * cs),
            )

    def wait(self, ms):
        self.clock.tick(1000 / ms)

    def top_msg(self, msg):
        msg_image = self.font_img(msg)
        msgim_center_x, _ = msg_image.get_size()
        msgim_center_x //= 2
    
        self.surface.blit(msg_image, (self.width // 2-msgim_center_x, 0))

    def font_img(self, text):
        return pygame.font.Font(pygame.font.get_default_font(), 12).render(text, False, self.config.text_color, self.config.bg_color)

    def center_msg(self, msg):
        for i, line in enumerate(msg.splitlines()):
            msg_image = self.font_img(line)
            msgim_center_x, msgim_center_y = msg_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2
        
            self.surface.blit(msg_image, (self.width // 2-msgim_center_x, self.height // 2-msgim_center_y+i*22))
    
    def draw_matrix(self, matrix:list[list[int]], offset:tuple[int, int], width:int=0, opacity:int=255):
        off_x, off_y  = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if not val: continue
                color = Color.ALL[val] if val < len(Color.ALL) else Color.GRAY
                rect = pygame.Rect((off_x+x) * self.cell_size, (off_y+y) * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.surface, (*color, opacity), rect, width)

    def draw_heuristics(self, env):
        if self.config.render_bumpiness:
            self.draw_bumpiness(env.board)

        if self.config.render_holes:
            self.draw_holes(env.board)

        if self.config.render_max_height:
            self.draw_max_height(env.board)

    def draw_bumpiness(self, board):
        heights = self.heuristics._get_heights(board)
        for i, height in enumerate(heights):
            rows, _ = board.shape
            start = ((i + 5) * self.cell_size, (rows - height + 1) * self.cell_size)
            end = ((i + 6) * self.cell_size, (rows - height + 1) * self.cell_size)
            pygame.draw.line(self.surface, self.config.highlight_color, start, end, 5)
            if i < len(heights) - 1:
                start = ((i + 6) * self.cell_size, (rows - heights[i + 1] + 1) * self.cell_size)
                pygame.draw.line(self.surface, self.config.highlight_color, end, start, 5)
 
    def draw_holes(self, board):
        bridge_mask = board != 0
        rows, cols = board.shape

        for col in range(cols):
            if np.any(bridge_mask[:-1, col]):
                bridge_row = np.argmax(bridge_mask[:, col])
                for row in range(bridge_row + 1, rows):
                    if not bridge_mask[row, col]:
                        x = (col + 5) * self.cell_size
                        y = (row + 1 ) * self.cell_size
                        pygame.draw.rect(self.surface, self.config.highlight_color, (x, y, self.cell_size, self.cell_size), 4)

    def draw_max_height(self, board):
        max_heights = np.max(self.heuristics._get_heights(board))
        rows, cols = board.shape

        start = (5 * self.cell_size, (rows - max_heights + 1) * self.cell_size)
        end = ((cols + 6) * self.cell_size, (rows - max_heights + 1) * self.cell_size)
        pygame.draw.line(self.surface, self.config.highlight_color, start , end, 5)
            
