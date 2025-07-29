import numpy as np

from mortality.MortalityController import MortalityController
from utils.ParamHandler import ParamHandler


class Synch(MortalityController):

    def __init__(self, param_handler: ParamHandler) -> None:
        super().__init__(param_handler)

    def get_cells_to_update(self, game_matrix: np.ndarray) -> np.ndarray:
        idx = np.unique(np.argwhere(game_matrix == game_matrix)[:, :self.param_handler.num_dim], axis=0)
        return idx
