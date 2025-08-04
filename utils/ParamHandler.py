from typing import Optional

import yaml

from utils.Enums import SpatialityStrategy

class ParamHandler:
    experiment_name: str
    problem_name: str
    problem_params: dict

    initial_matrix_path: Optional[str] = None

    num_epochs: int
    num_dim: int
    population_length: int
    num_phenotypes: int
    neighbourhood_type: str
    mortality_strategy: str
    mortality_rate: float

    reproduction_strategy_name: str
    num_cells_for_mean: int

    parallel: bool
    num_cpu: int

    mortality_rate: float

    def __init__(self, yaml_path: str):
        self.__load_params_from_yaml(yaml_path)

    def __load_params_from_yaml(self, yaml_path: str):

        with open(yaml_path, 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)

        self.experiment_name = data['experiment_name']
        self.problem_name = data['problem_name']
        self.problem_params = data['problem_params']


        self.num_epochs = data['num_epochs']
        self.population_length = data['population_length']
        self.num_dim = data['num_dim']

        self.neighbourhood_type = data['neighbourhood_type']

        if data['spatiality_strategy'] == "MIXED":
            self.spatiality_strategy = SpatialityStrategy.MIXED

        elif data['spatiality_strategy'] == "SPATIAL":
            self.spatiality_strategy = SpatialityStrategy.SPATIAL

        else:
            raise ValueError("Spatiality strategy not supported")


        self.mortality_strategy = data['mortality_strategy']
        self.mortality_rate = data['mortality_rate']

        self.parallel = data['run_in_parallel']
        self.num_cpu = data['num_cpu']

        self.reproduction_strategy_name = data['reproduction_strategy_name']
        self.num_cells_for_mean = data['num_cells_for_mean']

        if 'initial_probability' in data.keys():
            self.initial_probability = data['initial_probability']
            self.num_phenotypes = len(self.initial_probability.keys())

        if 'num_phenotypes' in data.keys():
            self.num_phenotypes = data['num_phenotypes']

        if "phenotype_names" in data.keys():
            self.phenotype_names = data['phenotype_names']

        elif "phenotype_name" not in data.keys() and 'num_phenotypes' in data.keys():
            self.phenotype_names = {}
            for n in range(data['num_phenotypes']):
                self.phenotype_names[n] = str(n)


        if data['initial_matrix'] != 'None':
            self.initial_matrix_path = data['initial_matrix']



    def set_num_phenotypes(self, num_phenotypes: int):
        if hasattr(self, 'num_phenotypes') and self.num_phenotypes is not None:
            if hasattr(self, 'phenotype_names') and len(self.phenotype_names) != num_phenotypes:
                raise ValueError("Number of phenotype names does not match number of phenotypes")

            if self.num_phenotypes != num_phenotypes:
                raise ValueError("Number of initial phenotype probabilities does not match number of phenotypes")
        else:
            self.num_phenotypes = num_phenotypes

        if not hasattr(self, 'initial_probability') or len(self.initial_probability.keys()) != self.num_phenotypes:
            self.initial_probability = {}

            for i in range(self.num_phenotypes):
                self.initial_probability[str(i)] = 1/self.num_phenotypes



