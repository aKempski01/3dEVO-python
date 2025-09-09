from typing import Optional

import numpy as np
import yaml

from utils.Enums import SpatialityStrategy


class ParamHandler:
    experiment_name: str
    problem_name: str
    problem_params: dict
    phenotype_names_to_idx: dict

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

    chosen_resource_function: str = "None"
    resource_function_params: dict

    def __init__(self, yaml_path: str):
        self.initial_probability = None
        self.__load_params_from_yaml(yaml_path)


    def __load_params_from_yaml(self, yaml_path: str):

        with open(yaml_path, 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)

        if 'save_history' in data:
            self.save_history_after_calculations = data['save_history']
        else:
            self.save_history_after_calculations = False

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
            s = np.sum(list(self.initial_probability.values()))
            for k in self.initial_probability.keys():
                self.initial_probability[k] /= s
                self.initial_probability[k] = float(self.initial_probability[k])
            self.num_phenotypes = len(self.initial_probability.keys())

        if 'num_phenotypes' in data.keys():
            self.num_phenotypes = data['num_phenotypes']

        if "phenotype_names" in data.keys():
            self.phenotype_names = data['phenotype_names']

        elif "phenotype_name" not in data.keys() and 'num_phenotypes' in data.keys():
            self.phenotype_names = {}
            for n in range(data['num_phenotypes']):
                self.phenotype_names[n] = str(n)

        if 'initial_matrix' in data.keys() and data['initial_matrix'] != 'None':
            self.initial_matrix_path = data['initial_matrix']


        if 'chosen_resource_function' in data.keys():
            self.chosen_resource_function = data['chosen_resource_function']
            if 'resource_function_params' in data.keys():
                self.resource_function_params = data['resource_function_params']

        else:
            self.chosen_resource_function = "None"

    def update_phenotype_names_to_idx(self):
        if hasattr(self, 'initial_probability'):
            ks = list(self.initial_probability.keys()).copy()
            for k in ks:
                self.initial_probability[[key for key, val in self.phenotype_names_to_idx.items() if val == k][0]] = self.initial_probability.pop(k)

        if hasattr(self, 'resource_function_params') and 'resource_phenotypes' in self.resource_function_params.keys() and self.chosen_resource_function != 'None':
            for k, v in list(self.resource_function_params['resource_phenotypes'].items()):
                self.resource_function_params['resource_phenotypes'][k] = [key for key, val in self.phenotype_names_to_idx.items() if val == v][0]

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
                self.initial_probability[str(i)] = 1 / self.num_phenotypes
