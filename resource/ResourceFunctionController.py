from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Tuple

import numpy as np

from neighbourhood.NeighbourController import NeighbourController
from utils.ParamHandler import ParamHandler


class ResourceMode(Enum):
    TIME = 0
    LOCAL_AMOUNT = 1
    GLOBAL_AMOUNT = 2


class ResourceFunctionController(ABC):
    param_handler: ParamHandler

    function_value: float
    function_matrix: np.ndarray

    resource_mode: ResourceMode

    def __init__(self, param_handler: ParamHandler, neighbour_controller: NeighbourController):
        self.param_handler = param_handler
        self.neighbour_controller = neighbour_controller

        if not hasattr(self.param_handler, "resource_function_params"):
            raise AttributeError("configuration YAML file has no resource function params")

        if "mode" not in self.param_handler.resource_function_params.keys():
            raise AttributeError("configuration YAML file is lacking a 'mode' parameter")


        if self.param_handler.resource_function_params["mode"] == 'time':
            self.resource_mode = ResourceMode.TIME
        elif self.param_handler.resource_function_params["mode"] == 'local':
            self.resource_mode = ResourceMode.LOCAL_AMOUNT
        elif self.param_handler.resource_function_params["mode"] == 'global':
            self.resource_mode = ResourceMode.GLOBAL_AMOUNT
        else:
            raise AttributeError("configuration YAML file has a typo in a 'mode' parameter - available modes: 'time', 'local', 'global' ")



    def get_function_value(self, idx: Tuple[int, int] | Tuple[int, int, int]) -> float:
        if self.resource_mode == ResourceMode.LOCAL_AMOUNT:
            if self.param_handler.num_dim == 2:
                return float(self.function_matrix[idx[0], idx[1]])

            elif self.param_handler.num_dim == 3:
                return float(self.function_matrix[idx[0], idx[1], idx[2]])

        return self.function_value


    @abstractmethod
    def update_function_value(self, epoch_num: int, game_matrix: Optional[np.ndarray] = None) -> None:
        pass
