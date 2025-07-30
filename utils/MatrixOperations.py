import numpy as np

from utils.Enums import SpatialityStrategy
from utils.ParamHandler import ParamHandler


def get_game_matrix(param_handler: ParamHandler) -> np.ndarray:
    if param_handler.num_dim == 2:
        return get_game_matrix_2d(param_handler)

    elif param_handler.num_dim == 3:
        return get_game_matrix_3d(param_handler)

    else:
        raise ValueError('Game matrix dimension must be 2 or 3')



def get_game_matrix_2d(ph: ParamHandler) -> np.ndarray:
    game_matrix = np.random.random([ph.population_length] * 2 + [ph.num_phenotypes])

    if ph.spatiality_strategy == SpatialityStrategy.MIXED:
        gm = np.sum(game_matrix, axis=-1)
        for i in range(ph.num_phenotypes):
            game_matrix[:, :, i] /= gm
        return game_matrix

    elif ph.spatiality_strategy == SpatialityStrategy.SPATIAL:
        idx = np.argmax(game_matrix, axis=-1)
        game_matrix[:, :, :] = 0

        for p in range(ph.num_phenotypes):
            game_matrix[:, :, p] = np.where(idx == p, 1, 0)

        return game_matrix

    else:
        raise ValueError('Unknown spatiality strategy: {}'.format(ph.spatiality_strategy))


def get_game_matrix_3d(ph: ParamHandler):
    game_matrix = np.random.random([ph.population_length] * ph.num_dim + [ph.num_phenotypes])
    # gm = np.sum(game_matrix, axis = -1)


    if ph.spatiality_strategy == SpatialityStrategy.MIXED:
        gm = np.sum(game_matrix, axis=-1)
        for i in range(ph.num_phenotypes):
            game_matrix[:, :, :, i] /= gm
        return game_matrix

    elif ph.spatiality_strategy == SpatialityStrategy.SPATIAL:
        idx = np.argmax(game_matrix, axis=-1)
        game_matrix[:, :, :, :] = 0

        for p in range(ph.num_phenotypes):
            game_matrix[:, :, :, p] = np.where(idx == p, 1, 0)

        return game_matrix
