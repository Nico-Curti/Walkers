#!/usr/bin/env python

import numpy as np
import time
import sys
from ..solution import Solution

def gao(objfunc,
        lower_bound,
        upper_bound,
        dim,
        n_population,
        max_iters,
        elite_rate = .1,
        mutation_rate = .3,
        pos = None,
        seed = 0
        ):

  np.random.seed(seed)

  # Initializing arrays
  walk = np.empty(shape=(max_iters, dim), dtype=float)

  if pos == None:
    pos = np.random.uniform(low=lower_bound,
                            high=upper_bound,
                            size=(n_population, dim))
  else:
    assert(pos.shape == 2)
    n, d = pos.shape
    assert(n == n_population)
    assert(d == dim)

  elite = int(n_population * elite_rate)
  if elite == 0:
    raise UserWarning('The elite rate is too small! Automatically set to the 10\% of population')
    elite = int(.1 * n_population)


  new_gen  = np.zeros(shape=(n_population, dim), dtype=float)
  rngcross = np.random.choice(a = range(elite),
                              size=(max_iters, n_population - elite, 2))
  rngmut   = np.random.uniform(low=0.,
                               high=1.,
                               size=(max_iters, n_population, dim))
  rngmut   = rngmut < mutation_rate
  rngswap  = np.random.choice(a=[True, False],
                               size=(max_iters, n_population - elite, dim))


  print ("GAO is optimizing \"" + objfunc.__name__ + "\"")

  sol = Solution(dim          = dim,
                 n_population = n_population,
                 max_iters    = max_iters,
                 optimizer    = "GAO",
                 objfname     = objfunc.__name__,
                 start_time   = time.time()
                 )

  # main loop
  for (t, cross), mut, swap in zip(enumerate(rngcross), rngmut, rngswap):

    fitness = np.apply_along_axis(objfunc.evaluate, 1, pos)
    rank    = np.argsort(fitness)

    pos    = pos[rank]
    best   = pos[0]
    fmin   = fitness[rank[0]]

    # cross over
    new_gen[:elite] = pos[:elite]
    new_gen[elite:][swap] = pos[cross[:,0]][swap]
    swap = ~swap
    new_gen[elite:][swap] = pos[cross[:,1]][swap]

    # mutation
    new_gen[mut]   += np.random.uniform(low=lower_bound,
                                        high=upper_bound,
                                        size=(n_population, dim)
                                        )[mut]

    pos    = np.clip(new_gen, lower_bound, upper_bound)

    walk[t] = best
    sys.stdout.write('\r')
    sys.stdout.write("It %-5d: |%-25s| %.3f %.3f sec"
                     %(t,
                       '█' * int(t / (max_iters/26)) + '-' * (25 - int(t / (max_iters/26))),
                       fmin,
                       time.time() - sol.start_time))
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

  sol = gao(objfunc = score_func,
            lower_bound = lower_bound,
            upper_bound = upper_bound,
            dim = dim,
            n_population = n_population,
            max_iters = max_iters)
