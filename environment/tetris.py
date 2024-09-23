import random
import numpy as np
from utils.heuristics import Heuristics

line_points = [0, 40, 100, 300, 1200]
delay_per_level = [48, 43, 38, 33, 28, 23, 18, 13, 8, 6, 5, 5, 5, 4, 4, 4, 3, 3, 3, 2] # <= 19 = 1 

class Tetris:
    SHAPES = [
        np.array([[1, 1, 1], [0, 1, 0]], dtype=np.uint8),
        np.array([[0, 2, 2], [2, 2, 0]], dtype=np.uint8),
        np.array([[3, 3, 0], [0, 3, 3]], dtype=np.uint8),
        np.array([[4, 0, 0], [4, 4, 4]], dtype=np.uint8),
        np.array([[0, 0, 5], [5, 5, 5]], dtype=np.uint8),
        np.array([[6, 6, 6, 6]], dtype=np.uint8),
        np.array([[7, 7], [7, 7]], dtype=np.uint8),
    ]

    def __init__(self, columns:int, rows:int, use_level:bool=True):
        self.cols = columns
        self.rows = rows
        self.high_score = 0
        self.score = 0
        self.use_level = use_level
        self.heuristics = Heuristics()
        
        self.reset()

    def __str__(self):
        out = f"score:{self.score}"
        out += f"\nlines:{self.score}"
        out += f"\npieces:{self.score}"
        out += f"\nshape:"
        for i in range(len(self.shape)):
            out += f"\n{self.shape[i]}"
        out += f"\nboard:"
        for row in self.board:
            out += f"\n{row}"
        return out

    def reset(self) -> np.ndarray[int]:
        self.done = False
        self.paused = False
        self.board = self._new_board()
        self.high_score = max(self.high_score, self.score)
        self.score = 0
        self.prev_score = 0
        self.lines = 0
        self.pieces = 0
        self.level = 1
        self.held_shapes = []
        self.next_shapes = []
        self.bag = []
        self._get_new_shapes()
        self.state = np.array([0, 0, 0, 0, 0])
        self.line_clear_types = {0:0, 1:0, 2:0, 3:0, 4:0}
        return self.state

    def _get_current_state(self, board:np.ndarray, shape:np.ndarray, offset:tuple) -> np.ndarray[int]:
        new_board = board.copy()
        self._place_shape(new_board, shape, offset)
        return self.heuristics.get_heuristics(new_board)
    
    def _get_state(self, x, rotation, holding):
        board = self.board.copy()
        shape = self.held_shapes[0] if holding else self.shape
        rotated = self._rotate(self.board, shape, (self.shape_x, 0), rotation)
        y = 0
        while not self._check_collision(board, rotated, (x, y + 1)):
            y += 1
        return self._get_current_state(board[:], rotated, (x, y))

    def get_possible_actions(self):
        rotations = []
        actions = []

        for holding in range(2):
            for rotation in range(4): 
                rotated = self._rotate(self.board, self.shape, (self.shape_x, 0), rotation)
                if str(rotated) in rotations:
                    continue
                max_x = int(self.cols - rotated.shape[1] + 1)
                for x in range(max_x):
                    actions.append((x, rotation, holding))
                rotations.append(str(rotated))
            self.hold()
        return actions 
    
    def get_possible_states(self):
        next_actions = self.get_possible_actions() 
        return {action:self._get_state(*action) for action in next_actions}

    # Private tetris

    def _rotate_clockwise(self, shape:np.ndarray, times:int=1) -> np.ndarray:
        return np.rot90(shape, times * -1)

    def _check_collision(self, board:np.ndarray, shape:np.ndarray, offset:tuple) -> int:
        off_x, off_y = offset
        shape_height, shape_width = shape.shape
        rows, cols = board.shape
        if off_x < 0 or off_x + shape_width > cols or off_y + shape_height > rows:
            return True
        board_area = board[off_y:off_y + shape_height, off_x:off_x + shape_width]

        return np.any(np.logical_and(shape, board_area))

    def _place_shape(self, board:np.ndarray, shape:np.ndarray, offset:tuple) -> None:
        off_x, off_y = offset
        for cy, row in enumerate(shape):
            for cx, val in enumerate(row):
                board[cy+off_y-1][cx+off_x] += val

    def _rotate(self, board:np.ndarray, shape:np.ndarray, offset:tuple, times:int=1) -> np.ndarray:
        new_shape = self._rotate_clockwise(shape, times)
        if not self._check_collision(board, new_shape, offset):
            return new_shape
        return shape
    
    def _move(self, board:np.ndarray, shape:np.ndarray, offset:tuple, delta_x:int) -> int:
        new_x = max(0, min(offset[0] + delta_x, board.shape[1] - shape.shape[1]))
        if self._check_collision(board, shape, (new_x, offset[1])):
            return offset[0]
        return new_x

    def _soft_drop(self, board:np.ndarray, shape:np.ndarray, offset:tuple) -> int:
        x, y = offset
        while not self._check_collision(board, shape, (x, y + 1)):
            y += 1
        return y

    def _level_multiplier(self):
        return self.level if self.use_level else 1

    def _new_board(self) -> np.ndarray[np.ndarray[np.uint8]]:
        return np.zeros((self.rows, self.cols), dtype=np.uint8)

    def _add_points(self, lines_cleared: int) -> int:
        self.lines += lines_cleared
        score = line_points[lines_cleared] * self._level_multiplier()
        self.score += score
        return score

    def _get_new_random_shape(self) -> np.ndarray[np.ndarray[np.uint8]]:
        if not self.bag:
            self.bag = self.SHAPES.copy()
            random.shuffle(self.bag)
        return self.bag.pop()

    def _get_new_shapes(self):
        self.next_shapes.extend([self._get_new_random_shape() for _ in range(4 - len(self.next_shapes))])
        self.shape = self.next_shapes.pop(0)
        self.shape_x = self.cols // 2 - len(self.shape[0]) // 2
        self.shape_y = 0

        if self._check_collision(self.board, self.shape, (self.shape_x, self.shape_y)):
            self.done = True   

    def _clear_lines(self, board:np.ndarray) -> int:
        full_rows = np.all(board != 0, axis=1)
        num_full_rows = np.sum(full_rows)
        if num_full_rows == 0: return 0
        non_full_rows = np.where(~full_rows)[0]
        board[num_full_rows:] = board[non_full_rows]
        board[:num_full_rows] = 0
        self.lines += int(num_full_rows)
        return int(num_full_rows)

    def _evaluate_position(self):
        if not self._check_collision(self.board, self.shape, (self.shape_x, self.shape_y)): return

        self.pieces += 1
        self._place_shape(self.board, self.shape, (self.shape_x, self.shape_y))
        cleared_lines = self._clear_lines(self.board)
        self.line_clear_types[cleared_lines] += 1
        self.level = self.lines // 10 + 1
        self._get_new_shapes()
        self._add_points(cleared_lines)

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
            self.move(0)

    def down(self) -> tuple[bool, int, int]:
        self.shape_y += 1
        self._evaluate_position()
        return self.done, self.score, self.score - self.prev_score

    def soft_drop(self):
        self.prev_score = self.score
        prev_y = self.shape_y
        self.shape_y = self._soft_drop(self.board, self.shape, (self.shape_x, self.shape_y))
        self.score += self.shape_y - prev_y
        
    def hard_drop(self) -> tuple[bool, int, int]:
        self.soft_drop()
        return self.down()

    def step(self, delta_x:int, rotation:int, holding) -> tuple[bool, int, int]:
        if holding:
            self.hold()
        self.rotate(rotation)
        self.move(delta_x - self.shape_x)
        return self.hard_drop()
