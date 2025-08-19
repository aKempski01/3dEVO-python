from typing import Optional, Tuple

from neighbourhood.NeighbourController import NeighbourController
from problem.ProblemController import ProblemController
from resource.ResourceFunctionController import ResourceFunctionController
from utils.ParamHandler import ParamHandler


class ApoptosisProblem(ProblemController):
    a_param: int
    b_param: int
    c_param: int

    def __init__(self, param_handler: ParamHandler, neighbour_controller: NeighbourController, resource_function_controller: Optional[ResourceFunctionController]):
        super().__init__(param_handler, neighbour_controller, resource_function_controller)

        self.num_phenotypes = 3
        self.supported_num_dims = [2, 3]
        self.phenotype_names = {0: 'K',
                                1: "M",
                                2: "N"}

    # 0: K, 1: M. 2: N

    def fitness_problem(self, player: int, enemy: int, idx: Optional[Tuple[int, int] | Tuple[int, int, int]] = None):
        if player == 0 and enemy == 0:
            return 1 - self.a_param + self.b_param

        elif player == 0 and enemy != 0:
            return 1 - self.a_param

        elif player == 1 and enemy == 0:
            return 1 + self.b_param + self.c_param

        elif player == 1 and enemy != 0:
            return 1 + self.c_param

        elif player == 2 and enemy == 0:
            return 1 + self.b_param

        elif player == 2 and enemy != 0:
            return 1

