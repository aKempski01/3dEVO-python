import numpy as np

from neighbourhood.NeighbourController import NeighbourController
from reproduction.ReproductionController import ReproductionController
from utils.Enums import SpatialityStrategy
from utils.ParamHandler import ParamHandler


class Weighted(ReproductionController):

    def __init__(self, param_handler: ParamHandler, neighbour_controller: NeighbourController):
        super().__init__(param_handler, neighbour_controller)
        if param_handler.spatiality_strategy != SpatialityStrategy.MIXED:
            raise ValueError("Weighted reproduction only supports MIXED spatial strategy.")

    def reproduce(self, game_matrix: np.ndarray, pay_off_matrix: np.ndarray, indices: np.ndarray) -> np.ndarray:
        if self.param_handler.num_dim == 2:
            return self.__reproduction_2d(game_matrix, pay_off_matrix, indices)
        elif self.param_handler.num_dim == 3:
            return self.__reproduction_3d(game_matrix, pay_off_matrix, indices)
        else:
            raise ValueError("Incorrect number of dimensions")



    def __reproduction_2d(self, game_matrix: np.ndarray, pay_off_matrix: np.ndarray, indices: np.ndarray):
        _gm = game_matrix.copy()
        for idx in indices:
            neighbours = self.neighbour_controller.get_cell_neighbours_2d(idx[0], idx[1])
            fit_list = []
            neighbours = list(neighbours)
            for n in neighbours:
                fit_list.append(pay_off_matrix[n[0], n[1]])

            if len(fit_list) > self.param_handler.num_cells_for_mean:
                for r in range(len(fit_list) - self.param_handler.num_cells_for_mean):
                    to_remove = np.argmin(fit_list)
                    fit_list.pop(to_remove)
                    neighbours.pop(to_remove)

            neighbours = np.array(neighbours)
            new_val = np.zeros(self.param_handler.num_phenotypes)
            for i in range(len(neighbours)):
                new_val += game_matrix[neighbours[i][0], neighbours[i][1], :] * fit_list[i]

            new_val /= np.sum(new_val)
            _gm[idx[0], idx[1], :] = new_val.copy()
        return _gm


    def __reproduction_3d(self, game_matrix: np.ndarray, pay_off_matrix: np.ndarray, indices: np.ndarray):
        _gm = game_matrix.copy()
        for idx in indices:
            neighbours = self.neighbour_controller.get_cell_neighbours_3d(idx[0], idx[1], idx[2])
            fit_list = []
            neighbours = list(neighbours)
            for n in neighbours:
                fit_list.append(pay_off_matrix[n[0], n[1], n[2]])

            if len(fit_list) > self.param_handler.num_cells_for_mean:
                for r in range(len(fit_list) - self.param_handler.num_cells_for_mean):
                    to_remove = np.argmin(fit_list)
                    fit_list.pop(to_remove)
                    neighbours.pop(to_remove)

            neighbours = np.array(neighbours)
            new_val = np.zeros(self.param_handler.num_phenotypes)
            for i in range(len(neighbours)):
                new_val += game_matrix[neighbours[i, 0], neighbours[i, 1], neighbours[i, 2], :] * fit_list[i]

            new_val /= np.sum(new_val)
            _gm[idx[0], idx[1], idx[2], :] = new_val.copy()
        return _gm

