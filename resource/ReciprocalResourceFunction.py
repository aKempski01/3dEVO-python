from typing import Optional, List

from poetry.console.commands import self

from neighbourhood.NeighbourController import NeighbourController
from resource.ResourceFunctionController import ResourceFunctionController, ResourceMode
from utils.ParamHandler import ParamHandler

import numpy as np


class ReciprocalResourceFunction(ResourceFunctionController):
    phenotype_to_select: int
    a_param: float
    h_param: float
    k_param: float

    def __init__(self, param_handler: ParamHandler, neighbour_controller: NeighbourController):
        super().__init__(param_handler, neighbour_controller)

        if 'a_param' not in self.param_handler.resource_function_params.keys() or 'h_param' not in self.param_handler.resource_function_params.keys() or 'k_param' not in self.param_handler.resource_function_params.keys():
            raise AttributeError("configuration YAML file has incorrect parameters")

        if self.resource_mode != ResourceMode.TIME and 'phenotype_to_select' not in self.param_handler.resource_function_params.keys():
            raise AttributeError("configuration YAML file has incorrect parameters")


        self.phenotype_to_select = self.param_handler.resource_function_params['phenotype_to_select']
        self.a_param = self.param_handler.resource_function_params['a_param']
        self.k_param = self.param_handler.resource_function_params['k_param']
        self.h_param = self.param_handler.resource_function_params['h_param']


    def update_function_value(self, epoch_num: int, game_matrix: Optional[np.ndarray] = None, indices: Optional[List[np.ndarray]] = None) -> None:
        if game_matrix is None:
            raise AttributeError("game_matrix parameter is not provided")


        if self.resource_mode == ResourceMode.LOCAL_AMOUNT:
            self.__local_update(game_matrix, indices)

        elif self.resource_mode == ResourceMode.GLOBAL_AMOUNT:
            self.__global_update(game_matrix)

        elif self.resource_mode == ResourceMode.TIME:
            self.__time_update(epoch_num)

        else:
            raise AttributeError("resource_mode parameter is not supported")


    def __global_update(self, game_matrix: np.ndarray):
        if self.param_handler.num_dim == 2:
            H = np.sum(game_matrix[:, :, self.phenotype_to_select])
        elif self.param_handler.num_dim == 3:
            H = np.sum(game_matrix[:, :, :, self.phenotype_to_select])
        else:
            raise AttributeError("num_dim parameter is not supported")

        self.function_value = self.k_param + self.a_param / (H - self.h_param)



    def __local_update(self, game_matrix: np.ndarray, indices: List[np.ndarray]):
        mat = np.zeros([self.param_handler.population_length] * self.param_handler.num_dim, dtype=np.float32)

        if self.param_handler.num_dim == 2:
            for xy in indices:
                neighbours = self.neighbour_controller.get_cell_neighbours_2d(xy[0], xy[1])
                for n in neighbours:
                    mat[xy[0], xy[1]] += game_matrix[n[0], n[1], self.phenotype_to_select]


        elif self.param_handler.num_dim == 3:
            for xyz in indices:
                neighbours = self.neighbour_controller.get_cell_neighbours_3d(xyz[0], xyz[1], xyz[2])
                for n in neighbours:
                    mat[xyz[0], xyz[1], xyz[2]] += game_matrix[n[0], n[1], n[2], self.phenotype_to_select]

        else:
            raise AttributeError("num_dim parameter is not supported")

        self.function_matrix = mat - self.h_param
        self.function_matrix = self.a_param / self.function_matrix
        self.function_matrix += self.k_param

    def __time_update(self, epoch_num: int):
        self.function_value = self.k_param + self.a_param / (epoch_num - self.h_param)
