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
    
    def _calculate_max_height_and_bumpiness(self, board:np.ndarray):
        heights = self._get_heights(board)
        max_height = np.max(heights)
        min_height = np.min(heights)
        mean_heights = np.mean(heights)
        bumpiness = np.sum(np.abs(np.diff(heights)))

        return min_height, mean_heights, max_height, bumpiness
    
    def _count_full_rows(self, board:np.ndarray):
        full_rows = np.all(board != 0, axis=1)
        return int(np.sum(full_rows))
    
    def _check_for_pillar(self, board:np.ndarray):
        empty=[]
        previous_row=[1]*board.shape[1]
        previous_i = 0
        for row in np.where(board != 0,1,0)[::-1]:
            i = np.argmin(row)
            if np.sum(row) == board.shape[1]-1:
                if len(empty) == 0 and previous_row[i]:
                    empty=[]
                    empty.append(i)
                    previous_i = i
                elif previous_i == i:
                    empty.append(i)
                    previous_i = i
            else:
                empty = []
            if len(empty) == 4 and len(set(empty)) == 1:
                return 1
        return 0

    def get_heuristics(self, board:np.ndarray):
        cleared_lines = self._count_full_rows(board)
        holes = self._count_bridges(board)
        min_height, mean_heights, max_height, bumpiness = self._calculate_max_height_and_bumpiness(board)
        check_pillar = self._check_for_pillar(board)
        return np.array([cleared_lines, holes, bumpiness, max_height,check_pillar])
    
    def _get_heights(self, board):
        return np.max(np.where(board != 0, len(board) - np.arange(len(board))[:, None], 0), axis=0)
