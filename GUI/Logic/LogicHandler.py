from typing import List, Optional
import glob

import numpy as np

from utils.ParamHandler import ParamHandler


class LogicHandler:

    experiment_list: List[str]

    param_handler: Optional[ParamHandler] = None
    chosen_exp: Optional[str] = None


    def __init__(self):
        self.refresh_exp()
        self.load_experiment(self.experiment_list[0])


    def refresh_exp(self):
        self.experiment_list = glob.glob("runs/*")


    def load_experiment(self, name: str):
        self.chosen_exp = name
        self.param_handler = ParamHandler(self.chosen_exp+"/data.yaml")

    def get_array(self, epoch_num: int):
        return np.load(self.chosen_exp + '/epoch_'+str(epoch_num)+".npy")


    def get_history(self):
        history = np.zeros((self.param_handler.num_epochs+1, self.param_handler.num_phenotypes))

        for e in range(self.param_handler.num_epochs+1):
            arr = np.load(self.chosen_exp + '/epoch_'+str(e)+'.npy')

            if self.param_handler.num_dim == 2:
                history[e, :] = [np.sum(arr[:, :, i]) for i in range(self.param_handler.num_phenotypes)]

            elif self.param_handler.num_dim == 3:
                history[e, :] = [np.sum(arr[:, :, :, i]) for i in range(self.param_handler.num_phenotypes)]


        history /= self.param_handler.population_length**self.param_handler.num_dim

        return history

