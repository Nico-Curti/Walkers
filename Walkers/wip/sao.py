#!/usr/bin/env python

import numpy as np
import time
import sys
import warnings
from ..solution import Solution

def sao(objfunc,
        lower_bound,
        upper_bound,
        dim,
        n_population,
        max_iters,
        T0 = 1e-2,
        T1 = 1e-6,
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

  if T1 > T0:
    warnings.warn('Final temperature major than minor. Automatically swapped')
    tmp = T0
    T0  = T1
    T1  = tmp

  temperature = np.logspace(np.log10(T0), np.log10(T1), max_iters, endpoint=False)
  new_gen  = np.zeros(shape=(n_population, dim), dtype=float)

  if verbose:
    print ("SAO is optimizing \"" + objfunc.__name__ + "\"")

  sol = Solution(dim          = dim,
                 n_population = n_population,
                 max_iters    = max_iters,
                 optimizer    = "SAO",
                 objfname     = objfunc.__name__,
                 start_time   = time.time()
                 )

  # main loop
  for t, temp in enumerate(temperature):

    fitness = np.apply_along_axis(objfunc.evaluate, 1, pos)


    pos    = np.clip(new_gen, lower_bound, upper_bound)

    walk[t] = best
    if verbose:
      sys.stdout.write('\r')
      sys.stdout.write("It %-5d: |%-25s| %.3f %.3f sec"
                       %(t,
                         '█' * int(t / (max_iters/26)) + '-' * (25 - int(t / (max_iters/26))),
                         fmin,
                         time.time() - sol.start_time))
  if verbose:
    sys.stdout.write('\n')

  sol.end_time   = time.time()
  sol.run_time   = sol.end_time - sol.start_time
  sol.walk       = walk
  sol.best       = best
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

  sol = sao(objfunc = score_func,
            lower_bound = lower_bound,
            upper_bound = upper_bound,
            dim = dim,
            n_population = n_population,
            max_iters = max_iters)
