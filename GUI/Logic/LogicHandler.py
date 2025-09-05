from typing import List, Optional
import glob
import yaml

import numpy as np

from utils.ParamHandler import ParamHandler
import os

class LogicHandler:

    experiment_list: List[str]

    param_handler: Optional[ParamHandler] = None
    chosen_exp: Optional[str] = None


    def __init__(self):
        self.refresh_exp()
        self.load_experiment(self.experiment_list[0])


    def refresh_exp(self):
        self.experiment_list = glob.glob("runs/*")
        self.experiment_list.sort(key=os.path.getmtime, reverse=True)


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


    def get_history_by_name(self, name: str):
        with open(name+ "/data.yaml", 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)


        history = np.zeros((data['num_epochs']+1, data['num_phenotypes']))

        for e in range(data['num_epochs']+1):
            arr = np.load(name + '/epoch_'+str(e)+'.npy')

            if self.param_handler.num_dim == 2:
                history[e, :] = [np.sum(arr[:, :, i]) for i in range(data['num_phenotypes'])]

            elif self.param_handler.num_dim == 3:
                history[e, :] = [np.sum(arr[:, :, :, i]) for i in range(data['num_phenotypes'])]


        history /= data['population_length'] ** data['num_dim']

        return history

    def get_phenotypes_by_name(self, name: str):
        names = []
        with open(name + "/data.yaml", 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
            for i in range(data['num_phenotypes']):
                names.append(data['phenotype_names'][i])

        return names


    def get_yaml_by_name(self, name: str):
        with open(name+ "/data.yaml", 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
        return data

    def check_compatibility(self, name: str, num_dim: int, problem_name: str, num_epochs: int, population_length: int):
        with open(name+ "/data.yaml", 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)

        if data['population_length'] != population_length or data['num_dim'] != num_dim or data['num_epochs'] != num_epochs or data['problem_name'] != problem_name:
            return False

        return True
