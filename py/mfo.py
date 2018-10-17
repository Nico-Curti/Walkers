#!usr/bin/python

# Reference : https://www.sciencedirect.com/science/article/pii/S0950705115002580

# WRONG

import numpy as np
import time
import sys

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


def mfo(objfunc,
        lower_bound,
        upper_bound,
        dim,          # Number of dimensions
        n_population, # Population size
        max_iters,    # Number of generations
        b = 1.        #
        ):
  # Initializing arrays
  walk = np.empty(shape=(max_iters,), dtype=float)
  positions = np.random.uniform(low=lower_bound,
                                high=upper_bound,
                                size=(dim, n_population))
  at = np.linspace(-1, -2, num=max_iters)
  flames = [np.round(n_population - i*(n_population - 1)/max_iters)
            for i in range(1, max_iters + 1)]

  print ("MFO is optimizing \"" + objfunc.__name__ + "\"")
  solution["optimizer"]  = "MFO"
  solution["dimension"]  = dim,
  solution["population"] = n_population
  solution["max_iters"]  = max_iters
  solution["objfname"]   = objfunc.__name__
  solution["start_time"] = time.time()

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
                       time.time() - solution["start_time"]))
  sys.stdout.write('\n')
  solution["end_time"] = time.time()
  solution["run_time"] = solution["end_time"] - solution["start_time"]
  solution["walk"]     = walk
  solution["best"]     = fmin


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

  mfo(score_func,
      lower_bound,
      upper_bound,
      dim,
      n_population,
      max_iters)
