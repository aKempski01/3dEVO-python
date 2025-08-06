from typing import List, Dict, Optional

from neighbourhood.NeighbourController import NeighbourController
from problem.ProblemController import ProblemController
from resource.ResourceFunctionController import ResourceFunctionController
from utils.ParamHandler import ParamHandler


class HawkDoveDynamicProblem(ProblemController):
    V_param: int
    C_param: int
    phenotype_names: Dict[int, str]

    def __init__(self, param_handler: ParamHandler, neighbour_controller: NeighbourController, resource_function_controller: Optional[ResourceFunctionController]):
        super().__init__(param_handler, neighbour_controller, resource_function_controller)

        if self.resource_function is None:
            raise Exception('Resource function cannot be None in the following problem')

        self.supported_num_dims = [2, 3]

        self.num_phenotypes = 2
        self.phenotype_names = {0: 'Hawk',
                                1: "Dove"}


    def fitness_problem(self, player: int, enemy: int):
        r = self.resource_function.get_function_value()

        if player == 0 and enemy == 0:
            return (self.V_param - self.C_param) / 2

        elif player == 0 and enemy == 1:
            return r * self.V_param * 0.25

        elif player == 1 and enemy == 0:
            return self.V_param

        elif player == 1 and enemy == 1:
            return (r+1) * self.V_param * 0.5
