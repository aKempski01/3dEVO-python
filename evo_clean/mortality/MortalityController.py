import numpy as np

from abc import ABC, abstractmethod

from evo_clean.utils.ParamHandler import ParamHandler


class MortalityController(ABC):
    def __init__(self, param_handler: ParamHandler) -> None:
        self.param_handler = param_handler

    @abstractmethod
    def get_cells_to_update(self, game_matrix: np.ndarray) -> np.ndarray:
        pass