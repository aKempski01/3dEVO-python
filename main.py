import numpy as np
import config
from matplotlib import pyplot as plt
from fitness.fitness import fitness_fun
from utils.matrix_operations import get_game_matrix
from mortality.mortality import mortality
from reproduction.reproduction import reproduction
import tqdm
import time

from GUI.main_window import Mainwindow

def main():
    if not config.validate_config():
        return

    game_matrix = get_game_matrix()
    history = {"gm": [game_matrix], "fitness": []}


    for e in tqdm.tqdm(range(config.max_iterations)):
        pay_off_matrix = fitness_fun(game_matrix)

        history['fitness'].append(np.sum(pay_off_matrix))

        indices = mortality(game_matrix)
        game_matrix = reproduction(game_matrix, pay_off_matrix, indices)

        history['gm'].append(game_matrix)


    history['fitness'].append(np.sum(pay_off_matrix))

    mw = Mainwindow()
    mw.display_output_matrix(history['gm'])

if __name__ == '__main__':
    main()

