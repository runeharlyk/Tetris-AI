import pygame
from environment.config import Config
from environment.colors import Color

class PyGameRenderer():
    def __init__(self, cell_size):
        self.clock = pygame.time.Clock()
        self.cell_size = cell_size

    def render(self, env):
        if not pygame.get_init():
            pygame.init()
            pygame.key.set_repeat(250,25)
            self.width  = env.cols * self.cell_size + self.cell_size * 10
            self.height = env.rows * self.cell_size + self.cell_size
            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.event.set_blocked(pygame.MOUSEMOTION) 
            self.font = pygame.font.Font(None, 36)

        self.screen.fill((0,0,0))

        if env.done:
            self.center_msg(f"Game Over!\nPress r to restart\nFinal score:{env.score}")
        else:
            if env.paused:
                self.center_msg("Paused")
            else:
                self.top_msg(f'Score: {env.score}')
                self.draw_rect((255, 0, 0), 5, 0, env.cols, env.rows)
                for i, shape in enumerate(env.held_shapes):
                    self.draw_matrix(shape, (1, i*3 + 1))
                self.draw_matrix(env.board, (5, 1))
                self.draw_matrix(env.shape, (env.shape_x + 5, env.shape_y + 1))
                for i, shape in enumerate(env.next_shapes):
                    self.draw_matrix(shape, (env.board.shape[1]+6, i*3 + 1))
                self.draw_grid()
                self.draw_stats(env)
        pygame.display.update()

    def draw_stats(self, env):
        stats = f'Lines:{env.lines} Pieces:{env.pieces} Level:{env.level}'
        for i, line in enumerate(stats.split()):
            msg_image = self.font_img(line)
            text_offset_x = (env.board.shape[1]+6) * self.cell_size
            text_offset_y = (i + len(env.next_shapes)*3 + 1) * self.cell_size
            self.screen.blit(msg_image, (text_offset_x, text_offset_y))

    def draw_rect(self, color, left, top, width, height):
        cs = self.cell_size
        pygame.draw.rect(self.screen, color, 
                         pygame.Rect(left*cs, top*cs, width*cs, height*cs),  2)

    def draw_grid(self):
        for i in range(self.width // self.cell_size):
            pygame.draw.line(self.screen, (0, 0, 0), (i * self.cell_size, 0), (i * self.cell_size, self.height * self.cell_size))
        for i in range(self.height // self.cell_size):
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.cell_size), (self.width * self.cell_size, i * self.cell_size))

    def wait(self, ms):
        self.clock.tick(1000 / ms)

    def top_msg(self, msg):
        msg_image = self.font_img(msg)
        msgim_center_x, _ = msg_image.get_size()
        msgim_center_x //= 2
    
        self.screen.blit(msg_image, (self.width // 2-msgim_center_x, 0))

    def font_img(self, text):
        return pygame.font.Font(pygame.font.get_default_font(), 12).render(text, False, (255,255,255), (0,0,0))

    def center_msg(self, msg):
        for i, line in enumerate(msg.splitlines()):
            msg_image = self.font_img(line)
        
            msgim_center_x, msgim_center_y = msg_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2
        
            self.screen.blit(msg_image, (self.width // 2-msgim_center_x, self.height // 2-msgim_center_y+i*22))
    
    def draw_matrix(self, matrix, offset):
        off_x, off_y  = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if not val: continue
                color = Color.ALL[int(val)]
                rect = pygame.Rect((off_x+x) * self.cell_size, (off_y+y) * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect,0)
