from abc import ABC, abstractmethod

from utils.ParamHandler import ParamHandler


class NeighbourController(ABC):
    param_handler: ParamHandler

    def __init__(self, param_handler: ParamHandler) -> None:
        self.param_handler = param_handler
        pass


    @abstractmethod
    def get_cell_neighbours_2d(self, x: int, y: int):
        pass

    @abstractmethod
    def get_cell_neighbours_3d(self, x: int, y: int, z: int):
        pass


    @abstractmethod
    def get_max_num_neighbours(self) -> int:
        pass
