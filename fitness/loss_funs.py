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




