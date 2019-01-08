#!usr/bin/python

# Refence : https://www.sciencedirect.com/science/article/pii/S2214785317313433
#           https://www.cs.tufts.edu/comp/150GA/homeworks/hw3/_reading7%20Cuckoo%20search.pdf

import numpy as np
from scipy.special import gamma
import time
import sys
from ..solution import Solution

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
        beta = 1.5,
        nest = None,
        seed = 0
        ):

  assert(beta < 2. and beta > 1.)

  np.random.seed(seed)

  walk = np.empty(shape=(max_iters, dim), dtype=float)
  sigma = levy_flight(beta)
  beta_inv = 1. / beta

  if nest == None:
    # RInitialize nests randomely
    nest = np.random.uniform(low=lower_bound,
                             high=upper_bound,
                             size=(dim, n_population))
  else:
    nest = nest.T
    assert(nest.shape == 2)
    d, n = nest.shape
    assert(d == dim)
    assert(n == n_population)

  print ("CS is optimizing \"" + objfunc.__name__ + "\"")

  sol = Solution(dim          = dim,
                 n_population = n_population,
                 max_iters    = max_iters,
                 optimizer    = "CS",
                 objfname     = objfunc.__name__,
                 start_time   = time.time()
                 )

  fitness = np.apply_along_axis(objfunc.evaluate, 0, nest)
  best = np.argmin(fitness)
  fmin = fitness[best]
  best = np.array(nest[:, best], ndmin=2).T

  # main loop
  for t in range(max_iters):
    # Generate new solutions (but keep the current best)
    # get_cukoos function
    u = np.random.randn(dim, n_population) * sigma
    v = np.random.randn(dim, n_population)
    step = u / abs(v)**(beta_inv)
    stepsize = 1e-2 * (step * (nest - best))
    s = nest + stepsize * np.random.randn(dim, n_population)
    new_nest = np.clip(s, lower_bound, upper_bound)

    # Evaluate new solutions and find best
    # get_best_nest function
    fit_new  = np.apply_along_axis(objfunc.evaluate, 0, new_nest)
    idx = fit_new <= fitness
    fitness[idx] = fit_new[idx]
    nest[:, idx] = new_nest[:, idx]

    rng = np.random.uniform(low=0., high=1., size=(dim, n_population))
    rng = rng > pa
    new_nest[rng] += np.random.uniform(low=0., high=1., size=(dim, n_population))[rng] * \
                     (                                                                   \
                      new_nest[:, np.random.permutation(n_population)] -                 \
                      new_nest[:, np.random.permutation(n_population)]                   \
                     )[rng]

    # Evaluate new solutions and find best
    # get_best_nest function
    fit_new  = np.apply_along_axis(objfunc.evaluate, 0, new_nest)
    idx = fit_new <= fitness
    fitness[idx] = fit_new[idx]
    nest[:, idx] = new_nest[:, idx]

    tmp_best = np.argmin(fit_new)
    if fit_new[tmp_best] < fmin: # to check
      fmin = fit_new[tmp_best]
      best = np.array(new_nest[:, tmp_best], ndmin=2).T

    # Update convergence curve
    walk[t] = best
    sys.stdout.write('\r')
    sys.stdout.write("It %-5d: [%-25s] %.3f %.3f sec"
                     %(t,
                       '=' * int(t / 20),
                       fmin,
                       time.time() - sol.start_time))
  sys.stdout.write('\n')

  sol.end_time   = time.time()
  sol.run_time   = sol.end_time - sol.start_time
  sol.walk       = walk
  sol.best       = fmin
  sol.population = nest.T

  return sol


if __name__ == "__main__":

  from ..landscape import AckleyFunction as score_func

  n_population = 50
  max_iters = 500
  lower_bound = -32
  upper_bound = 32
  dim = 30

  sol = cs(objfunc = score_func,
           lower_bound = lower_bound,
           upper_bound = upper_bound,
           dim = dim,
           n_population = n_population,
           max_iters = max_iters)
