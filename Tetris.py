import pygame
import numpy as np

class Tetris():    
    rendering = False
    
    def __init__(self, state=None):
        pygame.init()
    
    def step(self):
        pass
        
    def render(self):
        if not self.rendering: self.init_render()
                 
        self.screen.fill((187,173,160))
        
        pygame.display.flip()

    def reset(self):
        pass

    def close(self):
        pygame.quit()
                 
    def init_render(self):
        self.screen = pygame.display.set_mode([800, 600])
        pygame.display.set_caption('Tetris')
        self.background = pygame.Surface(self.screen.get_size())
        self.rendering = True
        self.clock = pygame.time.Clock()
        
    def game_over(self):
        pass
    
    def won(self):
        pass
        
    def move(self):
        pass
       
    def new_game(self, board_index = 0):
        pass

if __name__ == "main":
    game = Tetris()
    while 1:
        game.render
