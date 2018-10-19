#!usr/bin/python

# Reference : https://www.sciencedirect.com/science/article/pii/S0045794913002162
#             https://arxiv.org/pdf/1004.4170.pdf
#             https://www.researchgate.net/publication/258478684_Bat_Algorithm_Inspired_Algorithm_for_Solving_Numerical_Optimization_Problems

# Maybe

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
        step = 1e-3   # scale of normal random generator
        ):
  # Initializing arrays
  Qt = np.random.uniform(low=Qmin, high=Qmax, size=(max_iters, n_population))
  v  = np.zeros(shape=(dim, n_population), dtype=float) # velocities
  walk = np.empty(shape=(max_iters,), dtype=float)

  # Initialize the population/solutions
  Sol = np.random.uniform(low=lower_bound,
                          high=upper_bound,
                          size=(dim, n_population))
  print ("BAT is optimizing \"" + objfunc.__name__ + "\"")
  solution["optimizer"]  = "BAT"
  solution["dimension"]  = dim,
  solution["population"] = n_population
  solution["max_iters"]  = max_iters
  solution["objfname"]   = objfunc.__name__
  solution["start_time"] = time.time()

  fitness = np.apply_along_axis(objfunc, 0, Sol)
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
    fit_new = np.apply_along_axis(objfunc, 0, S)

    # Update if the solution improves
    upd = np.logical_and(rng2, fit_new <= fitness)
    Sol[:, upd] = S[:, upd]
    fitness[upd] = fit_new[upd]

    # check boundaries
    Sol = np.clip(Sol, lower_bound, upper_bound)

    tmp_best = np.argmin(fit_new)
    # Update the current best solution
    if fit_new[tmp_best] <= fmin:
      fmin = fit_new[tmp_best]
      best = np.array(S[:, tmp_best], ndmin=2)
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

  bat(score_func,
      lower_bound,
      upper_bound,
      dim,
      n_population,
      max_iters)
