import unittest
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from utils.heuristics import Heuristics
from helper import load_board, theory
heuristics = Heuristics()

class TestBridgeCountFunction(unittest.TestCase):
    @theory(((1, 0), (2, 0), (3, 0)))
    def test_many_bridge_count(self, board_id, bridges):
        board = load_board(board_id)

        actual_bridges = heuristics._count_bridges(board)

        self.assertEqual(actual_bridges, bridges)

class TestHeightAndBumpinesssFunction(unittest.TestCase):
    @theory(((1, 0), (2, 4), (3, 4)))
    def test_height(self, board_id, max_height):
        board = load_board(board_id)

        _, _, actual_max_height, _ = heuristics._calculate_max_height_and_bumpiness(board)

        self.assertEqual(actual_max_height, max_height)

    @theory(((1, 0), (2, 4), (3, 0)))
    def test_bumpiness(self, board_id, bumpiness):
        board = load_board(board_id)

        _, _, _, actual_bumpiness = heuristics._calculate_max_height_and_bumpiness(board)

        self.assertEqual(actual_bumpiness, bumpiness)

class TestCountFullLinesFunction(unittest.TestCase):
    @theory(((1, 0), (2, 0), (3, 4)))
    def test_count_full_lines(self, board_id, full_rows):
        board = load_board(board_id)

        actual_full_rows = heuristics._count_full_rows(board)

        self.assertEqual(actual_full_rows, full_rows)
        
class TestPillarCheckFunction(unittest.TestCase):
    @theory(((1, 0), (2, 1)))
    def test_check_pillar(self, board_id, have_pillar):
        board = load_board(board_id)

        actual_have_pillar = heuristics._check_for_pillar(board)

        self.assertEqual(actual_have_pillar, have_pillar)


if __name__ == '__main__':
    unittest.main()
