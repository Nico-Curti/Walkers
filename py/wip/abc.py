#!usr/bin/python

# Reference :
#https://it.mathworks.com/matlabcentral/fileexchange/52966-artificial-bee-colony-abc-in-matlab

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
        max_trials=100, # abandonment limit parameter (trial limit)
        a=1.            # acceleration coeff upper bound
        ):
  # Initializing arrays
  walk = np.empty(shape=(max_iters,), dtype=float)
  pos = np.random.uniform(low=lower_bound,
                          high=upper_bound,
                          size=(n_population, dim))
  trials = np.zeros(shape=(n_population,), dtype=int)
  employers = n_population // 2

  print ("ABC is optimizing \"" + objfunc.__name__ + "\"")
  solution["optimizer"]  = "ABC"
  solution["dimension"]  = dim,
  solution["population"] = n_population
  solution["max_iters"]  = max_iters
  solution["objfname"]   = objfunc.__name__
  solution["start_time"] = time.time()

  fitness = np.apply_along_axis(objfunc, 1, pos)
  best = np.argmin(fitness)
  fmin = fitness[best]
  best = pos[best, :]

  # main loop
  for t in range(max_iters):
    # the first half are employeeBee
    trial, = np.nonzero(trials[:employers] <= max_trials)
    component = np.array([np.random.choice(p) for p in pos[trial]], ndmin=2).T
    phi = np.random.uniform(low=-a, high=a, size=(trial.size, dim))
    new_pos = pos[trial] + (pos[trial] - component) * phi
    new_pos = np.clip(new_pos, lower_bound, upper_bound)
    new_fit = np.apply_along_axis(objfunc, 1, new_pos)

    # update employeeBee
    idx, = np.nonzero(new_fit < fitness[:employers])
    pos[trial[idx]] = new_pos[idx]
    trials[:employers][idx] = 0
    trials[:employers][~idx] += 1

    # update_optimal_solution
    idx = np.argmin(new_fit)

    if fmin > new_fit[idx]:
      fmin = new_fit[idx]
      best = pos[idx]

    # compute probabilities
    prob = np.exp(-new_fit / np.mean(new_fit))
    prob /= sum(prob)

    # select best food sources
    rng = np.random.uniform(low=0., high=1., size=(employers,))
    best_food_sources, = np.nonzero(prob > rng)  # to check
    # check
    while not best_food_sources.size:
      best_food_sources, = np.nonzero(prob > np.random.uniform(low=0., high=1., size=(employers,)))

    # the second half are onlookerBee
    candidate = np.random.choice(best_food_sources, size=(employers,)) + employers # wrong
    trial, = np.nonzero(trials[employers:] <= max_trials)
    component = np.array([np.random.choice(p) for p in pos[trial]], ndmin=2).T
    phi = np.random.uniform(low=-a, high=a, size=(trial.size, dim))
    new_pos = pos[candidate][trial] + (pos[candidate][trial] - component) * phi
    new_pos = np.clip(new_pos, lower_bound, upper_bound)
    new_fit = np.apply_along_axis(objfunc, 1, new_pos)

    idx, = np.nonzero(new_fit < fitness[employers:])
    pos[trial[idx]] = new_pos[idx]
    trials[employers:][idx] = 0
    trials[employers:][~idx] += 1

    # scout bee phase
    idx, = np.nonzero(trials >= max_trials)
    if idx.size:
      pos[idx, :] = np.random.uniform(low=lower_bound, high=upper_bound, size=(idx.size, dim))
      fitness[idx] = np.apply_along_axis(objfunc, 1, pos[idx, :])
      trials[idx] = 0

    prob[trials[:employers] >= max_iters] = 0.

    # update optimal solution
    idx = np.argmin(fitness)

    if fmin > fitness[idx]:
      fmin = fitness[idx]
      best = pos[idx]

    # Update convergence curve
    walk[t] = fmin
    print(fmin)
#    sys.stdout.write('\r')
#    sys.stdout.write("It %-5d: [%-25s] %.3f %.3f sec"
#                     %(t,
#                       '=' * int(t / 20),
#                       fmin,
#                       time.time() - solution["start_time"]))
#  sys.stdout.write('\n')
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