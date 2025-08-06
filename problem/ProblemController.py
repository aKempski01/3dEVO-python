from abc import ABC, abstractmethod
from multiprocessing import Pool
from typing import List, Dict, Optional

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
    def fitness_problem(self, player: int, enemy: int) -> float:
        pass


    def fitness_function(self, game_matrix):
        if self.param_handler.num_dim not in self.supported_num_dims:
            raise ValueError("Number of dimensions not supported.")

        if self.param_handler.num_dim == 2:
            return self.fitness_2d(game_matrix)

        elif self.param_handler.num_dim == 3:
            return self.fitness_3d(game_matrix)

        else:
            raise ValueError("Number of dimensions not supported.")



    def fitness_2d(self, game_matrix: np.ndarray):
        if self.param_handler.parallel:
            with Pool(processes=self.param_handler.num_cpu) as pool:
                async_results = [pool.apply_async(self.par_2d, args=(game_matrix, i)) for i in range(self.param_handler.population_length)]
                results = [ar.get() for ar in async_results]
            return np.array(results)

        else:
            fit_array = np.zeros([self.param_handler.population_length] * self.param_handler.num_dim)
            for x in range(self.param_handler.population_length):
                for y in range(self.param_handler.population_length):
                    neighbours = self.neighbour_controller.get_cell_neighbours_2d(x, y)

                    for i in range(self.param_handler.num_phenotypes):
                        for j in range(self.param_handler.num_phenotypes):
                            f = self.fitness_problem(i, j) * game_matrix[x, y, i].copy()

                            for n in neighbours:
                                fit_array[x][y] += f * game_matrix[n[0], n[1], j].copy()

            return fit_array


    def par_2d(self, game_matrix, idx: int):
        fit_array = np.zeros([self.param_handler.population_length] * (self.param_handler.num_dim - 1))
        for x in range(self.param_handler.population_length):
            neighbours = self.neighbour_controller.get_cell_neighbours_2d(x, idx)
            for i in range(self.param_handler.num_phenotypes):
                for j in range(self.param_handler.num_phenotypes):
                    # todo
                    # sprawdzić czy tu cos się nie psuje
                    f = self.fitness_problem(i, j) * game_matrix[x, idx, i].copy()
                    if f != 0:
                        for n in neighbours:
                            fit_array[x] += f * game_matrix[n[0], n[1], j].copy()

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
                                f = self.fitness_problem(i, j) * game_matrix[x, y, z, i].copy()
                                if f != 0:
                                    for n in neighbours:
                                        fit_array[x][y][z] += f * game_matrix[n[0], n[1], j].copy()

            return fit_array


    def par_3d(self, game_matrix, idx: int):
        fit_array = np.zeros([self.param_handler.population_length] * (self.param_handler.num_dim - 1))
        for x in range(self.param_handler.population_length):
            for y in range(self.param_handler.population_length):
                neighbours = self.neighbour_controller.get_cell_neighbours_3d(x, y, idx)
                for i in range(self.param_handler.num_phenotypes):
                    for j in range(self.param_handler.num_phenotypes):
                        f = self.fitness_problem(i, j) * game_matrix[x, y, idx, i].copy()
                        if f != 0:
                            for n in neighbours:
                                fit_array[x][y] += f * game_matrix[n[0], n[1], n[2], j].copy()

        return fit_array


