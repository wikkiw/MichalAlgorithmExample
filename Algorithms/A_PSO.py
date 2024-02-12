import numpy as np

class Algorithm():

    def __init__(self, func, dim, bounds, max_evals, params=None):

        # Params is for algorithm specific parameters
        if params is None:
            self.params = {
                "c1": 1.49445,
                "c2": 1.49445,
                "w": 0.729,
                "pop_size": 40
            }
        else:
            self.params = params
        self.func = func
        self.dim = dim
        self.bounds = bounds
        self.max_evals = max_evals

    def run(self):

        # Algorithm body -- PSO
        pop_size = self.params.get('pop_size', 10 * self.dim)
        c1 = self.params.get('c1', 1.49445)
        c2 = self.params.get('c2', 1.49445)
        w = self.params.get('w', 0.729)

        # Initialize population
        pop = np.random.rand(pop_size, self.dim) * (self.bounds[1] - self.bounds[0]) + self.bounds[0]
        pop_v = np.zeros((pop_size, self.dim))
        pbest = np.copy(pop)
        pbest_cost = np.array([self.func(ind) for ind in pbest])
        gbest = pop[np.argmin(pbest_cost)]
        gbest_cost = np.min(pbest_cost)
        pop_cost = np.copy(pbest_cost)
        evals = pop_size
        gen = 0

        best = {
            'params': gbest,
            'fitness': gbest_cost,
            'gen': gen,
            'eval_num': np.argmin(pbest_cost)
        }

        # main loop
        while evals < self.max_evals:
            for i in range(pop_size):
                # PSO V update
                r1, r2 = np.random.rand(), np.random.rand()
                pop_v[i] += pop_v[i] * w + c1 * r1 * (pbest[i] - pop[i]) + c2 * r2 * (gbest - pop[i])

                # PSO position update
                pop[i] += pop_v[i]

                # BCM
                pop[i] = np.clip(pop[i], self.bounds[0], self.bounds[1])

                # Update personal best
                current_cost = self.func(pop[i])
                evals += 1
                if current_cost < pbest_cost[i]:
                    pbest[i] = np.copy(pop[i])
                    pbest_cost[i] = current_cost

                if current_cost <= best['fitness']:
                    best['fitness'] = current_cost
                    best['params'] = np.copy(pop[i])
                    best['gen'] = gen
                    best['eval_num'] = evals

                if evals >= self.max_evals:
                    break

            gen += 1

        return best
