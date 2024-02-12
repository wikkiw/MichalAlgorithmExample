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

        # Algorithm body

        # Result
        best = {
            'params': [],
            'fitness': -1,
            'gen': 0,
            'eval_num': 0
        }

        return best

