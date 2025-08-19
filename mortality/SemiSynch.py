from typing import List

import numpy as np

from mortality.MortalityController import MortalityController
from utils.ParamHandler import ParamHandler


class SemiSynch(MortalityController):

    def __init__(self, param_handler: ParamHandler) -> None:
        super().__init__(param_handler)

    def get_cells_to_update_old(self, game_matrix: np.ndarray) -> np.ndarray:
        idx = np.random.randint(0, self.param_handler.population_length, (int(self.param_handler.mortality_rate * self.param_handler.population_length * self.param_handler.population_length), self.param_handler.num_dim))
        return idx

    def get_cells_to_update(self, game_matrix: np.ndarray) -> List[np.ndarray]:
        gm = np.random.random([self.param_handler.population_length] * self.param_handler.num_dim)
        idx = np.argwhere(gm < self.param_handler.mortality_rate)
        # idx = np.random.randint(0, self.param_handler.population_length, (int(self.param_handler.mortality_rate * self.param_handler.population_length * self.param_handler.population_length), self.param_handler.num_dim))
        return list(idx)
