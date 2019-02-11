#!/usr/bin/env python

# Reference :

import numpy as np
import time
import sys
from bisect import bisect_left
from ..solution import Solution

def bbo(objfunc,
        lower_bound,
        upper_bound,
        dim,            # Number of dimensions
        n_population,   # Population size
        max_iters,      # Number of generations
        pmutate = 1e-2, #
        elite = 2,      #
        seed = 0,
        pos = None,     # initial population
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

  if elite > n_population - 1 or elite <= 0:
    raise Warning('Wrong elite size! It must be in [1, n_population - 1]')
  if isinstance(elite, float):
    elite = int(elite)

  mut = np.linspace(n_population, 1., n_population) / (n_population + 1)
  lambda1t = (1. - mut).reshape((n_population, 1))
  smu = sum(mut)
  cmu = np.cumsum(mut)

  if verbose:
    print ("BBO is optimizing \"" + objfunc.__name__ + "\"")

  sol = Solution(dim          = dim,
                 n_population = n_population,
                 max_iters    = max_iters,
                 optimizer    = "BBO",
                 objfname     = objfunc.__name__,
                 start_time   = time.time()
                 )

  # compute objective function for each particle
  fitness = np.apply_along_axis(objfunc.evaluate, 1, pos)
  idx     = np.argsort(fitness)
  pos     = pos[idx, :]
  fitness = fitness[idx]

  # main loop
  for t in range(max_iters):
    elite_pos = pos[:elite, :]
    elite_cos = fitness[:elite]

    migrate = np.random.uniform(low=0., high=1., size=(n_population, dim))
    migrate = migrate < lambda1t

    new_pos = pos
    # Performing Roulette Wheel
    rng = np.random.uniform(low=0., high=smu, size=(dim*n_population,))
    rng = np.asarray([bisect_left(cmu, r) - 1 for r in rng], dtype=int)
    rng[rng < 0] = 0
    rng = rng.reshape((n_population, dim))

    new_pos[migrate] = pos[migrate][rng[migrate]]

    migrate = ~migrate
    new_pos[migrate] = pos[migrate]

    # Performing Mutation
    mut = np.random.uniform(low=0., high=1., size=(n_population, dim))
    mut = pmutate > mut
    new_pos[mut] = np.random.uniform(low=lower_bound,
                                     high=upper_bound,
                                     size=(n_population, dim))[mut]
    # compute objective function for each individual
    fitness = np.apply_along_axis(objfunc.evaluate, 1, new_pos)
    pos = new_pos

    idx = np.argsort(fitness)
    pos[idx[-elite:], :]  = elite_pos
    fitness[idx[-elite:]] = elite_cos

    idx = np.argsort(fitness)
    pos = pos[idx, :]
    fitness = fitness[idx]

    # Update convergence curve
    walk[t] = pos[idx[0]]
    if verbose:
      sys.stdout.write('\r')
      sys.stdout.write("It %-5d: [%-25s] %.3f %.3f sec"
                       %(t,
                         '█' * int(t / (max_iters/26)) + '-' * (25 - int(t / (max_iters/26))),
                         fitness[0],
                         time.time() - sol.start_time))
  if verbose:
    sys.stdout.write('\n')

  sol.end_time   = time.time()
  sol.run_time   = sol.end_time - sol.start_time
  sol.walk       = walk
  sol.best       = fitness[0]
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

  sol = bbo(objfunc = score_func,
            lower_bound = lower_bound,
            upper_bound = upper_bound,
            dim = dim,
            n_population = n_population,
            max_iters = max_iters)