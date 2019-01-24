#!/usr/bin/env python

# Reference : https://www.sciencedirect.com/science/article/pii/S0950705115002580

import numpy as np
import time
import sys
from ..solution import Solution

def mfo(objfunc,
        lower_bound,
        upper_bound,
        dim,          # Number of dimensions
        n_population, # Population size
        max_iters,    # Number of generations
        b = 1.,       #
        positions = None,
        seed = 0
        ):

  np.random.seed(seed)

  # Initializing arrays
  walk = np.empty(shape=(max_iters,), dtype=float)

  if positions == None:
    positions = np.random.uniform(low=lower_bound,
                                  high=upper_bound,
                                  size=(dim, n_population))

  at = np.linspace(-1, -2, num=max_iters)
  flames = [np.round(n_population - i*(n_population - 1)/max_iters)
            for i in range(1, max_iters + 1)]

  print ("MFO is optimizing \"" + objfunc.__name__ + "\"")

  sol = Solution(dim          = dim,
                 n_population = n_population,
                 max_iters    = max_iters,
                 optimizer    = "MFO",
                 objfname     = objfunc.__name__,
                 start_time   = time.time()
                 )

  fitness = np.apply_along_axis(objfunc, 0, positions)

  idx = np.argsort(fitness)
  sort_pos = pos[idx, :]
  fmin = fitness[idx[0]]

  # main loop
  for (t, a), flame in zip(enumerate(at), flames):
    # Check if moths go out of the search spaceand bring it back
    positions = np.clip(positions, lower_bound, upper_bound)
    # evaluate moths
    fitness = np.apply_along_axis(objfunc, 0, positions)

    t = (a - 1.) * np.random.uniform(low=1,
                                     high=(a - 1.) + 1,
                                     size=(dim, n_population))
    positions[:, : flame] = * np.exp(b * t) * np.cos(t * 2. * np.pi) +
    positions[:, flame: ] = * np.exp(b * t) * np.cos(t * 2. * np.pi) +

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
  sol.population = positions

  return sol


if __name__ == "__main__":

  from ..landscape import AckleyFunction

  n_population = 50
  max_iters = 500
  lower_bound = -32
  upper_bound = 32
  dim = 30
  score_func = AckleyFunction(dim=dim)

  sol = mfo(objfunc = score_func,
            lower_bound = lower_bound,
            upper_bound = upper_bound,
            dim = dim,
            n_population = n_population,
            max_iters = max_iters)
