#!/usr/bin/env python

# Reference: https://research.ijcaonline.org/volume69/number3/pxc3887528.pdf
#            http://www2.siit.tu.ac.th/bunyarit/publications/2014_Aor_ADCONIP2014_Japan.pdf

import numpy as np
from scipy.spatial.distance import squareform, pdist
import time
import sys
from ..solution import Solution

new_alpha = lambda alpha, max_iters : (1e-4/.9)**(1. / max_iters) * alpha

def ffa( objfunc,
        lower_bound,
        upper_bound,
        dim,          # Number of dimensions
        n_population, # Population size
        max_iters,    # Number of generations
        alpha = .5,   # Randomness 0--1 (highly random)
        betamin = .2, # minimum value of beta
        beta0 = 1.,   #
        gamma = 1.,   # Absorption coefficient
        seed = 0,
        pos = None,
        verbose = True
        ):

  np.random.seed(int(seed))

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

  walk = np.empty(shape=(max_iters, dim), dtype=float)
  domain = abs(upper_bound - lower_bound)

  if betamin > beta0:
    warnings.warn('Beta-min greater than Beta-0! Automatically swapped')
    betamin, beta0 = beta0, betamin

  if verbose:
    print ("FFA is optimizing \"" + objfunc.__name__ + "\"")

  sol = Solution(dim          = dim,
                 n_population = n_population,
                 max_iters    = max_iters,
                 optimizer    = "FFA",
                 objfname     = objfunc.__name__,
                 start_time   = time.time()
                 )

  # main loop
  for t in range(max_iters):
    # This line of reducing alpha is optional
    alpha = new_alpha(alpha, max_iters)
    # Evaluate new solutions (for all n fireflies)
    fitness = np.apply_along_axis(objfunc.evaluate, 1, pos)

    best = np.argmin(fitness)
    fmin = fitness[best]
    best = pos[best]

    r = squareform(pdist(pos, "euclidean"))
    lightn, light0 = np.meshgrid(fitness, fitness)
    ii, jj = (light0 > lightn).nonzero()
    # The attractiveness parameter beta=exp(-gamma*r)
    beta = (beta0 - betamin) * np.exp(-gamma * r * r) + betamin

    rng = np.random.uniform(low=-.5 * domain * alpha,
                            high=.5 * domain * alpha,
                            size=(n_population, n_population, dim))
    for i, j, b, r in zip(ii, jj, beta[ii, jj], rng[ii, jj]):
      pos[i, :] = pos[i, :] * (1. - b) + pos[j, :] * b + r

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

  sol = ffa(objfunc = score_func,
            lower_bound = lower_bound,
            upper_bound = upper_bound,
            dim = dim,
            n_population = n_population,
            max_iters = max_iters)