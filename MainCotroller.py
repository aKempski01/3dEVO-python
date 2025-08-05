import time

from mortality.MortalityController import MortalityController
from mortality.Asynch import Asynch
from mortality.Synch import Synch
from mortality.SemiSynch import SemiSynch

from problem.ProblemController import ProblemController
from problem.HawkDoveProblem import HawkDoveProblem
from problem.ApoptosisProblem import ApoptosisProblem

from neighbourhood.NeighbourController import NeighbourController
from neighbourhood.MooreNeighbour import Moore
from neighbourhood.VonNeumannNeighbour import VonNeumann

from reproduction.ReproductionController import ReproductionController
from reproduction.Weighted import Weighted
from reproduction.Deterministic import Deterministic
from reproduction.Probabilistic import Probabilistic

from utils.MatrixOperations import get_game_matrix
from utils.ParamHandler import ParamHandler
from utils.SaveController import SaveController


# todo:
# poprawić wizualizacje w 3D



class MainCotroller:
    problem_controller: ProblemController
    param_handler: ParamHandler
    neighbour_controller: NeighbourController
    mortality_controller: MortalityController
    reproduction_controller: ReproductionController
    save_controller: SaveController


    def __init__(self, yaml_path: str):
        self.param_handler = ParamHandler(yaml_path)
        self.__get_neighbour()

        self.__get_problem_controller()
        self.__get_mortality()
        self.__get_reproduction()

        self.param_handler.set_num_phenotypes(self.problem_controller.num_phenotypes)


        self.save_controller = SaveController(self.param_handler)


    def run(self):
        self.save_controller.save_yaml_file(self.problem_controller)
        game_matrix = get_game_matrix(self.param_handler)

        self.save_controller.save_game_matrix(game_matrix, 0)
        for epoch in range(self.param_handler.num_epochs):
            print("-----------------------")
            s = time.time()
            pay_off_matrix = self.problem_controller.fitness_function(game_matrix)
            indices = self.mortality_controller.get_cells_to_update(game_matrix)

            game_matrix = self.reproduction_controller.reproduce(game_matrix, pay_off_matrix, indices)



            self.save_controller.save_game_matrix(game_matrix, epoch+1)
            print("Epoch {} computed in {}".format(epoch, time.time() - s))



    def __get_problem_controller(self):
        problems = ProblemController.__subclasses__()
        try:
            self.problem_controller = [p(self.param_handler, self.neighbour_controller) for p in problems if p.__name__ == self.param_handler.problem_name][0]
        except IndexError:
            exit("There is no problem named {}. Make sure, that problem name is the same as class name and class is included at the top of the file".format(self.param_handler.problem_name))


    def __get_neighbour(self):
        neighbours = NeighbourController.__subclasses__()
        try:
            self.neighbour_controller = [n(self.param_handler) for n in neighbours if n.__name__ == self.param_handler.neighbourhood_type][0]
        except IndexError:
            exit("There is no neighbourhood method named {}. Make sure, that neighbourhood name is the same as class name and class is included at the top of the file".format(self.param_handler.neighbourhood_type))


    def __get_mortality(self):
        mortalities = MortalityController.__subclasses__()
        try:
            self.mortality_controller = [m(self.param_handler) for m in mortalities if m.__name__ == self.param_handler.mortality_strategy][0]
        except IndexError:
            exit("There is no mortality method named {}. Make sure, that mortality name is the same as class name and class is included at the top of the file".format(self.param_handler.mortality_strategy))


    def __get_reproduction(self):
        reproductions = ReproductionController.__subclasses__()
        try:
            self.reproduction_controller = [r(self.param_handler, self.neighbour_controller) for r in reproductions if r.__name__ == self.param_handler.reproduction_strategy_name][0]
        except IndexError:
            exit("There is no reproduction strategy named {}. Make sure, that reproduction name is the same as class name and class is included at the top of the file".format(self.param_handler.reproduction_strategy_name))

