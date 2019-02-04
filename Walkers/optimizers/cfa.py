#!/usr/bin/env python

# Reference :

import numpy as np
import time
import sys
from ..solution import Solution

def cfa(objfunc,
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

  # Initializing arrays
  walk = np.empty(shape=(max_iters, dim), dtype=float)

  if pos == None:
    pos = np.random.uniform(low=lower_bound,
                            high=upper_bound,
                            size=(n_population, dim))
  else:
    if pos.shape != 2:
      raise Warning('Wrong dimension shape of old generation! Probably you should transpose')
    n, d = pos.shape
    if d != dim or n != n_population:
      raise Warning('Wrong dimension shape of old generation! Number of population or dims incompatible')

  m = n_population // 4
  g21 = m + 1
  g22 = 2 * m
  g31 = g22 + 1
  g32 = 3 * m
  g41 = g32 + 1

  if verbose:
    print ("CFA is optimizing \"" + objfunc.__name__ + "\"")

  sol = Solution(dim          = dim,
                 n_population = n_population,
                 max_iters    = max_iters,
                 optimizer    = "CFA",
                 objfname     = objfunc.__name__,
                 start_time   = time.time()
                 )

  fitness = np.apply_along_axis(objfunc.evaluate, 1, pos)
  best = np.argmin(fitness)
  fmin = fitness[best]
  best = pos[best, :]

  Rt = np.random.uniform(low=-1.,  high=2., size=(max_iters,))
  Vt = np.random.uniform(low=-1.5, high=1.5, size=(max_iters,))
  Wt = np.random.uniform(low=-1., high=1., size=(max_iters,))

  # main loop
  for (t, R), V, W in zip(enumerate(Rt), Vt, Wt):
    avg_best = np.mean(best)

    pos[:m, :]      = R * pos[:m, :] + (best - pos[:m, :]) # * 1.
    pos[g21:g22, :] = V * (best - pos[g21:g22, :]) + best # * 1.
    pos[g31:g32, :] = W * (best - avg_best) + best # * 1.
    pos[g41:, :]    = np.random.uniform(low=lower_bound,
                                        high=upper_bound,
                                        size=(n_population - g41, dim))

    fitness = np.apply_along_axis(objfunc.evaluate, 1, pos)
    best = np.argmin(fitness)
    fmin = fitness[best]
    best = pos[best, :]

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

  sol = cfa(objfunc = score_func,
            lower_bound = lower_bound,
            upper_bound = upper_bound,
            dim = dim,
            n_population = n_population,
            max_iters = max_iters)

