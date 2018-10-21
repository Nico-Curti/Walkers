#!usr/bin/python

# Reference :

import numpy as np
import time
import sys
from bisect import bisect_left

np.random.seed(123)

solution = {"best" : 0.,
            "walk" : [],
            "optimizer" : "",
            "objfname"  : "",
            "start_time" : 0.,
            "end_time"   : 0.,
            "execution_time" : 0.,
            "dimension" : 0.,
            "population" : 0.,
            "max_iters" : 0.
        }


def bbo(objfunc,
        lower_bound,
        upper_bound,
        dim,            # Number of dimensions
        n_population,   # Population size
        max_iters,      # Number of generations
        pmutate = 1e-2, #
        elite = 2        #
        ):
  # Initializing arrays
  walk = np.empty(shape=(max_iters,), dtype=float)
  pos = np.random.uniform(low=lower_bound,
                          high=upper_bound,
                          size=(n_population, dim))
  mut = np.linspace(n_population, 1., n_population) / (n_population + 1)
  lambda1t = (1. - mut).reshape((n_population, 1))
  smu = sum(mut)
  cmu = np.cumsum(mut)

  print ("BBO is optimizing \"" + objfunc.__name__ + "\"")
  solution["optimizer"]  = "BBO"
  solution["dimension"]  = dim,
  solution["population"] = n_population
  solution["max_iters"]  = max_iters
  solution["objfname"]   = objfunc.__name__
  solution["start_time"] = time.time()

  # compute objective function for each particle
  fitness = np.apply_along_axis(objfunc, 1, pos)
  idx = np.argsort(fitness)
  pos = pos[idx, :]
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
    fitness = np.apply_along_axis(objfunc, 1, new_pos)
    pos = new_pos

    idx = np.argsort(fitness)
    pos[idx[-elite:], :] = elite_pos
    fitness[idx[-elite:]] = elite_cos

    idx = np.argsort(fitness)
    pos = pos[idx, :]
    fitness = fitness[idx]

    # Update convergence curve
    walk[t] = fitness[0]
    sys.stdout.write('\r')
    sys.stdout.write("It %-5d: [%-25s] %.3f %.3f sec"
                     %(t,
                       '=' * int(t / 20),
                       fitness[0],
                       time.time() - solution["start_time"]))
  sys.stdout.write('\n')
  solution["end_time"] = time.time()
  solution["run_time"] = solution["end_time"] - solution["start_time"]
  solution["walk"]     = walk
  solution["best"]     = fitness[0]


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

  bbo(score_func,
      lower_bound,
      upper_bound,
      dim,
      n_population,
      max_iters)