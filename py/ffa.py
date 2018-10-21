#!usr/bin/python

# Reference: https://research.ijcaonline.org/volume69/number3/pxc3887528.pdf
#            http://www2.siit.tu.ac.th/bunyarit/publications/2014_Aor_ADCONIP2014_Japan.pdf

import numpy as np
from scipy.spatial.distance import squareform, pdist
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
        gamma = 1.    # Absorption coefficient
        ):
  ns = np.random.uniform(low=lower_bound,
                         high=upper_bound,
                         size=(n_population, dim))
  walk = np.empty(shape=(max_iters,), dtype=float)
  domain = abs(upper_bound - lower_bound)

  print ("FFA is optimizing \"" + objfunc.__name__ + "\"")
  solution["optimizer"] = "FFA"
  solution["dimension"] = dim,
  solution["population"] = n_population
  solution["max_iters"] = max_iters
  solution["objfname"] = objfunc.__name__
  timer = time.time()
  solution["start_time"] = timer

  # main loop
  for t in range(max_iters):
    # This line of reducing alpha is optional
    alpha = new_alpha(alpha, max_iters)
    # Evaluate new solutions (for all n fireflies)
    fitness = np.apply_along_axis(objfunc, 1, ns)

    fmin = min(fitness)

    r = squareform(pdist(ns, "euclidean"))
    lightn, light0 = np.meshgrid(fitness, fitness)
    ii, jj = (light0 > lightn).nonzero()
    # The attractiveness parameter beta=exp(-gamma*r)
    beta = (beta0 - betamin) * np.exp(-gamma * r * r) + betamin

    rng = np.random.uniform(low=-.5 * domain * alpha,
                            high=.5 * domain * alpha,
                            size=(n_population, n_population, dim))
    for i, j, b, r in zip(ii, jj, beta[ii, jj], rng[ii, jj]):
      ns[i, :] = ns[i, :] * (1. - b) + ns[j, :] * b + r

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
  solution["walk"] = walk
  solution["best"] = fmin


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

  ffa(score_func,
      lower_bound,
      upper_bound,
      dim,
      n_population,
      max_iters)