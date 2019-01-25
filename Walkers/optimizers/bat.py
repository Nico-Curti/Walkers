#!/usr/bin/env python

# Reference : https://www.sciencedirect.com/science/article/pii/S0045794913002162
#             https://arxiv.org/pdf/1004.4170.pdf
#             https://www.researchgate.net/publication/258478684_Bat_Algorithm_Inspired_Algorithm_for_Solving_Numerical_Optimization_Problems

import numpy as np
import time
import sys
from ..solution import Solution

def bat(objfunc,
        lower_bound,
        upper_bound,
        dim,          # Number of dimensions
        n_population, # Population size
        max_iters,    # Number of generations
        A = .5,       # Loudness  (constant or decreasing)
        r = .5,       # Pulse rate (constant or decreasing)
        Qmin = 0.,    # Frequency minimum
        Qmax = 2.,    # Frequency maximum
        step = 1e-3,  # scale of normal random generator
        Sol = None,
        seed = 0
        ):

  np.random.seed(seed)

  # Initializing arrays
  Qt = np.random.uniform(low=Qmin, high=Qmax, size=(max_iters, n_population))
  v  = np.zeros(shape=(dim, n_population), dtype=float) # velocities
  walk = np.empty(shape=(max_iters, dim), dtype=float)

  if Sol == None:
    # Initialize the population/solutions
    Sol = np.random.uniform(low=lower_bound,
                            high=upper_bound,
                            size=(dim, n_population))
  else:
    Sol = Sol.T
    assert(Sol.shape == 2)
    d, n = Sol.shape
    assert(d == dim)
    assert(n == n_population)

  print ("BAT is optimizing \"" + objfunc.__name__ + "\"")

  sol = Solution(dim          = dim,
                 n_population = n_population,
                 max_iters    = max_iters,
                 optimizer    = "BAT",
                 objfname     = objfunc.__name__,
                 start_time   = time.time()
                 )

  fitness = np.apply_along_axis(objfunc.evaluate, 0, Sol)
  best = np.argmin(fitness)
  fmin = fitness[best]
  best = np.array(Sol[:, best], ndmin=2)

  rngt = np.random.uniform(low=0., high=1., size=(max_iters,
                                                  n_population))
  rngt = rngt > r
  dim_rngt = np.sum(rngt, axis=1)
  rng2t = np.random.uniform(low=0., high=1., size=(max_iters,
                                                   n_population))
  rng2t = rng2t < A
  # main loop
  for (t, Q), rng, rng2, dim_rng in zip(enumerate(Qt), rngt, rng2t, dim_rngt):
    v += Q * (Sol - best.T)
    S  = Sol + v

    # Pulse rate
    S[:, rng] = best.T + step * np.random.randn(dim, dim_rng)

    # Evaluate new solutions
    fit_new = np.apply_along_axis(objfunc.evaluate, 0, S)

    # Update if the solution improves
    upd = np.logical_and(rng2, fit_new <= fitness)
    Sol[:, upd] = S[:, upd]
    fitness[upd] = fit_new[upd]

    # check boundaries
    Sol = np.clip(Sol, lower_bound, upper_bound)

    best = np.argmin(fitness)
    # Update the current best solution
    fmin = fitness[best]
    best = np.array(Sol[:, best], ndmin=2)
    # Update convergence curve
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
  sol.best       = fmin
  sol.population = Sol.T

  return sol


if __name__ == "__main__":

  from ..landscape import AckleyFunction

  n_population = 50
  max_iters = 500
  lower_bound = -32
  upper_bound = 32
  dim = 30
  score_func = AckleyFunction(dim=dim)

  sol = bat(objfunc = score_func,
            lower_bound = lower_bound,
            upper_bound = upper_bound,
            dim = dim,
            n_population = n_population,
            max_iters = max_iters)
