#!/usr/bin/env python

# Reference :

import numpy as np
import time
import sys
import sklearn.preprocessing as sk
from ..solution import Solution

def mvo(objfunc,
        lower_bound,
        upper_bound,
        dim,          # Number of dimensions
        n_population, # Population size
        max_iters,    # Number of generations
        wep_max = 1., #
        wep_min = .2, #
        seed = 0,
        pos = None,
        verbose = True
        ):

  np.random.seed(int(seed))

  # Initializing arrays
  walk = np.empty(shape=(max_iters,), dtype=float)

  if pos == None:
    pos = np.random.uniform(low=lower_bound,
                                  high=upper_bound,
                                  size=(dim, n_population))
  else:
    pos = pos.T
    if pos.shape != 2:
      raise Warning('Wrong dimension shape of old generation! Probably you should transpose')
    d, n = pos.shape
    if d != dim or n != n_population:
      raise Warning('Wrong dimension shape of old generation! Number of population or dims incompatible')


  tdrt = [1. - i**.16666 / max_iters**.1666 for i in range(max_iters)]
  wept = np.linspace(wep_min, wep_max, num=max_iters)

  score = np.inf
  pos = np.zeros(shape=(1, dim), dtype=float)

  if verbose:
    print ("MVO is optimizing \"" + objfunc.__name__ + "\"")

  sol = Solution(dim          = dim,
                 n_population = n_population,
                 max_iters    = max_iters,
                 optimizer    = "MVO",
                 objfname     = objfunc.__name__,
                 start_time   = time.time()
                 )

  # main loop
  for (t, wep), tdr in zip(enumerate(wept), tdrt):
    pos = np.clip(pos, lower_bound, upper_bound)
    fitness = np.apply_along_axis(objfunc.evaluate, 0, pos)

    # Update the leader
    idx = np.argmin(fitness)
    if fitness[idx] < score:
      leader_score = fitness[idx]
      leader_pos   = np.array(pos[:, idx], ndmin=2).T

    n = sk.normalize(fitness.reshape((1, -1)), norm='l2', axis=1)

    # Update convergence curve
    walk[t] = leader_score
    if verbose:
      sys.stdout.write('\r')
      sys.stdout.write("It %-5d: [%-25s] %.3f %.3f sec"
                       %(t,
                         '█' * int(t / (max_iters/26)) + '-' * (25 - int(t / (max_iters/26))),
                         score,
                         time.time() - sol.start_time))
  if verbose:
    sys.stdout.write('\n')

  sol.end_time   = time.time()
  sol.run_time   = sol.end_time - sol.start_time
  sol.walk       = walk
  sol.best       = leader_score
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

  sol = mvo(objfunc = score_func,
            lower_bound = lower_bound,
            upper_bound = upper_bound,
            dim = dim,
            n_population = n_population,
            max_iters = max_iters)
