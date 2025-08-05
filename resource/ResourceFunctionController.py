from abc import ABC, abstractmethod

from utils.ParamHandler import ParamHandler


class ResourceFunctionController(ABC):
    param_handler: ParamHandler

    function_value: float

    def __init__(self, param_handler: ParamHandler):
        self.param_handler = param_handler

    def get_function_value(self):
        return self.function_value

    @abstractmethod
    def update_function_value(self, epoch_num: int):
        pass
