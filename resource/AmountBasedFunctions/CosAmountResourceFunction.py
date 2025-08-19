from typing import Optional

from poetry.console.commands import self

from neighbourhood.NeighbourController import NeighbourController
from resource.ResourceFunctionController import ResourceFunctionController, ResourceMode
from utils.ParamHandler import ParamHandler

import numpy as np


class CosAmountResourceFunction(ResourceFunctionController):
    phenotype_to_select: int

    def __init__(self, param_handler: ParamHandler, neighbour_controller: NeighbourController):
        super().__init__(param_handler, neighbour_controller)

        if self.resource_mode == ResourceMode.TIME:
            raise AttributeError("Time mode is not supported for the following resource cost function.")

        if 'phenotype_to_select' not in self.param_handler.resource_function_params.keys():
            raise AttributeError("configuration YAML file has incorrect parameters")

        self.phenotype_to_select = self.param_handler.resource_function_params['phenotype_to_select']



    def update_function_value(self, epoch_num: int, game_matrix: Optional[np.ndarray] = None):
        if game_matrix is None:
            raise AttributeError("game_matrix parameter is not provided")

        if self.resource_mode == ResourceMode.GLOBAL_AMOUNT:

            if self.param_handler.num_dim == 2:
                H = np.sum(game_matrix[:, :, self.phenotype_to_select])
            elif self.param_handler.num_dim == 3:
                H = np.sum(game_matrix[:, :, :, self.phenotype_to_select])
            else:
                raise AttributeError("num_dim parameter is not supported")

            self.function_value = np.cos(H * np.pi / 2)

        if self.resource_mode == ResourceMode.LOCAL_AMOUNT:
            self.__local_update(game_matrix)

        elif self.resource_mode == ResourceMode.GLOBAL_AMOUNT:
            self.__global_update(game_matrix)

        else:
            raise AttributeError("resource_mode parameter is not supported")


    def __global_update(self, game_matrix: np.ndarray):
        if self.param_handler.num_dim == 2:
            H = np.sum(game_matrix[:, :, self.phenotype_to_select])
        elif self.param_handler.num_dim == 3:
            H = np.sum(game_matrix[:, :, :, self.phenotype_to_select])
        else:
            raise AttributeError("num_dim parameter is not supported")

        self.function_value = np.cos(H * np.pi / 2)



    def __local_update(self, game_matrix: np.ndarray):
        mat = np.zeros([self.param_handler.population_length] * self.param_handler.num_dim, dtype=np.float32)

        if self.param_handler.num_dim == 2:
            for x in range(self.param_handler.population_length):
                for y in range(self.param_handler.population_length):
                    neighbours = self.neighbour_controller.get_cell_neighbours_2d(x, y)
                    for n in neighbours:
                        mat[x, y] += game_matrix[n[0], n[1], self.phenotype_to_select]

        elif self.param_handler.num_dim == 3:
            for x in range(self.param_handler.population_length):
                for y in range(self.param_handler.population_length):
                    for z in range(self.param_handler.population_length):
                        neighbours = self.neighbour_controller.get_cell_neighbours_3d(x, y, z)
                        for n in neighbours:
                            mat[x, y, z] += game_matrix[n[0], n[1], n[2], self.phenotype_to_select]

        else:
            raise AttributeError("num_dim parameter is not supported")

        self.function_matrix = np.cos(mat * np.pi * 0.5)
