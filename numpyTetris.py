from random import randrange as rand
import pygame, sys
import numpy as np

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

tetris_shapes = [
    np.array([[1, 1, 1], [0, 1, 0]]),
    np.array([[0, 2, 2], [2, 2, 0]]),
    np.array([[3, 3, 0], [0, 3, 3]]),
    np.array([[4, 0, 0], [4, 4, 4]]),
    np.array([[0, 0, 5], [5, 5, 5]]),
    np.array([[6, 6, 6, 6]]),
    np.array([[7, 7], [7, 7]])
]

line_points = [0, 100, 300, 500, 800]

class Tetris:
    def __init__(self, columns, rows):
        self.cols = columns
        self.rows = rows
        self.high_score = 0
        self.score = 0
        
        self.reset()

    def reset(self):
        self.done = False
        self.board = self.new_board()
        self.high_score = max(self.high_score, self.score)
        self.score = 0
        self.lines = 0
        self.level = 1
        self.held_shapes = []
        self.next_shapes = []
        self.new_shape()

    def rotate_clockwise(self):
        new_shape = np.rot90(self.shape, -1)
        if not self.check_collision(new_shape, (self.shape_x, self.shape_y)):
            self.shape = new_shape

    def check_collision(self, shape, offset):
        off_x, off_y = offset
        shape_height, shape_width = shape.shape
        if off_x < 0 or off_x + shape_width > self.cols or off_y + shape_height > self.rows:
            return True
        board_area = self.board[off_y:off_y + shape_height, off_x:off_x + shape_width]

        return np.any(np.logical_and(shape, board_area))

    def remove_row(self, row):
        new_row = np.zeros((1, self.board.shape[1]))
        self.board = np.vstack((new_row, np.delete(self.board, row, axis=0)))
    
    def place_shape(self, shape, shape_off):
        off_x, off_y = shape_off
        for cy, row in enumerate(shape):
            for cx, val in enumerate(row):
                self.board[cy+off_y-1][cx+off_x] += val
                
    def new_board(self):
        board = np.zeros((self.rows + 1, self.cols), dtype=int)
        board[-1] = 1
        return board
    
    def new_shape(self):
        shape_index = np.random.randint(len(tetris_shapes))
        self.shape = tetris_shapes[shape_index].copy()
        self.shape_x = self.cols // 2 - len(self.shape[0]) // 2
        self.shape_y = 0
        
        if self.check_collision(self.shape, (self.shape_x, self.shape_y)):
            self.done = True        

    def move(self, delta_x):
        if self.done: return

        new_x = self.shape_x + delta_x
        if new_x < 0:
            new_x = 0
        if new_x > self.cols - len(self.shape[0]):
            new_x = self.cols - len(self.shape[0])
        if not self.check_collision(self.shape, (new_x, self.shape_y)):
            self.shape_x = new_x

    def clear_lines(self):
        cleared = 0
        while True:
            for i, row in enumerate(self.board[:-1]):
                if 0 not in row:
                    cleared += 1
                    self.remove_row(i)
                    break
            else:
                break
        return cleared

    def add_points(self, lines_cleared):
        self.lines += lines_cleared
        self.score += line_points[lines_cleared] * self.level

    def evaluate_position(self):
        if self.check_collision(self.shape, (self.shape_x, self.shape_y)):
            self.place_shape(self.shape, (self.shape_x, self.shape_y))
            self.new_shape()
            cleared_lines = self.clear_lines()
            self.add_points(cleared_lines)

    def down(self):
        self.shape_y += 1
        self.evaluate_position()

    def hold(self):
        if not self.held_shapes:
            self.held_shapes.append(self.shape)
            self.new_shape()    
        else:
            shape = self.held_shapes.pop()
            self.held_shapes.append(self.shape)
            self.shape = shape

    def soft_drop(self):
        while not self.check_collision(self.shape, (self.shape_x, self.shape_y + 1)):
            self.shape_y += 1

    def hard_drop(self):
        self.soft_drop()
        self.down()

    # def step(self, action):


class TetrisApp(object):
    def __init__(self):
        self.game = Tetris(config['cols'], config['rows'])

        pygame.init()
        pygame.key.set_repeat(250,25)
        self.width = config['cell_size']*config['cols'] + config['cell_size'] * 10
        self.height = config['cell_size']*config['rows'] + config['cell_size']
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION) 
    
    def top_msg(self, msg):
        msg_image =  pygame.font.Font(pygame.font.get_default_font(), 12).render(msg, False, (255,255,255), (0,0,0))
        msgim_center_x, msgim_center_y = msg_image.get_size()
        msgim_center_x //= 2
    
        self.screen.blit(msg_image, (self.width // 2-msgim_center_x, 0))

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
    

    def quit(self):
        self.center_msg("Exiting...")
        pygame.display.update()
        sys.exit()

    def should_play(self):
        return not self.gameover and not self.paused
    
    def down(self):
        if not self.should_play(): return
        self.game.down()
    
    def rotate_stone(self):
        if self.gameover or self.paused: return
        self.game.rotate_clockwise()
    
    def toggle_pause(self):
        self.paused = not self.paused
    
    def start_game(self):
        if self.game.done:
            self.game.reset()
    
    def run(self):
        self.key_actions = {
            'ESCAPE':   self.quit,
            'LEFT':     lambda: self.game.move(-1),
            'RIGHT':    lambda: self.game.move(+1),
            'DOWN':     self.down,
            'UP':       self.rotate_stone,
            'p':        self.toggle_pause,
            'c':        self.game.hold,
            'v':        self.game.soft_drop,
            'b':        self.game.hard_drop,
            'SPACE':    self.start_game
        }
        
        self.gameover = False
        self.paused = False
        
        pygame.time.set_timer(pygame.USEREVENT+1, config['delay'])
        self.dont_burn_my_cpu = pygame.time.Clock()
        while 1:
            self.render()

    def render(self):
        self.screen.fill((0,0,0))
        if self.game.done:
            self.center_msg("Game Over! \nPress space to continue")
        else:
            if self.paused:
                self.center_msg("Paused")
            else:
                self.top_msg(f'Score: {self.game.score}')
                if self.game.held_shapes:
                    self.draw_matrix(self.game.held_shapes[0], (1, 1))
                self.draw_matrix(self.game.board, (5, 1))
                self.draw_matrix(self.game.shape,
                                    (self.game.shape_x + 5,
                                    self.game.shape_y + 1))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT+1:
                self.down()
            elif event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                for key in self.key_actions:
                    if event.key == eval("pygame.K_"+key):
                        self.key_actions[key]()
                
        self.dont_burn_my_cpu.tick(config['maxfps'])

if __name__ == '__main__':
    App = TetrisApp()
    App.run()
    

