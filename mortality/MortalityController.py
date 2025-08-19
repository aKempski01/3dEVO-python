from typing import List

import numpy as np

from abc import ABC, abstractmethod

from utils.ParamHandler import ParamHandler


class MortalityController(ABC):
    def __init__(self, param_handler: ParamHandler) -> None:
        self.param_handler = param_handler

    @abstractmethod
    def get_cells_to_update(self, game_matrix: np.ndarray) -> List[np.ndarray]:
        pass