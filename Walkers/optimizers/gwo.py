#!/usr/bin/env python

# Reference : https://www.sciencedirect.com/science/article/pii/S0965997813001853
#             https://www.sciencedirect.com/science/article/pii/S0965997816301260

import numpy as np
import time
import sys
from ..solution import Solution

def gwo(objfunc,
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
  alpha_score, beta_score, delta_score = np.inf, np.inf, np.inf
  alpha_pos, beta_pos, delta_pos = np.zeros(shape=(dim, n_population), dtype=float), \
                                   np.zeros(shape=(dim, n_population), dtype=float), \
                                   np.zeros(shape=(dim, n_population), dtype=float)
  walk = np.empty(shape=(max_iters, dim), dtype=float)

  if pos == None:
    # Initialize the population/solutions
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

  if verbose:
    print ("GWO is optimizing \"" + objfunc.__name__ + "\"")

  sol = Solution(dim          = dim,
                 n_population = n_population,
                 max_iters    = max_iters,
                 optimizer    = "GWO",
                 objfname     = objfunc.__name__,
                 start_time   = time.time()
                 )

  at = np.linspace(2, 0, num=max_iters)
  # main loop
  for t, a in enumerate(at):
    # Return back the search agents that go beyond the boundaries of the search space
    pos = np.clip(pos, lower_bound, upper_bound)
    # compute objective function for each search agent
    fitness = np.apply_along_axis(objfunc.evaluate, 0, pos)

    # update alpha, beta and delta
    minpos   = np.argmin(fitness)
    if fitness[minpos] < alpha_score:
        alpha_score = fitness[minpos]
        alpha_pos   = np.array(pos[:, minpos], ndmin=2).T
    if fitness[minpos] > alpha_score and \
       fitness[minpos] < beta_score:
        beta_score = fitness[minpos]
        beta_pos   = np.array(pos[:, minpos], ndmin=2).T
    if fitness[minpos] > alpha_score and \
       fitness[minpos] > beta_score  and \
       fitness[minpos] < delta_score:
        delta_score = fitness[minpos]
        delta_pos   = np.array(pos[:, minpos], ndmin=2).T

    r1 = np.random.uniform(low=0., high=1., size=(dim, n_population))
    r2 = np.random.uniform(low=0., high=1., size=(dim, n_population))
    A  = 2. * a * r1 - a
    C  = 2. * r2
    D_alpha = alpha_pos - abs(C * alpha_pos - pos) * A

    r1 = np.random.uniform(low=0., high=1., size=(dim, n_population))
    r2 = np.random.uniform(low=0., high=1., size=(dim, n_population))
    A  = 2. * a * r1 - a
    C  = 2. * r2
    D_beta = beta_pos - abs(C * beta_pos - pos) * A

    r1 = np.random.uniform(low=0., high=1., size=(dim, n_population))
    r2 = np.random.uniform(low=0., high=1., size=(dim, n_population))
    A  = 2. * a * r1 - a
    C  = 2. * r2
    D_delta = delta_pos - abs(C * delta_pos - pos) * A

    pos = (D_alpha + D_beta + D_delta) / 3

    walk[t] = alpha_pos.T
    if verbose:
      sys.stdout.write('\r')
      sys.stdout.write("It %-5d: [%-25s] %.3f %.3f sec"
                       %(t,
                         '█' * int(t / (max_iters/26)) + '-' * (25 - int(t / (max_iters/26))),
                         alpha_score,
                         time.time() - sol.start_time))
  if verbose:
    sys.stdout.write('\n')

  sol.end_time   = time.time()
  sol.run_time   = sol.end_time - sol.start_time
  sol.walk       = walk
  sol.best       = alpha_score
  sol.population = pos.T

  return sol


if __name__ == "__main__":

  from ..landscape import AckleyFunction

  n_population = 50
  max_iters = 500
  lower_bound = -32
  upper_bound = 32
  dim = 30
  score_func = AckleyFunction(dim=dim)

  sol = gwo(objfunc = score_func,
            lower_bound = lower_bound,
            upper_bound = upper_bound,
            dim = dim,
            n_population = n_population,
            max_iters = max_iters)
