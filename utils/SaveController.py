import glob
import os
import yaml

import numpy as np

from utils.ParamHandler import ParamHandler


class SaveController:

    __save_dir: str
    __param_handler: ParamHandler


    def __init__(self, param_handler: ParamHandler) -> None:
        self.__param_handler = param_handler

        if not os.path.exists("runs"):
            os.mkdir("runs")

        dirs = glob.glob("runs/" + param_handler.experiment_name + "*")


        self.__save_dir = "runs/" + param_handler.experiment_name + "_" + str(len(dirs))
        os.mkdir(self.__save_dir)

    def save_yaml_file(self) -> None:

        with open(self.__save_dir+'/data.yaml', 'w') as file:
            yaml.dump(self.__param_handler.__dict__, file)

    def save_game_matrix(self, game_matrix: np.ndarray, epoch_num: int) -> None:
        np.save(self.__save_dir + '/epoch_'+str(epoch_num)+".npy", game_matrix, allow_pickle=True)


    def load_game_matrix(self, epoch_num: int) -> np.ndarray:
        gm = np.load(self.__save_dir + '/epoch_'+str(epoch_num)+".npy")
        return gm


