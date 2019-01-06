#!usr/bin/python

# Reference : http://www.swarmintelligence.org/tutorials.php

import numpy as np
import time
import sys
from solution import Solution

def pso(objfunc,
        lower_bound,
        upper_bound,
        dim,          # Number of dimensions
        n_population, # Population size
        max_iters,    # Number of generations
        Vmax = 6.,    #
        wmax = .9,    #
        wmin = .2,    #
        c1   = 2.,    #
        c2   = 2.,    #
        pos  = None,
        seed = 0
        ):

  np.random.seed(seed)

  # Initializing arrays
  walk = np.empty(shape=(max_iters,), dtype=float)

  if pos == None:
    pos = np.random.uniform(low=lower_bound,
                            high=upper_bound,
                            size=(dim, n_population))

  vel = np.zeros(shape=(dim, n_population))
  wt = np.linspace(wmax, wmin, num=max_iters)
  p_score = np.repeat(np.inf, repeats=n_population)
  p_best = np.zeros(shape=(dim, n_population), dtype=float)
  g_score = np.inf
  g_best  = np.zeros(shape=(1, dim))

  print ("PSO is optimizing \"" + objfunc.__name__ + "\"")

  sol = Solution(dim          = dim,
                 n_population = n_population,
                 max_iters    = max_iters,
                 optimizer    = "PSO",
                 objfname     = objfunc.__name__,
                 start_time   = time.time()
                 )

  # main loop
  for t, w in enumerate(wt):
    # Check if moths go out of the search spaceand bring it back
    pos = np.clip(pos, lower_bound, upper_bound)
    # evaluate moths
    fitness = np.apply_along_axis(objfunc, 0, pos)
    idx = fitness < p_score
    p_best[:, idx]  = pos[:, idx]
    p_score[idx] = fitness[idx]

    idx = np.argmin(fitness)
    if fitness[idx] < g_score:
      g_score = fitness[idx]
      g_best  = np.array(pos[:, idx], ndmin=2).T

    # update the W of PSO
    r1 = np.random.uniform(low=0., high=1., size=(dim, n_population))
    r2 = np.random.uniform(low=0., high=1., size=(dim, n_population))

    vel = w * vel + c1 * r1 * (p_best - pos) + c2 * r2 * (g_best - pos)
    vel = np.clip(vel, -Vmax, Vmax)
    pos += vel

    # Update convergence curve
    walk[t] = g_score
    sys.stdout.write('\r')
    sys.stdout.write("It %-5d: [%-25s] %.3f %.3f sec"
                     %(t,
                       '=' * int(t / 20),
                       g_score,
                       time.time() - sol.start_time))
  sys.stdout.write('\n')

  sol.end_time   = time.time()
  sol.run_time   = sol.end_time - sol.start_time
  sol.walk       = walk
  sol.best       = g_score
  sol.population = pos

  return sol


if __name__ == "__main__":
  # F10
  score_func = lambda x: -20. * np.exp(-.2 * np.sqrt(sum(x*x) / len(x)))     \
                         - np.exp(sum(np.cos(2. * np.pi * x)) / len(x)) \
                         + 22.718281828459045

  n_population = 50
  max_iters = 500
  lower_bound = -32
  upper_bound = 32
  dim = 30

  sol = pso(objfunc = score_func,
            lower_bound = lower_bound,
            upper_bound = upper_bound,
            dim = dim,
            n_population = n_population,
            max_iters = max_iters)
