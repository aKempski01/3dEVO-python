import numpy as np

import config
from utils.matrix_operations import get_cell_neighbours_2d, get_cell_neighbours_3d


def det_reproduction(game_matrix: np.ndarray, pay_off_matrix: np.ndarray, indices):
    if config.num_of_dims == 2:
        return reproduction_2d(game_matrix, pay_off_matrix, indices)

    if config.num_of_dims == 3:
        return reproduction_3d(game_matrix, pay_off_matrix, indices)


def reproduction_2d(game_matrix: np.ndarray, pay_off_matrix: np.ndarray, indices):
    _gm = game_matrix.copy()
    for idx in indices:
        neighbours = get_cell_neighbours_2d(idx[0], idx[1])
        fit_list = []
        for n in neighbours:
            fit_list.append(pay_off_matrix[n[0], n[1]])

        best_n = neighbours[np.argmax(fit_list)]

        _gm[idx[0], idx[1]] = game_matrix[best_n[0], best_n[1]]

    return _gm



def reproduction_3d(game_matrix: np.ndarray, pay_off_matrix: np.ndarray, indices):
    _gm = game_matrix.copy()
    for idx in indices:
        neighbours = get_cell_neighbours_3d(idx[0], idx[1], idx[2])
        fit_list = []
        for n in neighbours:
            fit_list.append(pay_off_matrix[n[0], n[1], n[2]])

        best_n = neighbours[np.argmax(fit_list)]

        _gm[idx[0], idx[1], idx[2]] = game_matrix[best_n[0], best_n[1], best_n[2]]

    return _gm


