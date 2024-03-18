import numpy as np

class Algorithm():


    def __init__(self, func, dim, bounds, max_evals, params=None):

        # Params is for algorithm specific parameters
        if params is None:
            self.params = {}
        else:
            self.params = params
        self.func = func
        self.dim = dim
        self.bounds = bounds
        self.max_evals = max_evals

    def run(self):

        # Best found objective function value
        best = 0

        # Algorithm body

        return best

