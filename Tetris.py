import pygame
import numpy as np

from random import choice

from settings import *
   
class Tetris():    
    rendering = False
    exit_program = False
    paused = False
    shouldRender = True 
    
    def __init__(self):
        self.next_shape = choice(list(TETROMINOS.keys()))

        pygame.init()
    
    def step(self):
        pass
        
    def render(self):
        if not self.shouldRender: return
        if not self.rendering: self.init_render()
                 
        self.background.fill(GRAY)

        self.draw_grid()
        self.background.blit(self.surface, (PADDING,PADDING))
        pygame.draw.rect(self.background, LINE_COLOR, self.rect, 2, 2)
        
        self.clock.tick()
        pygame.display.update()
    
    def draw_grid(self):

        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (x,0), (x,self.surface.get_height()), 1)

        for row in range(1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLOR, (0,y), (self.surface.get_width(),y))

        self.surface.blit(self.line_surface, (0,0))

    def reset(self):
        pass

    def close(self):
        pygame.quit()
                 
    def init_render(self):
        self.background = pygame.display.set_mode([400, 800])
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Tetris')

        self.surface = pygame.Surface(self.background.get_size())

        # Lines
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0,255,0))
        self.line_surface.set_colorkey((0,255,0))
        self.line_surface.set_alpha(120)

        self.rect = self.background.get_rect(topleft = (PADDING, PADDING))
        
        self.rendering = True
        
    def game_over(self):
        pass
    
    def won(self):
        pass
        
    def move(self):
        pass
       
    def new_game(self, board_index = 0):
        pass

    def handle_game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_program = True
            
            if event.type != pygame.KEYDOWN: continue
            match event.key:
                
                case pygame.K_ESCAPE: # Exit game
                    self.exit_program = True
                case pygame.K_SPACE: # Hard drop
                    pass 
                case pygame.K_LEFT: # Move piece left
                    pass
                case pygame.K_RIGHT: # Move piece right
                    pass
                case pygame.K_DOWN:
                    pass
                case pygame.K_UP:    
                    pass
                case pygame.K_p:
                    self.paused = self.paused

        
    def run(self):
        self.handle_game_events()

        if self.paused: 
            return
        
        self.render()
            
    def start(self):
        while not self.exit_program:
            self.run()
        pygame.quit()
        exit()
        
if __name__ == "__main__":
    game = Tetris()
    game.start()
