from typing import Optional, List

import numpy as np

from neighbourhood.NeighbourController import NeighbourController
from resource.ResourceFunctionController import ResourceFunctionController, ResourceMode
from utils.ParamHandler import ParamHandler


class SingleStepResourceFunction(ResourceFunctionController):

    step_inc: float
    step_epoch: int

    def __init__(self, param_handler: ParamHandler, neighbour_controller: NeighbourController):
        super().__init__(param_handler, neighbour_controller)

        if not hasattr(self.param_handler, "resource_function_params"):
            raise AttributeError("configuration YAML file has no resource function params")

        if self.resource_mode != ResourceMode.TIME:
            raise AttributeError("Only Time mode is supported for the following resource cost function.")

        if 'step_initial_value' not in self.param_handler.resource_function_params.keys() or 'step_inc' not in self.param_handler.resource_function_params.keys() or 'step_epoch' not in self.param_handler.resource_function_params.keys():
            raise AttributeError("configuration YAML file has incorrect parameters")

        self.function_value = self.param_handler.resource_function_params['step_initial_value']
        self.step_inc = self.param_handler.resource_function_params['step_inc']
        self.step_epoch = self.param_handler.resource_function_params['step_epoch']



    def update_function_value(self, epoch_num: int, game_matrix: Optional[np.ndarray] = None, indices: Optional[List[np.ndarray]] = None):
        if (epoch_num + 1) == self.step_epoch:
            self.function_value = self.step_inc

    def update_phenotype_idx(self) -> None:
        pass