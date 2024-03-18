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

        best = pop_cf[best_index]

        while evals < self.max_evals:

            new_pop = np.copy(pop)
            new_pop_cf = np.copy(pop_cf)

            for i in range(pop_size):
                # select leader
                leader = i
                while leader == i:
                    leader = np.random.randint(0, pop_size-1, 1)[0]
                    pass

                # move trials towards leader
                trial = np.copy(pop[i])
                trial_cf = pop_cf[i]

                for step in np.arange(step_size, path_length, step_size):
                    # Perturbation mask
                    mask = (np.random.rand(self.dim) < prt).astype(int)
                    # trial step
                    trial_temp = pop[i] + mask * (pop[leader] - pop[i]) * step
                    # bounds check
                    trial_temp = np.clip(trial_temp, self.bounds[0], self.bounds[1])
                    trial_temp_cf = self.func(trial_temp)
                    # new trial
                    if trial_temp_cf < trial_cf:
                        trial_cf = trial_temp_cf
                        trial = np.copy(trial_temp)
                        # test best
                        if trial_cf < best:
                            best = trial_cf

                    evals += 1
                    if evals >= self.max_evals:
                        break

                # copy trial to new pop
                new_pop[i] = np.copy(trial)
                new_pop_cf[i] = trial_cf

                # for i end
                if evals >= self.max_evals:
                    break
                pass

            # copy new pop into new generation
            pop = np.copy(new_pop)
            pop_cf = np.copy(new_pop_cf)
            gen += 1

            # main while end
            if evals >= self.max_evals:
                break
            pass

        pass

        return best

if __name__ == '__main__':

    from Functions import F_Sphere

    algorithm = Algorithm(F_Sphere.evaluate, 3, [-5, 5], 10000)
    print(algorithm.run())