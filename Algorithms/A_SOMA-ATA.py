import numpy as np

class Algorithm():

    def __init__(self, func, dim, bounds, max_evals, params=None):

        # Params is for algorithm specific parameters
        if params is None:
            self.params = {
                "pop_size": 40,
                "step_size": 0.11,
                "prt": 0.3,
                "path_length": 2.0
            }
        else:
            self.params = params
        self.func = func
        self.dim = dim
        self.bounds = bounds
        self.max_evals = max_evals


    def run(self):

        # Algorithm body
        # Default parameters for SOMA
        pop_size = self.params.get('pop_size', 10 * self.dim)
        step_size = self.params.get('step_size', 0.11)
        prt = self.params.get('prt', 0.1)  # Perturbation
        path_length = self.params.get('path_length', 2.0)

        pop = np.random.rand(pop_size, self.dim) * (self.bounds[1] - self.bounds[0]) + self.bounds[0]
        pop_cf = np.array([self.func(ind) for ind in pop])
        evals = pop_size
        gen = 0
        best_index = np.argmin(pop_cf)

        best = {
            'params': pop[best_index],
            'fitness': pop_cf[best_index],
            'gen': gen,
            'eval_num': np.argmin(pop_cf)
        }

        for i in range(pop_size):
            for j in range(pop_size):
                if i != j:  # An individual does not move towards itself
                    # Initialize trial individual
                    trial = np.copy(pop[i])
                    for step in np.arange(0, path_length, step_size):
                        # Perturbation mask
                        mask = np.random.rand(self.dim) < prt

                        print(mask)
                        return


                        # Move towards another individual
                        trial_temp = trial + mask * (pop[j] - trial) * step
                        # Ensure trial is within bounds
                        trial_temp = np.clip(trial_temp, self.bounds[:, 0], self.bounds[:, 1])
                        trial_fitness = self.func(trial_temp)
                        if trial_fitness < fitness[i]:
                            trial = trial_temp
                            fitness[i] = trial_fitness




        # Result
        best = {
            'params': [],
            'fitness': -1,
            'gen': 0,
            'eval_num': 0
        }

        return best

if __name__ == '__main__':

    from Functions import F_Sphere

    algorithm = Algorithm(F_Sphere.evaluate, 3, [-5, 5], 1000)
    algorithm.run()