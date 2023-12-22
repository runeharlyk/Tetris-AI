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
        self.board = self._new_board()
        self.high_score = max(self.high_score, self.score)
        self.score = 0
        self.lines = 0
        self.level = 1
        self.held_shapes = []
        self.next_shapes = []
        self._get_new_shapes()

    # Heuristics
    def _count_holes(self, board:np.ndarray):
        cumsum_filled = np.cumsum(board != 0, axis=0)
        return np.sum((board == 0) & (cumsum_filled > 0))
    
    def _calculate_height_and_bumpiness(self, board:np.ndarray):
        heights = np.max(np.where(board != 0, len(board) - np.arange(len(board))[:, None], 0), axis=0)
        total_height = np.max(heights)
        bumpiness = np.sum(np.abs(np.diff(heights)))

        return total_height, bumpiness
    
    def _count_full_lines(self, board:np.ndarray):
        full_rows = np.all(board != 0, axis=1)
        return int(np.sum(full_rows))

    def _get_current_state(self, board:np.ndarray, shape:np.ndarray, offset:tuple):
        new_board = board.copy()
        self._place_shape(new_board, shape, offset)
        cleared_lines = self._count_full_lines(new_board)
        holes = self._count_holes(board)
        bumpiness, height = self._calculate_height_and_bumpiness(board)

        return np.array([cleared_lines, holes, bumpiness, height])

    def get_state(self, board:np.ndarray):
        cleared_lines = self._count_full_lines(board)
        holes = self._count_holes(board)
        bumpiness, height = self._calculate_height_and_bumpiness(board)

        return np.array([cleared_lines, holes, bumpiness, height])
    
    def get_possible_states(self):
        states = {}
        shape = self.shape
        shape_x = self.shape_x
        board = self.board.copy()
        _, cols = board.shape

        for rotation in range(4):
            rotated = self._rotate(board, shape, (shape_x, 0), rotation)
            max_x = int(cols - rotated.shape[1])
            for x in range(max_x):
                pos = [x, 0]
                while not self._check_collision(board, rotated, pos):
                    pos[1] += 1
                pos[1] -= 1
                states[(x, rotation)] = self._get_current_state(board, rotated, pos)

        return states

            # Check for each rotation
        
                # Check for each x position
    
    # Private tetris

    def _rotate_clockwise(self, shape:np.ndarray, times:int=1):
        return np.rot90(shape, times * -1)

    def _check_collision(self, board:np.ndarray, shape:np.ndarray, offset:tuple):
        off_x, off_y = offset
        shape_height, shape_width = shape.shape
        rows, cols = board.shape
        if off_x < 0 or off_x + shape_width > cols or off_y + shape_height > rows - 1:
            return True
        board_area = board[off_y:off_y + shape_height, off_x:off_x + shape_width]

        return np.any(np.logical_and(shape, board_area))

    def _place_shape(self, board:np.ndarray, shape:np.ndarray, offset:tuple):
        off_x, off_y = offset
        for cy, row in enumerate(shape):
            for cx, val in enumerate(row):
                board[cy+off_y-1][cx+off_x] += val

    def _rotate(self, board:np.ndarray, shape:np.ndarray, offset:tuple, times:int=1):
        new_shape = self._rotate_clockwise(shape, times)
        if not self._check_collision(board, new_shape, offset):
            return new_shape
        return shape
    
    def _move(self, board:np.ndarray, shape:np.ndarray, offset:tuple, delta_x:int):
        new_x = max(0, min(offset[0] + delta_x, board.shape[1] - shape.shape[1]))
        if self._check_collision(board, shape, (new_x, offset[1])):
            return offset[0]
        return new_x

    def _soft_drop(self, board:np.ndarray, shape:np.ndarray, offset:tuple):
        x, y = offset
        while not self._check_collision(board, shape, (x, y + 1)):
            y += 1
        return y
    
    def _new_board(self):
        return np.zeros((self.rows, self.cols), dtype=int)
    
    def _add_points(self, lines_cleared:int):
        self.lines += lines_cleared
        self.score += line_points[lines_cleared] * self.level

    def _get_new_random_shape(self):
        shape_index = np.random.randint(len(tetris_shapes))
        return tetris_shapes[shape_index].copy()

    def _get_new_shapes(self):
        self.next_shapes.extend([self._get_new_random_shape() for _ in range(4 - len(self.next_shapes))])
        self.shape = self.next_shapes.pop(0)
        self.shape_x = self.cols // 2 - len(self.shape[0]) // 2
        self.shape_y = 0

        if self._check_collision(self.board, self.shape, (self.shape_x, self.shape_y)):
            self.done = True   

    def _clear_lines(self, board:np.ndarray):
        full_rows = np.all(board != 0, axis=1)
        num_full_rows = np.sum(full_rows)
        if num_full_rows == 0: return 0
        non_full_rows = np.where(~full_rows)[0]
        board[num_full_rows:] = board[non_full_rows]
        board[:num_full_rows] = 0
        return int(num_full_rows)

    def _evaluate_position(self):
        if not self._check_collision(self.board, self.shape, (self.shape_x, self.shape_y)): return

        self._place_shape(self.board, self.shape, (self.shape_x, self.shape_y))
        self._get_new_shapes()
        cleared_lines = self._clear_lines(self.board)
        self._add_points(cleared_lines)
        print(self.get_state(self.board))

    # Actions
    def rotate(self, times:int=1):
        if self.done: return
        self.shape = self._rotate(self.board, self.shape, (self.shape_x, self.shape_y), times)

    def move(self, delta_x:int):
        if self.done: return
        self.shape_x = self._move(self.board, self.shape, (self.shape_x, self.shape_y), delta_x)

    def hold(self):
        if not self.held_shapes:
            self.held_shapes.append(self.shape)
            self._get_new_shapes()    
        else:
            shape = self.held_shapes.pop()
            self.held_shapes.append(self.shape)
            self.shape = shape

    def down(self):
        self.shape_y += 1
        return self._evaluate_position()

    def soft_drop(self):
        self.shape_y = self._soft_drop(self.board, self.shape, (self.shape_x, self.shape_y))
        return self._evaluate_position()

    def hard_drop(self):
        self.soft_drop()
        return self.down()

    def step(self, delta_x:int, rotation:int):
        self.rotate(rotation)
        self.move(delta_x)
        return self.hard_drop()




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
    

