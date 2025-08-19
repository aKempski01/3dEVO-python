from typing import List

import numpy as np

from mortality.MortalityController import MortalityController
from utils.ParamHandler import ParamHandler


class Asynch(MortalityController):

    def __init__(self, param_handler: ParamHandler) -> None:
        super().__init__(param_handler)

    def get_cells_to_update(self, game_matrix: np.ndarray) -> List[np.ndarray]:
        idx = np.random.randint(0, self.param_handler.population_length, self.param_handler.num_dim)
        return list([idx])
