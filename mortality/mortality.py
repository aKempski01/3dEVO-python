from typing import List
import numpy as np
from utils.enums import DeathStrategy

import config


def mortality(game_matrix: np.ndarray):
    if config.death_strategy == DeathStrategy.ASYNCH:
        idx = np.random.randint(0,config.pop_length, config.num_of_dims)
        return [idx]

    if config.death_strategy == DeathStrategy.SYNCH:
        idx = np.argwhere(game_matrix == game_matrix)
        return idx

    if config.death_strategy == DeathStrategy.SEMI_SYNCH:
        idx = np.random.randint(0,config.pop_length, (int(config.mortality_rate*config.pop_length*config.pop_length), config.num_of_dims))
        return idx


