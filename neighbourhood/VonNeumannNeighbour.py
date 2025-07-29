import numpy as np

from neighbourhood.NeighbourController import NeighbourController
from utils.ParamHandler import ParamHandler


class VonNeumann(NeighbourController):

    def __init__(self, param_handler: ParamHandler):
        super().__init__(param_handler)


    def get_cell_neighbours_2d(self, x: int, y: int) -> np.ndarray:
        neighbours = np.array([[1, 0],
                               [-1, 0],
                               [0, 1],
                               [0, -1]])

        vector = np.array([x, y])
        neighbours = neighbours + vector

        neighbours[neighbours == -1] = self.param_handler.population_length - 1
        neighbours[neighbours == self.param_handler.population_length] = 0

        return neighbours


    def get_cell_neighbours_3d(self, x: int, y: int, z: int) -> np.ndarray:
        neighbours = np.array([[1,0,0],
                               [-1,0,0],
                               [0, 1, 0],
                               [0, -1, 0],
                               [0, 0, 1],
                               [0, 0, -1]])

        vector = np.array([x,y,z])
        neighbours = neighbours + vector

        neighbours[neighbours == -1] = self.param_handler.population_length - 1
        neighbours[neighbours == self.param_handler.population_length] = 0

        return neighbours
