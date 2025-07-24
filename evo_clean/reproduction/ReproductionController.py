from abc import ABC, abstractmethod

import numpy as np

from evo_clean.neighbourhood.NeighbourController import NeighbourController
from evo_clean.utils.ParamHandler import ParamHandler


class ReproductionController(ABC):
    param_handler: ParamHandler
    neighbour_controller: NeighbourController

    def __init__(self, param_handler: ParamHandler, neighbour_controller: NeighbourController):
        self.param_handler = param_handler
        self.neighbour_controller = neighbour_controller


    @abstractmethod
    def reproduce(self, game_matrix: np.ndarray, pay_off_matrix: np.ndarray, indices: np.ndarray):
        pass

