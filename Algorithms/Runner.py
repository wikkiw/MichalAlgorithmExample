import numpy as np

class MaxEvalException(Exception):

    def __init__(self, a, f):
        self.text = f'WARNING: Algorithm {a.__module__} tried to exceed maximum number of evaluations on function = {f.__name__}.'

class DimException(Exception):

    def __init__(self, a, dim, length, f):
        self.text = f'ERROR: Algorithm {a.__module__} passed array of length = {length} for problem of dim = {dim} on function = {f.__name__}.'

# Runner (wrapper) class, which handles Algorithm run
class Runner():

    def __init__(self, alg, func, dim, bounds, max_evals, params=None):

        self._evals = 0
        self._max_evals = max_evals
        self._dim = dim
        self._bounds = bounds
        self._func = func
        # Result
        self._best = {
            'params': np.array([]),
            'fitness': None,
            'eval_num': 0,
            'error': 0
        }
        self._flag_OoB = False
        self._flag_MaxEval = False
        self._flag_Dim = False

        self._a = alg.Algorithm(self._func_eval_helper, dim, bounds, max_evals, params=params)

        pass


    def _func_eval_helper(self, x):

        # Max evaluations check
        if self._evals >= self._max_evals:
            if not self._flag_MaxEval:
                self._flag_MaxEval = True
            self._evals += 1
            raise MaxEvalException(self._a, self._func)
            #return np.random.rand()

        # Check dim vs len(x)
        if self._dim != len(x):
            if not self._flag_Dim:
                self._flag_Dim = True
            self._best['error'] = 1
            raise DimException(self._a, self._dim, len(x), self._func)
            #return np.random.rand()

        # Out of bounds check
        xx = np.clip(x, self._bounds[0], self._bounds[1])
        comp = x == xx
        equal_arr = comp.all()
        if equal_arr == False:
            if not self._flag_OoB:
                print(f'WARNING: Algorithm {self._a.__module__} tried to evaluate out of bounds. Parameters were clipped to bounds.')
                self._flag_OoB = True

        ret = self._func.evaluate(xx)

        # Logging best found value
        if self._best['fitness'] is None or ret <= self._best['fitness']:
            self._best['fitness'] = ret
            self._best['params'] = xx
            self._best['eval_num'] = self._evals

        self._evals += 1

        return ret



    def run(self):

        try:
            self._a.run()
        except MaxEvalException as e:
            print(e.text)
        except DimException as e:
            print(e.text)
        #for checking general unexpected exceptions
        except Exception as e:
            print(f'WARNING: Algorithm {self._a.__module__} raised unexpected exception {e} on function = {self._func.__name__}.')

        return self._best

