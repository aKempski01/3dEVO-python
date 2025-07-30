from neighbourhood.NeighbourController import NeighbourController
from problem.ProblemController import ProblemController
from utils.ParamHandler import ParamHandler


class ApoptosisProblem(ProblemController):
    a_param: int
    b_param: int
    c_param: int

    def __init__(self, param_handler: ParamHandler, neighbour_controller: NeighbourController):
        super().__init__(param_handler, neighbour_controller)

        self.num_phenotypes = 3
        self.supported_num_dims = [2, 3]
        self.phenotype_names = {0: 'K',
                                1: "M",
                                2: "N"}

    # 0: K, 1: M. 2: N

    def fitness_problem(self, player: int, enemy: int):
        if player == 0 and enemy == 0:
            return 1 - self.a_param + self.b_param

        elif player != 0 and enemy == 0:
            return 1 - self.a_param

        elif player == 0 and enemy == 1:
            return 1 + self.b_param + self.c_param

        elif player != 0 and enemy == 1:
            return 1 + self.c_param

        elif player == 0 and enemy == 2:
            return 1 + self.b_param

        elif player != 0 and enemy == 2:
            return 1

