import numpy as np
import random
from utils.Enums import SpatialityStrategy
from utils.ParamHandler import ParamHandler


def get_game_matrix(param_handler: ParamHandler) -> np.ndarray:
    if param_handler.initial_matrix_path != None:
        return get_game_matrix_from_file(param_handler)

    if param_handler.num_dim == 2:
        return get_game_matrix_2d(param_handler)

    elif param_handler.num_dim == 3:
        return get_game_matrix_3d(param_handler)

    else:
        raise ValueError('Game matrix dimension must be 2 or 3')




def get_game_matrix_2d(ph: ParamHandler) -> np.ndarray:
    if ph.spatiality_strategy == SpatialityStrategy.MIXED:
        game_matrix = np.random.random([ph.population_length] * 2 + [ph.num_phenotypes])

        for i in range(ph.num_phenotypes):
            w = ph.initial_probability[i] / np.sum(game_matrix[:, :, i])
            game_matrix[:, :, i] *= w

        gm = np.sum(game_matrix, axis=-1)
        for i in range(ph.num_phenotypes):

            game_matrix[:, :, i] /= gm
        return game_matrix



    if ph.spatiality_strategy == SpatialityStrategy.SPATIAL:

        game_matrix = np.zeros([ph.population_length] * ph.num_dim + [ph.num_phenotypes])

        for i in range(ph.num_phenotypes - 1):
            idx = np.argwhere(np.sum(game_matrix, axis=-1) == 0)
            idx = idx[random.sample(range(0, idx.shape[0] - 1), int(ph.population_length ** ph.num_dim * ph.initial_probability[i])), :]

            game_matrix[idx[:, 0], idx[:, 1], i] = 1

        idx = np.argwhere(np.sum(game_matrix, axis=-1) == 0)

        game_matrix[idx[:, 0], idx[:, 1], -1] = 1
        return game_matrix

    else:
        raise ValueError('Unknown spatiality strategy: {}'.format(ph.spatiality_strategy))


def get_game_matrix_3d(ph: ParamHandler):


    if ph.spatiality_strategy == SpatialityStrategy.MIXED:
        game_matrix = np.random.random([ph.population_length] * ph.num_dim + [ph.num_phenotypes])

        for i in range(ph.num_phenotypes):
            w = ph.initial_probability[i] / np.sum(game_matrix[:, :, :, i])
            # w = list(ph.initial_probability.values())[i]/np.sum(game_matrix[:, :, i])
            game_matrix[:, :, :, i] *= w

        gm = np.sum(game_matrix, axis=-1)
        for i in range(ph.num_phenotypes):
            game_matrix[:, :, :, i] /= gm
        return game_matrix


    if ph.spatiality_strategy == SpatialityStrategy.SPATIAL:

        game_matrix = np.zeros([ph.population_length] * ph.num_dim + [ph.num_phenotypes])

        for i in range(ph.num_phenotypes - 1):
            idx = np.argwhere(np.sum(game_matrix, axis=-1) == 0)

            idx = idx[random.sample(range(0, idx.shape[0] - 1),
                                    int(ph.population_length ** ph.num_dim * ph.initial_probability[i])), :]

            game_matrix[idx[:, 0], idx[:, 1], idx[:, 2], i] = 1

        idx = np.argwhere(np.sum(game_matrix, axis=-1) == 0)

        game_matrix[idx[:, 0], idx[:, 1], idx[:, 2], -1] = 1

        return game_matrix




def get_game_matrix_from_file(ph: ParamHandler) -> np.ndarray:
    gm = np.load(ph.initial_matrix_path)
    return gm
