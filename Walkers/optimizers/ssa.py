#!/usr/bin/env python

# Reference : https://www.sciencedirect.com/science/article/pii/S0045794913002162
#             https://arxiv.org/pdf/1004.4170.pdf
#             https://www.researchgate.net/publication/258478684_Bat_Algorithm_Inspired_Algorithm_for_Solving_Numerical_Optimization_Problems

import numpy as np
import time
import sys
from ..solution import Solution

def ssa(objfunc,
        lower_bound,
        upper_bound,
        dim,          # Number of dimensions
        n_population, # Population size
        max_iters,    # Number of generations
        seed = 0,
        pos = None,
        verbose = True
        ):

  np.random.seed(int(seed))

  if pos == None:
    # Initialize the population/solutions
    pos = np.random.uniform(low=lower_bound,
                                high=upper_bound,
                                size=(n_population, dim))
  else:
    if pos.shape != 2:
      raise Warning('Wrong dimension shape of old generation! Probably you should transpose')
    n, d = pos.shape
    if d != dim or n != n_population:
      raise Warning('Wrong dimension shape of old generation! Number of population or dims incompatible')

  walk = np.empty(shape=(max_iters, dim), dtype=float)

  if verbose:
    print ("SSA is optimizing \"" + objfunc.__name__ + "\"")

  sol = Solution(dim          = dim,
                 n_population = n_population,
                 max_iters    = max_iters,
                 optimizer    = "SSA",
                 objfname     = objfunc.__name__,
                 start_time   = time.time()
                 )

  fitness = np.apply_along_axis(objfunc.evaluate, 1, pos)
  best = np.argmin(fitness)
  fmin = fitness[best]
  best = np.array(pos[best], ndmin=2)

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
    pos[idx] = (best + c1 * c2)[idx]
    idx = (~c3).nonzero()
    pos[idx] = (best - c1 * c2)[idx]

    pos[half :] = (pos[half - 1: -1] + pos[half :]) * .5
    pos = np.clip(pos, lower_bound, upper_bound)

    fitness = np.apply_along_axis(objfunc.evaluate, 1, pos)
    best     = np.argmin(fitness)
    if fitness[best] < fmin:
      fmin = fitness[best]
      best = np.array(pos[best], ndmin=2)

    # Update convergence curve
    walk[t] = best
    if verbose:
      sys.stdout.write('\r')
      sys.stdout.write("It %-5d: [%-25s] %.3f %.3f sec"
                       %(t,
                         '█' * int(t / (max_iters/26)) + '-' * (25 - int(t / (max_iters/26))),
                         fmin,
                         time.time() - sol.start_time))
  if verbose:
    sys.stdout.write('\n')

  sol.end_time   = time.time()
  sol.run_time   = sol.end_time - sol.start_time
  sol.walk       = walk
  sol.best       = fmin
  sol.population = pos

  return sol


if __name__ == "__main__":

  from ..landscape import AckleyFunction

  n_population = 50
  max_iters = 500
  lower_bound = -32
  upper_bound = 32
  dim = 30
  score_func = AckleyFunction(dim=dim)

  sol = ssa(objfunc = score_func,
            lower_bound = lower_bound,
            upper_bound = upper_bound,
            dim = dim,
            n_population = n_population,
            max_iters = max_iters)
