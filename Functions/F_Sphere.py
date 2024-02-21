import numpy as np


def evaluate(x):
    if type(x) is not np.array:
        x = np.array(x)

    return np.sum(x ** 2)


def get_bounds():
    return [-5.12, 5.12]
