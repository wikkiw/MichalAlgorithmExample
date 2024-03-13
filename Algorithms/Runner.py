import numpy as np

# Runner (wrapper) class, which handles Algorithm run
class Runner():

    def __init__(self, alg, func, dim, bounds, max_evals, params=None):

        self._evals = 0
        self._max_evals = max_evals
        self._dim = dim
        self._bounds = bounds
        self._func = func

        self._a = alg.Algorithm(self._func_eval_helper, dim, bounds, max_evals, params=params)

        pass

    def _func_eval_helper(self, x):
        #TODO exit run() if eval > max_eval
        #TODO exit/raiseError if outOfBounds
        #TODO exit/raiseError if dim != len(x)
        #TODO log best val
        ret = self._func.evaluate(x)
        self._evals -= 1
        return ret

    def run(self):

        self._a.run()

        pass

