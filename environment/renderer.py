import pygame
from environment.colors import Color
from environment.tetris import Tetris

class PyGameRenderer():
    def __init__(self, cell_size):
        self.clock = pygame.time.Clock()
        self.cell_size = cell_size

    def render(self, env:Tetris):
        if not pygame.get_init():
            pygame.init()
            self.width  = env.cols * self.cell_size + self.cell_size * 10
            self.height = env.rows * self.cell_size + self.cell_size * 2
            self.screen = pygame.display.set_mode((self.width, self.height))
            self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.event.set_blocked(pygame.MOUSEMOTION) 
            self.font = pygame.font.Font(None, 36)

        self.surface.set_alpha(255)
        self.screen.fill((0, 0, 0))
        self.surface.fill((0, 0, 0))

        self.top_msg(f'Score: {env.score}')
        self.draw_rect((255, 0, 0), 5, 1, env.cols, env.rows)
        for i, shape in enumerate(env.held_shapes):
            self.draw_matrix(shape, (1, i * 3 + 1))
        self.draw_matrix(env.board, (5, 1))
        self.draw_matrix(env.shape, (env.shape_x + 5, env.shape_y + 1))
        self.draw_matrix(env.shape, (env.shape_x + 5, env._soft_drop(env.board, env.shape, (env.shape_x, env.shape_y)) + 1), 2)
        for i, shape in enumerate(env.next_shapes):
            self.draw_matrix(shape, (env.board.shape[1] + 6, i * 3 + 1))
        self.draw_grid()
        self.draw_stats(env)

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
        stats = f'Lines:{env.lines} Pieces:{env.pieces} Level:{env.level}'
        for i, line in enumerate(stats.split()):
            msg_image = self.font_img(line)
            text_offset_x = (env.board.shape[1]+6) * self.cell_size
            text_offset_y = (i + len(env.next_shapes) * 3 + 1) * self.cell_size
            self.surface.blit(msg_image, (text_offset_x, text_offset_y))

    def draw_rect(self, color, left, top, width, height):
        cs = self.cell_size
        pygame.draw.rect(self.surface, color, 
                         pygame.Rect(left*cs, top*cs, width*cs, height*cs),  2)

    def draw_grid(self):
        for i in range(self.width // self.cell_size):
            pygame.draw.line(self.surface, (0, 0, 0), (i * self.cell_size, 0), (i * self.cell_size, self.height * self.cell_size))
        for i in range(self.height // self.cell_size):
            pygame.draw.line(self.surface, (0, 0, 0), (0, i * self.cell_size), (self.width * self.cell_size, i * self.cell_size))

    def wait(self, ms):
        self.clock.tick(1000 / ms)

    def top_msg(self, msg):
        msg_image = self.font_img(msg)
        msgim_center_x, _ = msg_image.get_size()
        msgim_center_x //= 2
    
        self.surface.blit(msg_image, (self.width // 2-msgim_center_x, 0))

    def font_img(self, text):
        return pygame.font.Font(pygame.font.get_default_font(), 12).render(text, False, (255,255,255), (0,0,0))

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
