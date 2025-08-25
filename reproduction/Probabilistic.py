from random import random

import numpy as np

from neighbourhood.NeighbourController import NeighbourController
from reproduction.ReproductionController import ReproductionController
from utils.ParamHandler import ParamHandler


class Probabilistic(ReproductionController):

    def __init__(self, param_handler: ParamHandler, neighbour_controller: NeighbourController):
        super().__init__(param_handler, neighbour_controller)

    def reproduce(self, game_matrix: np.ndarray, pay_off_matrix: np.ndarray, indices: np.ndarray):
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
            for n in neighbours:
                fit_list.append(pay_off_matrix[n[0], n[1]])

            fit_list = np.array(fit_list)
            fit_list /= np.sum(fit_list)

            p_value = random()

            best_arg = -1

            for i in range(len(fit_list)):
                p_value -= fit_list[i]
                if p_value < 0:
                    best_arg = i
                    break

            best_n = neighbours[best_arg]
            _gm[idx[0], idx[1]] = game_matrix[best_n[0], best_n[1]].copy()

        return _gm

    def __reproduction_3d(self, game_matrix: np.ndarray, pay_off_matrix: np.ndarray, indices: np.ndarray):
        _gm = game_matrix.copy()
        for idx in indices:
            neighbours = self.neighbour_controller.get_cell_neighbours_3d(idx[0], idx[1], idx[2])
            fit_list = []
            for n in neighbours:
                fit_list.append(pay_off_matrix[n[0], n[1], n[2]])

            fit_list = np.array(fit_list)
            fit_list /= np.sum(fit_list)

            p_value = random()

            best_arg = -1

            for i in range(len(fit_list)):
                p_value -= fit_list[i]
                if p_value < 0:
                    best_arg = i
                    break

            best_n = neighbours[best_arg]
            _gm[idx[0], idx[1], idx[2]] = game_matrix[best_n[0], best_n[1], best_n[2]].copy()

        return _gm

