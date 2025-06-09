import random

import numpy as np

import config
from utils.matrix_operations import get_cell_neighbours_2d, get_cell_neighbours_3d


def prob_reproduction(game_matrix: np.ndarray, pay_off_matrix: np.ndarray, indices):
    if config.num_of_dims == 2:
        return reproduction_2d(game_matrix, pay_off_matrix, indices)

    if config.num_of_dims == 3:
        return reproduction_3d(game_matrix, pay_off_matrix, indices)


def reproduction_2d(game_matrix: np.ndarray, pay_off_matrix: np.ndarray, indices):
    for idx in indices:
        neighbours = get_cell_neighbours_2d(idx[0], idx[1])
        fit_list = []
        for n in neighbours:
            fit_list.append(pay_off_matrix[n[0], n[1]])

        fit_list = np.array(fit_list)
        fit_list /= np.sum(fit_list)

        p_value = random.random()

        best_arg = -1

        for i in range(len(fit_list)):
            p_value -= fit_list[i]
            if p_value < 0:
                best_arg = i
                break


        best_n = neighbours[best_arg]
        game_matrix[idx[0], idx[1]] = game_matrix[best_n[0], best_n[1]]

    return game_matrix

def reproduction_3d(game_matrix: np.ndarray, pay_off_matrix: np.ndarray, indices):
    for idx in indices:
        neighbours = get_cell_neighbours_3d(idx[0], idx[1], idx[2])
        fit_list = []
        for n in neighbours:
            fit_list.append(pay_off_matrix[n[0], n[1], n[2]])

        fit_list = np.array(fit_list)
        fit_list /= np.sum(fit_list)

        p_value = random.random()

        best_arg = -1

        for i in range(len(fit_list)):
            p_value -= fit_list[i]
            if p_value < 0:
                best_arg = i
                break

        best_n = neighbours[best_arg]
        game_matrix[idx[0], idx[1], idx[2]] = game_matrix[best_n[0], best_n[1], best_n[2]]

    return game_matrix