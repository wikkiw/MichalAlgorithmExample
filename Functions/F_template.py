import numpy as np

def evaluate(x):
    if type(x) is not np.array:
        x = np.array(x)

    return -1


def get_bounds():
    return [-100, 100]
