from typing import Optional, List

from poetry.console.commands import self

from neighbourhood.NeighbourController import NeighbourController
from resource.ResourceFunctionController import ResourceFunctionController, ResourceMode
from utils.ParamHandler import ParamHandler

import numpy as np


class CosResourceFunction(ResourceFunctionController):
    ph1: int

    def __init__(self, param_handler: ParamHandler, neighbour_controller: NeighbourController):
        super().__init__(param_handler, neighbour_controller)

        if self.resource_mode == ResourceMode.TIME:
            raise AttributeError("Time mode is not supported for the following resource cost function.")


    def update_phenotype_idx(self):
        if self.resource_mode != ResourceMode.TIME:
            if 'ph1' not in self.param_handler.resource_function_params['resource_phenotypes'].keys():
                raise AttributeError("The ph1 phenotype name is missing. Please fill it inside the resource phenotypes field.")

            else:
                self.ph1 = self.param_handler.resource_function_params['resource_phenotypes']['ph1']


    def update_function_value(self, epoch_num: int, game_matrix: Optional[np.ndarray] = None, indices: Optional[List[np.ndarray]] = None) -> None:
        if game_matrix is None:
            raise AttributeError("game_matrix parameter is not provided")

        if self.resource_mode == ResourceMode.LOCAL_AMOUNT:
            self.__local_update(game_matrix, indices)

        elif self.resource_mode == ResourceMode.GLOBAL_AMOUNT:
            self.__global_update(game_matrix)

        else:
            raise AttributeError("resource_mode parameter is not supported")


    def __global_update(self, game_matrix: np.ndarray):
        if self.param_handler.num_dim == 2:
            H = np.sum(game_matrix[:, :, self.ph1])
        elif self.param_handler.num_dim == 3:
            H = np.sum(game_matrix[:, :, :, self.ph1])
        else:
            raise AttributeError("num_dim parameter is not supported")

        self.function_value = np.cos(H * np.pi / 2)



    def __local_update(self, game_matrix: np.ndarray, indices: List[np.ndarray]):
        mat = np.zeros([self.param_handler.population_length] * self.param_handler.num_dim, dtype=np.float32)

        if self.param_handler.num_dim == 2:
            for xy in indices:
                neighbours = self.neighbour_controller.get_cell_neighbours_2d(xy[0], xy[1])
                for n in neighbours:
                    mat[xy[0], xy[1]] += game_matrix[n[0], n[1], self.ph1]


        elif self.param_handler.num_dim == 3:
            for xyz in indices:
                neighbours = self.neighbour_controller.get_cell_neighbours_3d(xyz[0], xyz[1], xyz[2])
                for n in neighbours:
                    mat[xyz[0], xyz[1], xyz[2]] += game_matrix[n[0], n[1], n[2], self.ph1]

        else:
            raise AttributeError("num_dim parameter is not supported")

        self.function_matrix = np.cos(mat * np.pi * 0.5)
