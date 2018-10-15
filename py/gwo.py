#!usr/bin/python

# Reference : https://www.sciencedirect.com/science/article/pii/S0965997813001853
#             https://www.sciencedirect.com/science/article/pii/S0965997816301260
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


def gwo(objfunc,
        lower_bound,
        upper_bound,
        dim,          # Number of dimensions
        n_population, # Population size
        max_iters    # Number of generations
        ):
  # Initializing arrays
  alpha_score, beta_score, delta_score = np.inf, np.inf, np.inf
  alpha_pos, beta_pos, delta_pos = np.zeros(shape=(dim, n_population), dtype=float), \
                                   np.zeros(shape=(dim, n_population), dtype=float), \
                                   np.zeros(shape=(dim, n_population), dtype=float)
  walk = np.empty(shape=(max_iters,), dtype=float)

  # Initialize the population/solutions
  positions = np.random.uniform(low=lower_bound,
                                high=upper_bound,
                                size=(dim, n_population))
  print ("GWO is optimizing \"" + objfunc.__name__ + "\"")
  solution["optimizer"]  = "GWO"
  solution["dimension"]  = dim,
  solution["population"] = n_population
  solution["max_iters"]  = max_iters
  solution["objfname"]   = objfunc.__name__
  solution["start_time"] = time.time()

  at = np.linspace(2, 0, num=max_iters)
  # main loop
  for t, a in enumerate(at):
    # Return back the search agents that go beyond the boundaries of the search space
    positions = np.clip(positions, lower_bound, upper_bound)
    # compute objective function for each search agent
    fitness = np.apply_along_axis(objfunc, 0, positions)

    # update alpha, beta and delta
    minpos   = np.argmin(fitness)
    if fitness[minpos] < alpha_score:
        alpha_score = fitness[minpos]
        alpha_pos   = np.array(positions[:, minpos], ndmin=2).T
    if fitness[minpos] > alpha_score and \
       fitness[minpos] < beta_score:
        beta_score = fitness[minpos]
        beta_pos   = np.array(positions[:, minpos], ndmin=2).T
    if fitness[minpos] > alpha_score and \
       fitness[minpos] > beta_score  and \
       fitness[minpos] < delta_score:
        delta_score = fitness[minpos]
        delta_pos   = np.array(positions[:, minpos], ndmin=2).T

    r1 = np.random.uniform(low=0., high=1., size=(dim, n_population))
    r2 = np.random.uniform(low=0., high=1., size=(dim, n_population))
    A  = 2. * a * r1 - a
    C  = 2. * r2
    D_alpha = alpha_pos - abs(C * alpha_pos - positions) * A

    r1 = np.random.uniform(low=0., high=1., size=(dim, n_population))
    r2 = np.random.uniform(low=0., high=1., size=(dim, n_population))
    A  = 2. * a * r1 - a
    C  = 2. * r2
    D_beta = beta_pos - abs(C * beta_pos - positions) * A

    r1 = np.random.uniform(low=0., high=1., size=(dim, n_population))
    r2 = np.random.uniform(low=0., high=1., size=(dim, n_population))
    A  = 2. * a * r1 - a
    C  = 2. * r2
    D_delta = delta_pos - abs(C * delta_pos - positions) * A

    positions = (D_alpha + D_beta + D_delta) / 3

    walk[t] = alpha_score

    sys.stdout.write('\r')
    sys.stdout.write("It %-5d: [%-25s] %.3f %.3f sec"
                     %(t,
                       '=' * int(t / 20),
                       alpha_score,
                       time.time() - solution["start_time"]))
  sys.stdout.write('\n')
  solution["end_time"] = time.time()
  solution["run_time"] = solution["end_time"] - solution["start_time"]
  solution["walk"]     = walk
  solution["best"]     = alpha_score


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

  gwo(score_func,
      lower_bound,
      upper_bound,
      dim,
      n_population,
      max_iters)
