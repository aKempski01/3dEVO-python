from evo_clean.neighbourhood.NeighbourController import NeighbourController
from evo_clean.problem.ProblemController import ProblemController
from evo_clean.utils.ParamHandler import ParamHandler


class ApoptosisProblem(ProblemController):
    params: dict


    def __init__(self, param_handler: ParamHandler, neighbour_controller: NeighbourController):
        super().__init__(param_handler, neighbour_controller)

        self.num_phenotypes = 3


    def fitness_function(self, game_matrix, num_dims):
        if num_dims == 2:
            return self.__fitness_2d(game_matrix)

        if num_dims == 3:
            return self.__fitness_3d(game_matrix)

