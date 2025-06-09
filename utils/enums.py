from enum import Enum


class DeathStrategy(Enum):
    SYNCH = 1
    ASYNCH = 2
    SEMI_SYNCH = 3


class ReproductionStrategy(Enum):
    DETERMINISTIC = 1
    PROBABILISTIC = 2
    WEIGHTED = 3

class SpatialityStrategy(Enum):
    SPATIAL = 1
    MIXED = 2


class NeighborhoodType(Enum):
    VONNEUMAN = 1
    MOORE = 2


class ProblemType(Enum):
    HAWKDOVE = 1
    APOPTOSIS = 2
