import numpy as np


def evaluate(x):
    return np.sum(x ** 4)


def get_bounds():
    return [-5.12, 5.12]