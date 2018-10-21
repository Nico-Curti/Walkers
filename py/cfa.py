#!usr/bin/python

# Reference :

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


def cfa(objfunc,
        lower_bound,
        upper_bound,
        dim,          # Number of dimensions
        n_population, # Population size
        max_iters    # Number of generations
        ):
  # Initializing arrays
  walk = np.empty(shape=(max_iters,), dtype=float)
  pos = np.random.uniform(low=lower_bound,
                          high=upper_bound,
                          size=(n_population, dim))

  m = n_population // 4
  g21 = m + 1
  g22 = 2 * m
  g31 = g22 + 1
  g32 = 3 * m
  g41 = g32 + 1

  print ("CFA is optimizing \"" + objfunc.__name__ + "\"")
  solution["optimizer"]  = "CFA"
  solution["dimension"]  = dim,
  solution["population"] = n_population
  solution["max_iters"]  = max_iters
  solution["objfname"]   = objfunc.__name__
  solution["start_time"] = time.time()

  fitness = np.apply_along_axis(objfunc, 1, pos)
  best = np.argmin(fitness)
  fmin = fitness[best]
  best = pos[best, :]

  Rt = np.random.uniform(low=-1.,  high=2., size=(max_iters,))
  Vt = np.random.uniform(low=-1.5, high=1.5, size=(max_iters,))
  Wt = np.random.uniform(low=-1., high=1., size=(max_iters,))

  # main loop
  for (t, R), V, W in zip(enumerate(Rt), Vt, Wt):
    avg_best = np.mean(best)

    pos[:m, :]      = R * pos[:m, :] + (best - pos[:m, :]) # * 1.
    pos[g21:g22, :] = V * (best - pos[g21:g22, :]) + best # * 1.
    pos[g31:g32, :] = W * (best - avg_best) + best # * 1.
    pos[g41:, :]    = np.random.uniform(low=lower_bound,
                                        high=upper_bound,
                                        size=(n_population - g41, dim))

    fitness = np.apply_along_axis(objfunc, 1, pos)
    best = np.argmin(fitness)
    fmin = fitness[best]
    best = pos[best, :]

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
  max_iters = 50
  lower_bound = -32
  upper_bound = 32
  dim = 30

  cfa(score_func,
      lower_bound,
      upper_bound,
      dim,
      n_population,
      max_iters)

