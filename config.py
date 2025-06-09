from utils.enums import DeathStrategy, ReproductionStrategy, SpatialityStrategy, NeighborhoodType, ProblemType

num_of_dims = 2
num_of_phenotypes = 2
max_iterations = 500
pop_length = 32


death_strategy = DeathStrategy.SEMI_SYNCH

mortality_rate = 0.1

reproduction_strategy = ReproductionStrategy.WEIGHTED
num_of_cells_for_mean = 6

spatiality_strategy = SpatialityStrategy.MIXED

neighborhood_type = NeighborhoodType.VONNEUMAN






problem_type = ProblemType.HAWKDOVE
# problem_type = ProblemType.APOPTOSIS

### Hawk - Dove problem
V_param = 6
C_param = 9




def validate_config():
    return True