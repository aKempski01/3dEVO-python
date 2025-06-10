import random

import numpy as np

import config
from utils.matrix_operations import get_cell_neighbours_2d, get_cell_neighbours_3d


def weighted_reproduction(game_matrix: np.ndarray, pay_off_matrix: np.ndarray, indices):
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

        if len(fit_list) > config.num_of_cells_for_mean:
            for r in range(len(fit_list) - config.num_of_cells_for_mean):
                to_remove = np.argmin(fit_list)
                fit_list.pop(to_remove)
                neighbours.pop(to_remove)

        new_val = np.zeros(config.num_of_phenotypes)
        for i in range(len(neighbours)):
            new_val += game_matrix[neighbours[i]]*fit_list[i]

        new_val /= np.sum(new_val)
        _gm[idx] = new_val
    return _gm

def reproduction_3d(game_matrix: np.ndarray, pay_off_matrix: np.ndarray, indices):
    pass