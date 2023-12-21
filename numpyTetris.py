from random import randrange as rand
import pygame, sys
import numpy as np

# The configuration
config = {
    'cell_size':    20,
    'cols':        8,
    'rows':        16,
    'delay':    750,
    'maxfps':    30
}

colors = [
(0,   0,   0  ),
(255, 0,   0  ),
(0,   150, 0  ),
(0,   0,   255),
(255, 120, 0  ),
(255, 255, 0  ),
(180, 0,   255),
(0,   220, 220)
]

# Define the shapes of the single parts
tetris_shapes = [
    np.array([[1, 1, 1], [0, 1, 0]]),
    np.array([[0, 2, 2], [2, 2, 0]]),
    np.array([[3, 3, 0], [0, 3, 3]]),
    np.array([[4, 0, 0], [4, 4, 4]]),
    np.array([[0, 0, 5], [5, 5, 5]]),
    np.array([[6, 6, 6, 6]]),
    np.array([[7, 7], [7, 7]])
]

class Tetris:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.held_shapes = []
        self.next_shapes = []

        self.reset()

    def reset(self):
        self.score = 0
        self.lines = 0
        self.level = 0
        self.board = self.new_board()

    def rotate_clockwise(self, shape):
        return np.rot90(shape, -1)

    def check_collision(self, shape, offset):
        off_x, off_y = offset
        for cy, row in enumerate(shape):
            for cx, cell in enumerate(row):
                try:
                    if cell and self.board[ cy + off_y ][ cx + off_x ]:
                        return True
                except IndexError:
                    return True
        return False

    def remove_row(self, row):
        new_row = np.zeros((1, self.board.shape[1]))
        self.board = np.vstack((new_row, np.delete(self.board, row, axis=0)))
    
    def place_shape(self, shape, shape_off):
        off_x, off_y = shape_off
        for cy, row in enumerate(shape):
            for cx, val in enumerate(row):
                self.board[cy+off_y-1][cx+off_x] += val
                
    def new_board(self):
        board = np.zeros((config['rows']+1, config['cols']), dtype=int)
        board[-1] = 1
        return board
    
    def new_shape(self):
        pass        

class TetrisApp(object):
    def __init__(self):
        self.game = Tetris(0, 0)

        pygame.init()
        pygame.key.set_repeat(250,25)
        self.width = config['cell_size']*config['cols']
        self.height = config['cell_size']*config['rows']
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION) # We do not need
                                                     # mouse movement
                                                     # events, so we
                                                     # block them.
        self.init_game()
    
    def new_stone(self):
        self.stone = tetris_shapes[rand(len(tetris_shapes))]
        self.stone_x = int(config['cols'] / 2 - len(self.stone[0])/2)
        self.stone_y = 0
        
        if self.game.check_collision(self.stone, (self.stone_x, self.stone_y)):
            self.gameover = True
    
    def init_game(self):
        self.game.reset()
        self.new_stone()
    
    def center_msg(self, msg):
        for i, line in enumerate(msg.splitlines()):
            msg_image =  pygame.font.Font(
                pygame.font.get_default_font(), 12).render(
                    line, False, (255,255,255), (0,0,0))
        
            msgim_center_x, msgim_center_y = msg_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2
        
            self.screen.blit(msg_image, (
              self.width // 2-msgim_center_x,
              self.height // 2-msgim_center_y+i*22))
    
    def draw_matrix(self, matrix, offset):
        off_x, off_y  = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen,
                        colors[int(val)],
                        pygame.Rect(
                            (off_x+x) *
                              config['cell_size'],
                            (off_y+y) *
                              config['cell_size'], 
                            config['cell_size'],
                            config['cell_size']),0)
    
    def move(self, delta_x):
        if not self.gameover and not self.paused:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > config['cols'] - len(self.stone[0]):
                new_x = config['cols'] - len(self.stone[0])
            if not self.game.check_collision(self.stone, (new_x, self.stone_y)):
                self.stone_x = new_x
    def quit(self):
        self.center_msg("Exiting...")
        pygame.display.update()
        sys.exit()
    
    def drop(self):
        if not self.gameover and not self.paused:
            self.stone_y += 1
            if self.game.check_collision(self.stone, (self.stone_x, self.stone_y)):
                self.game.place_shape(self.stone, (self.stone_x, self.stone_y))
                self.new_stone()
                while True:
                    for i, row in enumerate(self.game.board[:-1]):
                        if 0 not in row:
                            self.game.remove_row(i)
                            break
                    else:
                        break
    
    def rotate_stone(self):
        if not self.gameover and not self.paused:
            new_stone = self.game.rotate_clockwise(self.stone)
            if not self.game.check_collision(new_stone, (self.stone_x, self.stone_y)):
                self.stone = new_stone
    
    def toggle_pause(self):
        self.paused = not self.paused
    
    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False
    
    def run(self):
        key_actions = {
            'ESCAPE':    self.quit,
            'LEFT':        lambda:self.move(-1),
            'RIGHT':    lambda:self.move(+1),
            'DOWN':        self.drop,
            'UP':        self.rotate_stone,
            'p':        self.toggle_pause,
            'SPACE':    self.start_game
        }
        
        self.gameover = False
        self.paused = False
        
        pygame.time.set_timer(pygame.USEREVENT+1, config['delay'])
        dont_burn_my_cpu = pygame.time.Clock()
        while 1:
            self.screen.fill((0,0,0))
            if self.gameover:
                self.center_msg("""Game Over!
Press space to continue""")
            else:
                if self.paused:
                    self.center_msg("Paused")
                else:
                    self.draw_matrix(self.game.board, (0,0))
                    self.draw_matrix(self.stone,
                                     (self.stone_x,
                                      self.stone_y))
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT+1:
                    self.drop()
                elif event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_"
                        +key):
                            key_actions[key]()
                    
            dont_burn_my_cpu.tick(config['maxfps'])

if __name__ == '__main__':
    App = TetrisApp()
    App.run()
    

