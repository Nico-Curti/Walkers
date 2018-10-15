#!usr/bin/python

# Reference :

import numpy as np
import time
import sys
import sklearn.preprocessing as sk

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


def mvo(objfunc,
        lower_bound,
        upper_bound,
        dim,          # Number of dimensions
        n_population, # Population size
        max_iters,    # Number of generations
        wep_max = 1., #
        wep_min = .2  #
        ):
  # Initializing arrays
  walk = np.empty(shape=(max_iters,), dtype=float)
  universes = np.random.uniform(low=lower_bound,
                                high=upper_bound,
                                size=(dim, n_population))

  tdrt = [1. - i**.16666 / max_iters**.1666 for i in range(max_iters)]
  wept = np.linspace(wep_min, wep_max, num=max_iters)

  score = np.inf
  pos = np.zeros(shape=(1, dim), dtype=float)

  print ("MVO is optimizing \"" + objfunc.__name__ + "\"")
  solution["optimizer"]  = "MVO"
  solution["dimension"]  = dim,
  solution["population"] = n_population
  solution["max_iters"]  = max_iters
  solution["objfname"]   = objfunc.__name__
  solution["start_time"] = time.time()

  # main loop
  for (t, wep), tdr in zip(enumerate(wept), tdrt):
    universes = np.clip(universes, lower_bound, upper_bound)
    fitness = np.apply_along_axis(objfunc, 0, universes)

    # Update the leader
    idx = np.argmin(fitness)
    if fitness[idx] < score:
      leader_score = fitness[idx]
      leader_pos   = np.array(pos[:, idx], ndmin=2).T

    n = sk.normalize(fitness.reshape((1, -1)), norm='l2', axis=1)

    # Update convergence curve
    walk[t] = leader_score
    sys.stdout.write('\r')
    sys.stdout.write("It %-5d: [%-25s] %.3f %.3f sec"
                     %(t,
                       '=' * int(t / 20),
                       score,
                       time.time() - solution["start_time"]))
  sys.stdout.write('\n')
  solution["end_time"] = time.time()
  solution["run_time"] = solution["end_time"] - solution["start_time"]
  solution["walk"]     = walk
  solution["best"]     = score


if __name__ == "__main__":
  # F10
  score_func = lambda x: -20. * np.exp(-.2 * np.sqrt(sum(x*x) / len(x)))  \
                         - np.exp(sum(np.cos(2. * np.pi * x)) / len(x))   \
                         + 22.718281828459045

  n_population = 50
  max_iters = 500
  lower_bound = -32
  upper_bound = 32
  dim = 30

  mvo(score_func,
      lower_bound,
      upper_bound,
      dim,
      n_population,
      max_iters)
