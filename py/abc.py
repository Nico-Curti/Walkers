#!usr/bin/python

# Reference :

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


def abc(objfunc,
        lower_bound,
        upper_bound,
        dim,            # Number of dimensions
        n_population,   # Population size
        max_iters,      # Number of generations
        max_trials=100
        ):
  # Initializing arrays
  walk = np.empty(shape=(max_iters,), dtype=float)
  pos = np.random.uniform(low=lower_bound,
                          high=upper_bound,
                          size=(n_population, dim))
  employers = n_population // 2

  print ("ABC is optimizing \"" + objfunc.__name__ + "\"")
  solution["optimizer"]  = "ABC"
  solution["dimension"]  = dim,
  solution["population"] = n_population
  solution["max_iters"]  = max_iters
  solution["objfname"]   = objfunc.__name__
  solution["start_time"] = time.time()


  # main loop
  for t in range(max_iters):
    # miss condition
    component = [np.random.choice(p) for p in pos[:employers]]
    phi = np.random.uniform(low=-1., high=1., size=(employers, dim))
    new_pos = pos[:employers] + (pos[:employers] - component) * phi
    new_pos = np.clip(new_pos, lower_bound, upper_bound)

    new_fit = np.apply_along_axis(objfunc, 1, new_pos)

    idx = new_fit < fitness
    pos[idx, :employers] = new_pos[idx]

    # compute proba
    new_fit /= sum(new_fit)


    # scout_bees_phase
    # miss condition
    pos = np.random.uniform(low=lower_bound,
                            high=upper_bound,
                            size=(n_population, dim))
    trial = np.zeros(shape=(n_population))
    prob  = np.zeros(shape=(n_population))
    fitness = np.apply_along_axis(objfunc, 1, pos)


    # update_optimal_solution
    best = np.argmin(fitness)
    fmin = fitness[best]
    #best = pos[best]

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

  abc(score_func,
      lower_bound,
      upper_bound,
      dim,
      n_population,
      max_iters)