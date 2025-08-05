from resource.ResourceFunctionController import ResourceFunctionController
from utils.ParamHandler import ParamHandler


class StepResourceFunction(ResourceFunctionController):

    step_inc: float
    step_epoch: int

    def __init__(self, param_handler: ParamHandler):
        super().__init__(param_handler)

        if not hasattr(self.param_handler, "resource_function_params"):
            raise AttributeError("configuration YAML file has no resource function params")

        if 'step_initial_value' not in self.param_handler.resource_function_params.keys() or 'step_inc' not in self.param_handler.resource_function_params.keys() or 'step_epoch' not in self.param_handler.resource_function_params.keys():
            raise AttributeError("configuration YAML file has incorrect parameters")

        self.function_value = self.param_handler.resource_function_params['step_initial_value']
        self.step_inc = self.param_handler.resource_function_params['step_inc']
        self.step_epoch = self.param_handler.resource_function_params['step_epoch']



    def update_function_value(self, epoch_num: int):
        if (epoch_num + 1) % self.step_epoch == 0:
            self.function_value += self.step_inc

