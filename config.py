from utils.enums import DeathStrategy, ReproductionStrategy, SpatialityStrategy, NeighborhoodType, ProblemType

num_of_dims = 2
num_of_phenotypes = 2
max_iterations = 50
pop_length = 32


death_strategy = DeathStrategy.SEMI_SYNCH

mortality_rate = 0.1

reproduction_strategy = ReproductionStrategy.DETERMINISTIC
num_of_cells_for_mean = 6

spatiality_strategy = SpatialityStrategy.MIXED

neighborhood_type = NeighborhoodType.VONNEUMAN




parallel = True
num_cpu = 8


problem_type = ProblemType.HAWKDOVE
# problem_type = ProblemType.APOPTOSIS

### Hawk - Dove problem
V_param = 6
C_param = 9

# Apoptosis problem
apo_a = 0.2
apo_b = 0.3
apo_c = 0


def validate_config():
    return True