import numpy as np
import config
from matplotlib import pyplot as plt
from fitness.fitness import fitness_fun
from utils.matrix_operations import get_game_matrix
from mortality.mortality import mortality
from reproduction.reproduction import reproduction
import tqdm

def main():
    if not config.validate_config():
        return

    game_matrix = get_game_matrix()
    h = [np.sum(game_matrix[:,:,0])/(config.pop_length**config.num_of_dims)]

    for e in tqdm.tqdm(range(config.max_iterations)):
        pay_off_matrix = fitness_fun(game_matrix)
        indices = mortality(game_matrix)
        game_matrix = reproduction(game_matrix, pay_off_matrix, indices)
        h.append(np.sum(game_matrix[:,:,0])/(config.pop_length**config.num_of_dims))
        # return
        # h.append(np.sum(pay_off_matrix))


    plt.plot(h)
    plt.show()



if __name__ == '__main__':
    main()




# todo:
# dodać thread poola
# dodać jakąś formę graficzną tego

