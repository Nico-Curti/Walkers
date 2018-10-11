#!usr/bin/python

import numpy as np
from scipy.special import gamma
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

levy_flight = lambda beta : ( gamma(1. + beta)      * np.sin(np.pi * beta * .5) / \
                             (gamma((1. + beta)*.5) * beta * 2.**( (beta - 1.) * .5)) \
                             )**(1. / beta)

def cs( objfunc,
        lower_bound,
        upper_bound,
        dim,          # Number of dimensions
        n_population, # Population size
        max_iters,    # Number of generations
        pa = .25,     # discovery rate of alien eggs/solution
        beta = 1.5
        ):

  assert(beta < 2. and beta > 1.)
  walk = np.empty(shape=(max_iters,), dtype=float)
  sigma = levy_flight(beta)
  beta_inv = 1. / beta

  # RInitialize nests randomely
  nest = np.random.uniform(low=lower_bound,
                           high=upper_bound,
                           size=(dim, n_population))

  print ("CS is optimizing \"" + objfunc.__name__ + "\"")
  solution["optimizer"]  = "CS"
  solution["dimension"]  = dim,
  solution["population"] = n_population
  solution["max_iters"]  = max_iters
  solution["objfname"]   = objfunc.__name__
  solution["start_time"] = time.time()

  fitness = np.apply_along_axis(objfunc, 0, nest)
  best = np.argmin(fitness)
  fmin = fitness[best]
  best = np.array(nest[:, best], ndmin=2)

  # main loop
  for t in range(max_iters):
    # Generate new solutions (but keep the current best)
    u = np.random.randn(dim, n_population) * sigma
    v = np.random.randn(dim, n_population)
    step = u / abs(v)**(beta_inv)
    stepsize = 1e-2 * (step * (nest - best))
    s = nest + stepsize * np.random.randn(dim, n_population)
    new_nest = np.clip(s, lower_bound, upper_bound)

    # # Evaluate new solutions and find best
    # fit_new  = np.apply_along_axis(objfunc, 0, new_nest)
    # tmp_best = np.argmin(fit_new)
    # tmp_fmin = fit_new[tmp_best]
    # if tmp_fmin <= fmin: # to check
    #   best = np.array(new_nest[:, tmp_best], ndmin=2)
    #   fmin = tmp_fmin

    rng = np.random.uniform(low=0., high=1., size=(dim, n_population))
    rng = rng > pa
    new_nest[rng] +=

    # Evaluate new solutions and find best
    fit_new  = np.apply_along_axis(objfunc, 0, new_nest)
    tmp_best = np.argmin(fit_new)
    tmp_fmin = fit_new[tmp_best]
    if tmp_fmin <= fmin: # to check
      best = np.array(new_nest[:, tmp_best], ndmin=2)
      fmin = tmp_fmin

    # Update convergence curve
    walk[t] = fmin

    sys.stdout.write('\r')
    sys.stdout.write("It %-5d: [%-25s] %.3f %.3f sec"
                     %(t,
                       '=' * int(t / 20),
                       fmin,
                       time.time() - solution["start_time"]))

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

  cs(score_func,
     lower_bound,
     upper_bound,
     dim,
     n_population,
     max_iters)
