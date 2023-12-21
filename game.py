import numpy as np
import random

from config import *

class Tetris:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = np.zeros(shape=(width, height))

        # State size (Clearede lines, bumpiness, holes, height)
        self.state_size = 4

        # For running the engine
        self.score = -1
        self.anchor = None
        self.shape = None

        self._shape_counts = [0] * len(shapes)
        self.held_piece = [self._new_piece()]
        self.next_piece = [self._new_piece()]

        self.reset()

    def rotated(self, shape):
        return [(-j, i) for i, j in shape]

    def is_occupied(self, shape, anchor, board):
        for i, j in shape:
            x, y = anchor[0] + i, anchor[1] + j
            if y < 0:
                continue
            if x < 0 or x >= board.shape[0] or y >= board.shape[1] or board[x, y]:
                return True
        return False

    def soft_drop(self, shape, anchor, board):
        new_anchor = (anchor[0], anchor[1] + 1)
        return (shape, anchor) if self.is_occupied(shape, new_anchor, board) else (shape, new_anchor)

    def hard_drop(self, shape, anchor, board):
        while True:
            _, anchor_new = self.soft_drop(shape, anchor, board)
            if anchor_new == anchor:
                return shape, anchor_new
            anchor = anchor_new

    def _choose_shape(self):
        max_count = max(self._shape_counts)

        tetromino = None
        valid_tetrominos = [shape_names[i] for i in range(len(shapes)) if self._shape_counts[i] < max_count]
        if len(valid_tetrominos) == 0:
            tetromino = random.sample(shape_names, 1)[0]
        else:
            tetromino = random.sample(valid_tetrominos, 1)[0]
        self._shape_counts[shape_names.index(tetromino)] += 1
        return shapes[tetromino]

    def _new_piece(self):
        self.anchor = (self.width / 2, 1)
        self.shape = self._choose_shape()

    def _has_dropped(self):
        return self.is_occupied(self.shape, (self.anchor[0], self.anchor[1] + 1), self.board)

    def _clear_lines(self):
        can_clear = [np.all(self.board[:, i]) for i in range(self.height)]
        new_board = np.zeros_like(self.board)
        j = self.height - 1
        for i in range(self.height - 1, -1, -1):
            if not can_clear[i]:
                new_board[:, j] = self.board[:, i]
                j -= 1
        self.score += sum(can_clear)    
        self.board = new_board

        return sum(can_clear)

    def valid_action_count(self):
        valid_action_sum = 0

        for value, fn in self.value_action_map.items():
            # If they're equal, it is not a valid action
            if fn(self.shape, self.anchor, self.board) != (self.shape, self.anchor):
                valid_actiohn_sum += 1

        return valid_action_sum

    def step(self, action):
        pos = [action[0], 0]

        # Rotate shape n times
        for rot in range(action[1]):
            self.shape = self.rotated(self.shape)

        self.shape, self.anchor = self.hard_drop(self.shape, pos, self.board)

        done = False
        
        self._set_piece(True)
        cleared_lines = self._clear_lines()
        _score = self.score
        if np.any(self.board[:, 0]):
            self.reset()
            done = True
        else:
            self._new_piece()

        state = self.get_current_state(self.board)
        
        return state, _score, cleared_lines, done

    def reset(self):
        self.time = 0
        self.score = 0
        self.level = 1
        self.lines = 0
        self._new_piece()
        self.board = np.zeros_like(self.board)

        return np.array([0 for _ in range(self.state_size)])

    def _set_piece(self, on):
        """To lock a piece in the board"""
        for i, j in self.shape:
            x, y = i + self.anchor[0], j + self.anchor[1]
            if x < self.width and x >= 0 and y < self.height and y >= 0:
                self.board[int(self.anchor[0] + i), int(self.anchor[1] + j)] = on

    def _clear_line_dqn(self, board):
        can_clear = [np.all(board[:, i]) for i in range(self.height)]
        new_board = np.zeros_like(board)
        j = self.height - 1
        for i in range(self.height - 1, -1, -1):
            if not can_clear[i]:
                new_board[:, j] = self.board[:, i]
                j -= 1
        self.score += sum(can_clear)    
        board = new_board

        return sum(can_clear), board

    def get_bumpiness_height(self, board):
        bumpiness = 0
        columns_height = [0 for _ in range(self.width)]

        for i in range(self.width): 
            for j in range(self.height):
                if board.T[j][i]:
                    columns_height[i] = self.height - j
                    break
        for i in range(1, len(columns_height)):
            bumpiness += abs(columns_height[i] - columns_height[i-1])

        return bumpiness, sum(columns_height)

    def get_holes(self, board):
        holes = 0

        for col in zip(*board.T):
            row = 0
            while row < self.height and col[row] == 0:
                row += 1
            holes += len([x for x in col[row + 1:] if x == 0])

        return holes

    def get_current_state(self, board):
        # Getting lines which can be cleared and the new cleared board
        cleared_lines, board = self._clear_line_dqn(board)

        # Getting number of holes that are impossible to fill
        holes = self.get_holes(board)

        # Getting bumpiness / sum of difference between each adjacent column
        bumpiness, height = self.get_bumpiness_height(board)

        return np.array([cleared_lines, holes, bumpiness, height])


    def get_next_states(self):
        """To get all possible state from current shape"""
        old_shape = self.shape
        old_anchor = self.anchor
        states = {}
        # Loop to try each posibilities
        for rotation in range(4):
            max_x = int(max([s[0] for s in self.shape]))
            min_x = int(min([s[0] for s in self.shape]))

            for x in range(abs(min_x), self.width - max_x):
                # Try current position
                pos = [x, 0]
                while not self.is_occupied(self.shape, pos, self.board):
                    pos[1] += 1
                pos[1] -= 1

                self.anchor = pos
                self._set_piece(True)
                states[(x, rotation)] = self.get_current_state(self.board[:])
                self._set_piece(False)
                self.anchor = old_anchor

            self.shape = self.rotated(self.shape)
        return states

