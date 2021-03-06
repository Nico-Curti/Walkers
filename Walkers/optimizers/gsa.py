#!/usr/bin/env python

# Reference :

# https://github.com/himanshuRepo/Gravitational-Search-Algorithm/

import numpy as np
import time
import sys
from ..solution import Solution
from scipy.spatial.distance import pdist, squareform

def gsa(objfunc,
        lower_bound,
        upper_bound,
        dim,          # Number of dimensions
        n_population, # Population size
        max_iters,    # Number of generations
        elitist = 1., #
        rpower = 1.,  #
        alpha = 20.,  #
        G0 = 100,     #
        seed = 0,
        pos = None,
        verbose = True
        ):

  np.random.seed(int(seed))

  # Initializing arrays
  walk = np.empty(shape=(max_iters, dim), dtype=float)
  vel  = np.zeros(shape=(n_population, dim), dtype=float)

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

  # Calculating Gravitational Constant
  Gt = G0 * np.exp(-alpha * np.arange(0, max_iters) / max_iters)

  if elitist == 1.: kbest = np.round(n_population * (2. + (1. - np.linspace(0, 1., max_iters)) * (100. - 2.)) / 100.).astype(int)
  else:             kbest = np.repeat(n_population, repeats=max_iters)

  if verbose:
    print ("GSA is optimizing \"" + objfunc.__name__ + "\"")

  sol = Solution(dim          = dim,
                 n_population = n_population,
                 max_iters    = max_iters,
                 optimizer    = "GSA",
                 objfname     = objfunc.__name__,
                 start_time   = time.time()
                 )

  fitness = np.apply_along_axis(objfunc.evaluate, 1, pos)
  fmax = max(fitness)
  fmin = min(fitness)
  epsil = np.finfo(float).eps

  for (t, G), k in zip(enumerate(Gt), kbest):
    pos = np.clip(pos, lower_bound, upper_bound)

    # Calculating Mass
    if fmax == fmin: M = np.ones(shape=(n_population,))
    else:            M = (fitness - fmax) / (fmin - fmax)
    M /= sum(M)

    ## Calculating Gfield
    ds = np.argsort(M)[::-1]
    distance = squareform(pdist(pos[ds, :], metric="euclidean"))
    force = np.zeros(shape=(n_population, dim), dtype=float)
    for z in ds[:k]:
      R = np.array(distance[:, z], ndmin=2).T
      force += np.random.uniform(low=0., high=1., size=(n_population, dim)) * \
               M[z] * (pos[z, :] - pos) / (R**rpower + epsil)

    acc = force * G

    # Calculating Position
    vel  = np.random.uniform(low=0., high=1., size=(n_population, dim)) * vel + acc
    pos += vel

    fitness = np.apply_along_axis(objfunc.evaluate, 1, pos)
    fmax = max(fitness)
    best = np.argmin(fitness)
    fmin = fitness[best]
    best = pos[best]
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

  sol = gsa(objfunc = score_func,
            lower_bound = lower_bound,
            upper_bound = upper_bound,
            dim = dim,
            n_population = n_population,
            max_iters = max_iters)


