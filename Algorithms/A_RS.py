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

        best = {}

        # Algorithm body
        for eval in range(self.max_evals):
            params = np.random.rand(self.dim) * (self.bounds[1] - self.bounds[0]) + self.bounds[0]
            fitness = self.func(params)
            if best == {} or fitness < best['fitness']:
                best['params'] = params
                best['fitness'] = fitness
                best['eval_num'] = eval
                best['gen'] = eval

        return best