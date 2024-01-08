import unittest
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from environment.tetris import Tetris
env = Tetris(10, 20)

class TestNumberOfActionFunction(unittest.TestCase):
    def test_number_actions_with_holding_piece_t_duplicate(self): # Most unique rotations
        env.shape = env.SHAPES[0]
        env.held_shapes.append(env.SHAPES[0])

        actual_actions = env.get_possible_actions()

        self.assertEqual(len(actual_actions), 34)

    def test_number_actions_with_holding_piece_s_duplicate(self): # Most unique rotations
        env.shape = env.SHAPES[1]
        env.held_shapes.append(env.SHAPES[1])

        actual_actions = env.get_possible_actions()

        self.assertEqual(len(actual_actions), 17)

if __name__ == '__main__':
    unittest.main()
