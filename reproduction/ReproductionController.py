from abc import ABC, abstractmethod
from typing import List

import numpy as np

from neighbourhood.NeighbourController import NeighbourController
from utils.ParamHandler import ParamHandler


class ReproductionController(ABC):
    param_handler: ParamHandler
    neighbour_controller: NeighbourController

    def __init__(self, param_handler: ParamHandler, neighbour_controller: NeighbourController):
        self.param_handler = param_handler
        self.neighbour_controller = neighbour_controller


    @abstractmethod
    def reproduce(self, game_matrix: np.ndarray, pay_off_matrix: np.ndarray, indices: List[np.ndarray]):
        pass

