from typing import List, Dict, Optional, Tuple

from neighbourhood.NeighbourController import NeighbourController
from problem.ProblemController import ProblemController
from resource.ResourceFunctionController import ResourceFunctionController
from utils.ParamHandler import ParamHandler


class HawkDoveProblem(ProblemController):
    V_param: int
    C_param: int
    phenotype_names: Dict[int, str]

    def __init__(self, param_handler: ParamHandler, neighbour_controller: NeighbourController, resource_function_controller: Optional[ResourceFunctionController]):
        super().__init__(param_handler, neighbour_controller, resource_function_controller)

        self.supported_num_dims = [2, 3]

        self.num_phenotypes = 2
        self.phenotype_names = {0: 'Hawk',
                                1: "Dove"}


    def fitness_problem(self, player: int, enemy: int, idx: Optional[Tuple[int, int] | Tuple[int, int, int]] = None):
        if player == 0 and enemy == 0:
            return (self.V_param - self.C_param) / 2

        elif player == 1 and enemy == 0:
            return 0

        elif player == 0 and enemy == 1:
            return self.V_param

        elif player == 1 and enemy == 1:
            return self.V_param / 2
