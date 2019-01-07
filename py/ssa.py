#!usr/bin/python

# Reference : https://www.sciencedirect.com/science/article/pii/S0045794913002162
#             https://arxiv.org/pdf/1004.4170.pdf
#             https://www.researchgate.net/publication/258478684_Bat_Algorithm_Inspired_Algorithm_for_Solving_Numerical_Optimization_Problems

import numpy as np
import time
import sys
from solution import Solution

def ssa(objfunc,
        lower_bound,
        upper_bound,
        dim,          # Number of dimensions
        n_population, # Population size
        max_iters,    # Number of generations
        SalpPos = None,
        seed = 0
        ):

  np.random.seed(seed)

  if SalpPos == None:
    # Initialize the population/solutions
    SalpPos = np.random.uniform(low=lower_bound,
                                high=upper_bound,
                                size=(n_population, dim))

  walk = np.empty(shape=(max_iters,), dtype=float)

  print ("SSA is optimizing \"" + objfunc.__name__ + "\"")

  sol = Solution(dim          = dim,
                 n_population = n_population,
                 max_iters    = max_iters,
                 optimizer    = "SSA",
                 objfname     = objfunc.__name__,
                 start_time   = time.time()
                 )

  fitness = np.apply_along_axis(objfunc, 1, SalpPos)
  best = np.argmin(fitness)
  fmin = fitness[best]
  best = np.array(SalpPos[best], ndmin=2)

  C1 = 2. * np.exp(-(4 * np.arange(2, max_iters + 1) / max_iters)**2)
  half = int(n_population * .5)
  # main loop
  for t, c1 in enumerate(C1):
    c2 = np.random.uniform(low=lower_bound,
                           high=upper_bound,
                           size=(half, dim))
    c3 = np.random.uniform(low=0.,
                           high=1.,
                           size=(half, dim)) < .5
    idx = c3.nonzero()
    SalpPos[idx] = (best + c1 * c2)[idx]
    idx = (~c3).nonzero()
    SalpPos[idx] = (best - c1 * c2)[idx]

    SalpPos[half :] = (SalpPos[half - 1: -1] + SalpPos[half :]) * .5
    SalpPos = np.clip(SalpPos, lower_bound, upper_bound)

    fitness = np.apply_along_axis(objfunc, 1, SalpPos)
    best     = np.argmin(fitness)
    if fitness[best] < fmin:
      fmin = fitness[best]
      best = np.array(SalpPos[best], ndmin=2)

    # Update convergence curve
    walk[t] = fmin

    sys.stdout.write('\r')
    sys.stdout.write("It %-5d: [%-25s] %.3f %.3f sec"
                     %(t,
                       '=' * int(t / 20),
                       fmin,
                       time.time() - sol.start_time))
  sys.stdout.write('\n')

  sol.end_time   = time.time()
  sol.run_time   = sol.end_time - sol.start_time
  sol.walk       = walk
  sol.best       = fmin
  sol.population = SalpPos

  return sol


if __name__ == "__main__":
  # F10
  score_func = lambda x: -20. * np.exp(-.2 * np.sqrt(sum(x*x) / len(x)))     \
                         - np.exp(sum(np.cos(2. * np.pi * x)) / len(x)) \
                         + 22.718281828459045

  n_population = 50
  max_iters = 500
  lower_bound = -32
  upper_bound = 32
  dim = 30

  sol = ssa(objfunc = score_func,
            lower_bound = lower_bound,
            upper_bound = upper_bound,
            dim = dim,
            n_population = n_population,
            max_iters = max_iters)
