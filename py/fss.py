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


def fss(objfunc,
        lower_bound,
        upper_bound,
        dim,            # Number of dimensions
        n_population,   # Population size
        max_iters,      # Number of generations
        step=.1,        #
        fstep=1e-4,     #
        step_volitive=1e-2, #
        fstep_volitive=1e-3,
        min_w=1.,       #
        w_scale=2.   #
        ):
  # Initializing arrays
  walk = np.empty(shape=(max_iters,), dtype=float)
  pos = np.random.uniform(low=lower_bound,
                          high=upper_bound,
                          size=(dim, n_population))
  weight = np.repeat(w_scale * .5, repeats=n_population)
  curr_w = sum(weight)
  domain = abs(upper_bound - lower_bound)

  steps = np.linspace(step, fstep, num=max_iters) * domain
  volitives = np.linspace(step_volitive, fstep_volitive, num=max_iters) * domain

  print ("FSS is optimizing \"" + objfunc.__name__ + "\"")
  solution["optimizer"]  = "FSS"
  solution["dimension"]  = dim,
  solution["population"] = n_population
  solution["max_iters"]  = max_iters
  solution["objfname"]   = objfunc.__name__
  solution["start_time"] = time.time()

  fitness = np.apply_along_axis(objfunc, 0, pos)

  # main loop
  for (t, step), volitive in zip(enumerate(steps), volitives):

    # individual_movement
    new_pos = pos + step * np.random.uniform(low=-1., high=1., size=(dim, n_population))
    new_pos = np.clip(new_pos, lower_bound, upper_bound)

    new_fit = np.apply_along_axis(objfunc, 0, new_pos)

    idx, = np.nonzero(new_fit < fitness)

    # feeding
    if idx.size:
      delta_fit = abs(new_fit[idx] - fitness[idx])
      delta_pos = new_pos[:, idx] - pos[:, idx]
      pos[:, idx] = new_pos[:, idx]

      weight[idx] += delta_fit / max(delta_fit)
      weight = np.clip(weight, min_w, w_scale)

    # collective_instinctive_movement
      density  = sum(delta_fit)
      cost_eval_enhanced = np.sum(delta_pos * delta_fit, axis=1)
      cost_eval_enhanced /= density

      pos += cost_eval_enhanced.reshape((-1, 1))
      pos = np.clip(pos, lower_bound, upper_bound)

    # collective_volitive_movement
      tot_w = sum(weight)
      barycenter = np.sum(pos * weight, axis=1).reshape((-1, 1))
      barycenter /= density

    if tot_w > curr_w: pos -= (pos - barycenter) * volitive * np.random.uniform(low=0., high=1., size=(dim, n_population))
    else:              pos += (pos - barycenter) * volitive * np.random.uniform(low=0., high=1., size=(dim, n_population))

    curr_w = tot_w

    pos = np.clip(pos, lower_bound, upper_bound)
    fitness = np.apply_along_axis(objfunc, 0, pos)
    fmin = min(fitness)

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

  fss(score_func,
      lower_bound,
      upper_bound,
      dim,
      n_population,
      max_iters)
