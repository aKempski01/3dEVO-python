import numpy as np
from utils.enums import NeighborhoodType, ProblemType
from fitness.loss_funs import hawk_dove

import config
from utils.matrix_operations import get_cell_neighbours_2d, get_cell_neighbours_3d


def fitness_fun(game_matrix: np.ndarray):
    if config.num_of_dims == 2:
        return fitness_2d(game_matrix)

    if config.num_of_dims == 3:
        return fitness_3d(game_matrix)


def fitness_2d(game_matrix: np.ndarray):
    fit_array = np.zeros([config.pop_length]*config.num_of_dims)

    for x in range(config.pop_length):
        for y in range(config.pop_length):
            neighbours = get_cell_neighbours_2d(x, y)

            for i in range(config.num_of_phenotypes):
                for j in range(config.num_of_phenotypes):
                    f = fitness_pointer(i,j) * game_matrix[x, y, i]

                    for n in neighbours:
                        fit_array[x][y] += f * game_matrix[n[0], n[1], j]

    return fit_array


def fitness_3d(game_matrix: np.ndarray):
    fit_array = np.zeros([config.pop_length] * config.num_of_dims)

    for x in range(config.pop_length):
        for y in range(config.pop_length):
            for z in range(config.pop_length):
                neighbours = get_cell_neighbours_3d(x, y, z)
                for i in range(config.num_of_phenotypes):
                    for j in range(config.num_of_phenotypes):
                        f = fitness_pointer(i, j) * game_matrix[x, y, z, i]

                        for n in neighbours:
                            fit_array[x][y][z] += f * game_matrix[n[0], n[1], n[2], j]

    return fit_array






def fitness_pointer(player, enemy):
    if config.problem_type == ProblemType.HAWKDOVE:
        return hawk_dove(player, enemy)


