import config
from config import V_param, C_param


# 0: Dove
# 1: Hawk

def hawk_dove(player: int, enemy: int):
    if player == 1 and enemy == 1:
        return (V_param - C_param)/2

    elif player == 1 and enemy == 0:
        return V_param

    elif player == 0 and enemy == 1:
        return 0

    elif player == 0 and enemy == 0:
        return V_param / 2


# 0: K
# 1: M
# 2: N

def apoptosis(player: int, enemy: int):
    if player == 0:
        if enemy == 0:
            return 1 - config.apo_a + config.apo_b

        if enemy == 1:
            return 1 + config.apo_b + config.apo_c

        if enemy == 2:
            return 1 + config.apo_b

    else:
        if enemy == 0:
            return 1 - config.apo_a

        if enemy == 1:
            return 1 + config.apo_c

        if enemy == 2:
            return 1
