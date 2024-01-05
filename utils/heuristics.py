import numpy as np


class Heuristics:
    def __init__(self, ):
        pass
    
    def _count_bridges(self, board:np.ndarray):
        bridge_mask = board != 0
        empty_count = 0

        for col in range(board.shape[1]):
            if np.any(bridge_mask[:-1, col]):
                bridge_row = np.argmax(bridge_mask[:, col])
                empty_count += np.sum(board[bridge_row:, col] == 0)

        return empty_count
    
    def _calculate_height_and_bumpiness(self, board:np.ndarray):
        heights = np.max(np.where(board != 0, len(board) - np.arange(len(board))[:, None], 0), axis=0)
        max_height = np.max(heights)
        bumpiness = np.sum(np.abs(np.diff(heights)))

        return max_height, bumpiness
    
    def _count_full_rows(self, board:np.ndarray):
        full_rows = np.all(board != 0, axis=1)
        return int(np.sum(full_rows))

    def get_heuristics(self, board:np.ndarray):
        cleared_lines = self._count_full_rows(board)
        holes = self._count_bridges(board)
        bumpiness, height = self._calculate_height_and_bumpiness(board)

        return np.array([cleared_lines, holes, bumpiness, height])

    def get_state(self, board:np.ndarray):
        cleared_lines = self._count_full_rows(board)
        bridges = self._count_bridges(board)
        bumpiness, height = self._calculate_height_and_bumpiness(board)
        return np.array([cleared_lines, bridges, bumpiness, height])