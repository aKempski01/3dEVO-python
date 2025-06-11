import numpy as np
from matplotlib import pyplot as plt

import config
from utils.enums import SpatialityStrategy, NeighborhoodType


def get_game_matrix():
    if config.num_of_dims == 2:
        return get_game_matrix_2d()

    elif config.num_of_dims == 3:
        return get_game_matrix_3d()





def get_game_matrix_2d():
    game_matrix = np.random.random([config.pop_length] * config.num_of_dims + [config.num_of_phenotypes])

    if config.spatiality_strategy == SpatialityStrategy.MIXED:
        gm = np.sum(game_matrix, axis=-1)
        for i in range(config.num_of_dims):
            game_matrix[:, :, i] /= gm
        return game_matrix

    elif config.spatiality_strategy == SpatialityStrategy.SPATIAL:
        idx = np.argmax(game_matrix, axis=-1)
        game_matrix[:, :, :] = 0

        game_matrix[:,:,0] = np.where(idx == 0, 1, 0)
        game_matrix[:,:,1] = np.where(idx == 1, 1, 0)
        game_matrix[:,:,2] = np.where(idx == 2, 1, 0)

        return game_matrix


def get_game_matrix_3d():
    game_matrix = np.random.random([config.pop_length] * config.num_of_dims + [config.num_of_phenotypes])
    gm = np.sum(game_matrix, axis = -1)

    game_matrix[:,:,:,0] /= gm
    game_matrix[:,:,:,1] /= gm

    if config.spatiality_strategy == SpatialityStrategy.MIXED:
        return game_matrix

    elif config.spatiality_strategy == SpatialityStrategy.SPATIAL:
        game_matrix = np.where(game_matrix > 0.5, 1, 0)
        return game_matrix




def get_cell_neighbours_2d(x: int, y: int):
    neighbours = []

    if x != 0:
        neighbours.append((x - 1, y))

    if y != 0:
        neighbours.append((x, y - 1))

    if x != config.pop_length - 1:
        neighbours.append((x + 1, y))

    if y != config.pop_length - 1:
        neighbours.append((x, y + 1))

    if config.neighborhood_type == NeighborhoodType.MOORE:
        if x != 0 and y != 0:
            neighbours.append((x-1, y-1))

        if x != 0 and y != config.pop_length-1:
            neighbours.append((x-1, y+1))

        if x != config.pop_length-1 and y != 0:
            neighbours.append((x+1, y-1))

        if x != config.pop_length-1 and y != config.pop_length-1:
            neighbours.append((x+1, y+1))

    return neighbours



def get_cell_neighbours_3d(x: int, y: int, z: int):
    neighbours = []

    if x != 0:
        neighbours.append((x - 1, y, z))

    if y != 0:
        neighbours.append((x, y - 1,z))

    if x != config.pop_length - 1:
        neighbours.append((x + 1, y,z))

    if y != config.pop_length - 1:
        neighbours.append((x, y + 1,z))

    if z != 0:
        neighbours.append((x, y, z-1))

    if z != config.pop_length - 1:
        neighbours.append((x, y, z+1))

    if config.neighborhood_type == NeighborhoodType.MOORE:

        if x != 0 and y != 0 and z != 0:
            neighbours.append((x-1, y-1, z-1))

        if x != 0 and y != 0 and z != config.pop_length-1:
            neighbours.append((x-1, y-1, z+1))

        if x != 0 and y != config.pop_length-1 and z != 0:
            neighbours.append((x-1, y+1, z-1))

        if x != 0 and y != config.pop_length-1 and z != config.pop_length-1:
            neighbours.append((x-1, y+1, z+1))

        if x != config.pop_length-1 and y != 0 and z != 0:
            neighbours.append((x+1, y-1, z-1))

        if x != config.pop_length-1 and y != 0 and z != config.pop_length-1:
            neighbours.append((x+1, y-1, z+1))

        if x != config.pop_length-1 and y != config.pop_length-1 and z != 0:
            neighbours.append((x+1, y+1, z-1))

        if x != config.pop_length - 1 and y != config.pop_length - 1 and z != config.pop_length-1:
            neighbours.append((x + 1, y + 1, z+1))

    return neighbours