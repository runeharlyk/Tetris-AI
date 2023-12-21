import pygame
import numpy as np
from Renderer.RendererBase import *


class PyGameRenderer(RendererBase):
    def __init__(self) -> None:
        super().__init__()
        self.clock = pygame.time.Clock()

    def draw_shape(self, surface, shape):
        for cell in shape:
            left = abs(cell[0]) * 25
            top = abs(cell[1]) * 25
            rect = pygame.Rect(left, top, 25, 25)
            pygame.draw.rect(surface, blue, rect)
        for i in range(4):
            pygame.draw.line(surface, (0, 0, 0), (i * 25, 0), (i * 25, 2 * 25))
        for i in range(4):
            pygame.draw.line(surface, (0, 0, 0), (0, i * 25), (4 * 25, i * 25))


    def render_held(self, shape):
        self.hold_box_size = 4 * 25  # Assuming each block in Tetris is 25x25 pixels
        self.hold_box_surface = pygame.Surface((4 * 25, 2 * 25))
        # self.hold_box_surface.fill((128, 128, 128)) 
        self.draw_shape(self.hold_box_surface, shape)

    def draw_lines(self, env):
        for i in range(env.width):
            pygame.draw.line(self.board_surface, (0, 0, 0), (i * 25, 0), (i * 25, env.height * 25))
        for i in range(env.height):
            pygame.draw.line(self.board_surface, (0, 0, 0), (0, i * 25), (env.width * 25, i * 25))

    def draw_grid(self, board_colors):
        for i, row in enumerate(board_colors):
            for j, color in enumerate(row):
                rect = pygame.Rect(j * 25, i * 25, 25, 25)
                pygame.draw.rect(self.board_surface, color, rect)

    def render(self, env, score):
        env._set_piece(True)
        board = env.board[:].T
        color_map = {True: green, False: black}  # Define color mapping
        board_colors = [[color_map[board[i][j]] for j in range(env.width)] for i in range(env.height)]
        env._set_piece(False)

        # Initialize Pygame if it hasn't been initialized yet
        if not pygame.get_init():
            pygame.init()
            window_width = env.width * 25 + 100  # Additional 100 pixels for the hold box and padding
            window_height = env.height * 25 + 50  # Additional 50 pixels for the score
            self.screen = pygame.display.set_mode((window_width, window_height))
            self.font = pygame.font.Font(None, 36)



        # Convert the board to a Pygame surface
        self.board_surface = pygame.Surface((env.width * 25, env.height * 25))
        
        self.draw_grid(board_colors)
        self.render_held(env.held_piece[0])

        self.draw_lines(env)

        # Render the score
        
        text = self.font.render(f"Score: {score}", True, white)
        text_rect = text.get_rect(center=(env.width * 25 // 2 + 50, 25))  # Adjusted for the hold box

        # Blit everything to the self.screen
        self.screen.fill((0, 0, 0))  # Clear self.screen
        self.screen.blit(self.hold_box_surface, (25, 50))  # Draw the hold box (with some padding)
        self.screen.blit(self.board_surface, (self.hold_box_size + 50, 50))  # Draw the board (shifted to the right)
        self.screen.blit(text, text_rect)  # Draw the score

        # Update the display
        pygame.display.flip()

    def wait(self, ms):
        self.clock.tick(5)