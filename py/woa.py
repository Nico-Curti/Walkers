#!usr/bin/python

# Reference : https://en.wikiversity.org/wiki/Whale_Optimization_Algorithm

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


def woa(objfunc,
        lower_bound,
        upper_bound,
        dim,          # Number of dimensions
        n_population, # Population size
        max_iters,    # Number of generations
        b   = 1.     #
        ):
  # Initializing arrays
  walk = np.empty(shape=(max_iters,), dtype=float)
  pos = np.random.uniform(low=lower_bound,
                          high=upper_bound,
                          size=(dim, n_population))
  # a decreases linearly fron 2 to 0 in Eq. (2.3)
  at = np.linspace(2, 0, num=max_iters)
  # a2 linearly decreases from -1 to -2 to calculate t in Eq. (3.12)
  a2t = np.linspace(-1, -2, num=max_iters)
  leader_score = np.inf
  leader_pos = np.zeros(shape=(1, dim), dtype=float)

  print ("WOA is optimizing \"" + objfunc.__name__ + "\"")
  solution["optimizer"]  = "WOA"
  solution["dimension"]  = dim,
  solution["population"] = n_population
  solution["max_iters"]  = max_iters
  solution["objfname"]   = objfunc.__name__
  solution["start_time"] = time.time()

  # main loop
  for (t, a), a2 in zip(enumerate(at), a2t):
    # Return back the search agents that go beyond the boundaries of the search space
    pos = np.clip(pos, lower_bound, upper_bound)
    # Calculate objective function for each search agent
    fitness = np.apply_along_axis(objfunc, 0, pos)

    # Update the leader
    idx = np.argmin(fitness)
    if fitness[idx] < leader_score:
      leader_score = fitness[idx]
      leader_pos   = np.array(pos[:, idx], ndmin=2).T

    r1 = np.random.uniform(low=0., high=1., size=(n_population,))
    r2 = np.random.uniform(low=0., high=1., size=(n_population,))

    A = 2. * a * r1 - a
    C = 2. * r2
    p = np.random.uniform(low=0., high=1., size=(n_population,)) < .5

    A_condition = abs(A) >= 1.

    idx = np.logical_and(p, A_condition)
    if sum(idx):
      l_idx = np.floor(n_population *
                       np.random.uniform(low=0.,
                                         high=1.,
                                         size=(n_population, ))
                       ).astype(int)
      pos[:, l_idx] = pos[:, l_idx] - A[l_idx] * abs(C * pos[:, l_idx] - pos[:, l_idx])

    idx = np.logical_and(p, ~A_condition)
    pos[:, idx] = leader_pos - A[idx] * abs((C * leader_pos)[:, idx] - pos[:, idx])

    p = ~p
    l = (a2 - 1.) * np.random.uniform(low=0., high=1., size=(n_population,)) + 1.
    l = l[p]
    dist2leader = abs(leader_pos - pos[:, p])
    pos[:, p] = dist2leader * np.exp(b * l) * np.cos(2. * l * np.pi) + leader_pos


    # Update convergence curve
    walk[t] = leader_score
    sys.stdout.write('\r')
    sys.stdout.write("It %-5d: [%-25s] %.3f %.3f sec"
                     %(t,
                       '=' * int(t / 20),
                       leader_score,
                       time.time() - solution["start_time"]))
  sys.stdout.write('\n')
  solution["end_time"] = time.time()
  solution["run_time"] = solution["end_time"] - solution["start_time"]
  solution["walk"]     = walk
  solution["best"]     = leader_score


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

  woa(score_func,
      lower_bound,
      upper_bound,
      dim,
      n_population,
      max_iters)