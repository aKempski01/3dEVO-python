import numpy as np
import config
from reproduction.deterministic_reproduction import det_reproduction
from reproduction.prob_reproduction import prob_reproduction
from reproduction.weighted_reproduction import weighted_reproduction
from utils.enums import ReproductionStrategy


def reproduction(game_matrix: np.ndarray, pay_off_matrix: np.ndarray, indices):
    if config.reproduction_strategy == ReproductionStrategy.DETERMINISTIC:
        return det_reproduction(game_matrix, pay_off_matrix, indices)


    elif config.reproduction_strategy == ReproductionStrategy.PROBABILISTIC:
        return prob_reproduction(game_matrix, pay_off_matrix, indices)
    

    elif config.reproduction_strategy == ReproductionStrategy.WEIGHTED:
        return weighted_reproduction(game_matrix, pay_off_matrix, indices)





