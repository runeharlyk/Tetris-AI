import unittest
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from environment.tetris import Tetris

class TestBridgeCountFunction(unittest.TestCase):
    def test_no_bridge_count(self):
        env = Tetris(8, 16)
        env.shape = Tetris.SHAPES[0]
        env.rotate(2)
        env.hard_drop()
        self.assertEqual(env._count_bridges(env.board), 0)

    def test_many_bridge_count(self):
        env = Tetris(8, 16)
        for _ in range(len(Tetris.SHAPES)):
            env.shape = Tetris.SHAPES[0]
            env.shape_x = 4
            env.hard_drop()
        self.assertEqual(env._count_bridges(env.board), 14)

class TestHeightAndBumpinesssFunction(unittest.TestCase):
    def test_height(self):
        env = Tetris(8, 16)
        env.shape = Tetris.SHAPES[5]
        env.rotate(1)
        env.hard_drop()
        self.assertEqual(env._calculate_height_and_bumpiness(env.board)[0], 5)

    def test_bumpiness(self):
        env = Tetris(8, 16)
        env.shape = Tetris.SHAPES[5]
        env.rotate(2)
        env.hard_drop()
        self.assertEqual(env._calculate_height_and_bumpiness(env.board)[1], 4)

class TestCountFullLinesFunction(unittest.TestCase):
    def test_count_full_lines(self):
        env = Tetris(8, 16)
        env._place_shape(env.board, Tetris.SHAPES[5], (0, 1))
        env._place_shape(env.board, Tetris.SHAPES[5], (4, 1))
        self.assertEqual(env._count_full_rows(env.board), 1)

if __name__ == '__main__':
    unittest.main()
