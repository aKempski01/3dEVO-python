from abc import ABC, abstractmethod
from multiprocessing import Pool
from typing import List, Dict, Optional, Tuple

import numpy as np

from neighbourhood.NeighbourController import NeighbourController
from resource.ResourceFunctionController import ResourceFunctionController
from utils.ParamHandler import ParamHandler


class ProblemController(ABC):
    num_phenotypes: int
    supported_num_dims: List[int]

    param_handler: ParamHandler
    neighbour_controller: NeighbourController
    resource_function: Optional[ResourceFunctionController]
    phenotype_names: Dict[int, str]


    def __init__(self, param_handler: ParamHandler, neighbour_controller: NeighbourController, resource_function_controller: Optional[ResourceFunctionController]):
        if param_handler.problem_params is not None:
            for key, value in param_handler.problem_params.items():
                setattr(self, key, value)

        self.param_handler = param_handler
        self.neighbour_controller = neighbour_controller
        self.resource_function = resource_function_controller


    @abstractmethod
    def fitness_problem(self, player: int, enemy: int, idx: Optional[Tuple[int, int] | Tuple[int, int, int]] = None) -> float:
        pass


    def get_phenotype_names_to_idx(self):
        return self.phenotype_names


    def fitness_function(self, game_matrix, indices):
        if self.param_handler.num_dim not in self.supported_num_dims:
            raise ValueError("Number of dimensions not supported.")

        if self.param_handler.num_dim == 2:
            idx = self.explode_indices_2d(indices)
            return self.fitness_2d(game_matrix, idx)

        elif self.param_handler.num_dim == 3:
            idx = self.explode_indices_3d(indices)
            return self.fitness_3d(game_matrix)

        else:
            raise ValueError("Number of dimensions not supported.")



    def fitness_2d(self, game_matrix: np.ndarray, indices):
        if self.param_handler.parallel:
            with Pool(processes=self.param_handler.num_cpu) as pool:
                async_results = [pool.apply_async(self.par_2d, args=(game_matrix, i)) for i in range(self.param_handler.population_length)]
                results = [ar.get() for ar in async_results]
            return np.array(results)

        else:
            fit_array = np.zeros([self.param_handler.population_length] * self.param_handler.num_dim)
            for xy in indices:
                neighbours = self.neighbour_controller.get_cell_neighbours_2d(xy[0], xy[1])

                for i in range(self.param_handler.num_phenotypes):
                    for j in range(self.param_handler.num_phenotypes):
                        f = self.fitness_problem(i, j, (xy[0], xy[1])) * game_matrix[xy[0], xy[1], i].copy()

                        for n in neighbours:
                            fit_array[xy[0]][xy[1]] += f * game_matrix[n[0], n[1], j].copy()

            return fit_array


    def par_2d(self, game_matrix, idx: int):
        fit_array = np.zeros(self.param_handler.population_length)
        for y in range(self.param_handler.population_length):
            neighbours = self.neighbour_controller.get_cell_neighbours_2d(idx, y)
            for i in range(self.param_handler.num_phenotypes):
                for j in range(self.param_handler.num_phenotypes):
                    f = self.fitness_problem(i, j, (idx, y)) * game_matrix[idx, y, i].copy()
                    if f != 0:
                        for n in neighbours:
                            fit_array[y] += f * game_matrix[n[0], n[1], j].copy()

        return fit_array






    def fitness_3d(self, game_matrix: np.ndarray):
        if self.param_handler.parallel:
            with Pool(processes=self.param_handler.num_cpu) as pool:
                async_results = [pool.apply_async(self.par_3d, args=(game_matrix, i)) for i in range(self.param_handler.population_length)]
                results = [ar.get() for ar in async_results]
            return np.array(results)

        else:
            fit_array = np.zeros([self.param_handler.population_length] * self.param_handler.num_dim)
            for x in range(self.param_handler.population_length):
                for y in range(self.param_handler.population_length):
                    for z in range(self.param_handler.population_length):
                        neighbours = self.neighbour_controller.get_cell_neighbours_3d(x, y, z)

                        for i in range(self.param_handler.num_phenotypes):
                            for j in range(self.param_handler.num_phenotypes):
                                f = self.fitness_problem(i, j, (x, y, z)) * game_matrix[x, y, z, i].copy()
                                if f != 0:
                                    for n in neighbours:
                                        fit_array[x][y][z] += f * game_matrix[n[0], n[1], n[2], j].copy()

            return fit_array


    def par_3d(self, game_matrix, idx: int):
        fit_array = np.zeros([self.param_handler.population_length] * (self.param_handler.num_dim - 1))
        for y in range(self.param_handler.population_length):
            for z in range(self.param_handler.population_length):
                neighbours = self.neighbour_controller.get_cell_neighbours_3d(idx, y, z)
                for i in range(self.param_handler.num_phenotypes):
                    for j in range(self.param_handler.num_phenotypes):
                        f = self.fitness_problem(i, j, (idx, y, z)) * game_matrix[idx, y, z, i].copy()
                        if f != 0:
                            for n in neighbours:
                                fit_array[y][z] += f * game_matrix[n[0], n[1], n[2], j].copy()

        return fit_array



    def explode_indices_2d(self, indices: List[Tuple[int, int]]) -> List[np.ndarray[int, int]]:
        idx = indices.copy()
        for i in idx:
            n = self.neighbour_controller.get_cell_neighbours_2d(i[0], i[1])
            indices.extend(n)

        indices = list(np.unique(np.array(indices), axis=0))

        # indices = list(set(indices))
        return indices

    def explode_indices_3d(self, indices: List[Tuple[int, int]]) -> List[np.ndarray[int, int]]:
        idx = indices.copy()
        for i in idx:
            n = self.neighbour_controller.get_cell_neighbours_3d(i[0], i[1], i[2])
            indices.extend(n)

        indices = list(np.unique(np.array(indices), axis=0))

        return indices
