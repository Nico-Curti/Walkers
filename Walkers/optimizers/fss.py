#!/usr/bin/env python

# Reference : "A Novel Search Algorithm based on Fish School Behavior" published in 2008 by Bastos Filho, Lima Neto, Lins, D. O. Nascimento and P. Lima
#             "An Enhanced Fish School Search Algorithm" published in 2013 by Bastos Filho and  D. O. Nascimento

import numpy as np
import time
import sys
from ..solution import Solution

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
        w_scale=2.,     #
        seed = 0,
        pos = None,
        verbose = True
        ):

  np.random.seed(int(seed))

  # Initializing arrays
  walk = np.empty(shape=(max_iters, dim), dtype=float)

  if pos == None:
    pos = np.random.uniform(low=lower_bound,
                            high=upper_bound,
                            size=(dim, n_population))
  else:
    pos = pos.T
    if pos.shape != 2:
      raise Warning('Wrong dimension shape of old generation! Probably you should transpose')
    d, n = pos.shape
    if d != dim or n != n_population:
      raise Warning('Wrong dimension shape of old generation! Number of population or dims incompatible')

  weight = np.repeat(w_scale * .5, repeats=n_population)
  tot_w = w_scale * .5 * n_population # aka sum(weight)
  curr_w = tot_w

  steps = [step - i * (step - fstep) / max_iters for i in range(max_iters)]
  volitives = [step_volitive - i * (step_volitive - fstep_volitive) / max_iters for i in range(max_iters)]

  if verbose:
    print ("FSS is optimizing \"" + objfunc.__name__ + "\"")

  sol = Solution(dim          = dim,
                 n_population = n_population,
                 max_iters    = max_iters,
                 optimizer    = "FSS",
                 objfname     = objfunc.__name__,
                 start_time   = time.time()
                 )

  fitness = np.apply_along_axis(objfunc.evaluate, 0, pos)

  # main loop
  for (t, step), volitive in zip(enumerate(steps), volitives):

    # individual_movement
    new_pos = pos + step * np.random.uniform(low=-1., high=1., size=(dim, n_population))
    new_pos = np.clip(new_pos, lower_bound, upper_bound)

    new_fit = np.apply_along_axis(objfunc.evaluate, 0, new_pos)

    idx, = np.nonzero(new_fit < fitness)

    if idx.size:
      delta_fit = abs(new_fit[idx] - fitness[idx])
      delta_pos = new_pos[:, idx] - pos[:, idx]
      pos[:, idx] = new_pos[:, idx]

    # feeding
      M = max(delta_fit)
      if M:
        weight[idx] += delta_fit / M
      weight = np.clip(weight, min_w, w_scale)

    # collective_instinctive_movement
      density  = sum(delta_fit)
      cost_eval_enhanced = np.sum(delta_pos * delta_fit, axis=1)
      if density:
        cost_eval_enhanced /= density

      pos += cost_eval_enhanced.reshape((-1, 1))
      pos = np.clip(pos, lower_bound, upper_bound)

    # collective_volitive_movement
      tot_w = sum(weight)
      barycenter = np.sum(pos * weight, axis=1).reshape((-1, 1))
      barycenter /= tot_w

    if tot_w > curr_w: pos -= (pos - barycenter) * volitive * np.random.uniform(low=0., high=1., size=(dim, n_population))
    else:              pos += (pos - barycenter) * volitive * np.random.uniform(low=0., high=1., size=(dim, n_population))

    curr_w = tot_w

    pos = np.clip(pos, lower_bound, upper_bound)
    fitness = np.apply_along_axis(objfunc.evaluate, 0, pos)
    best = np.argmin(fitness)
    fmin = fitness[best]
    best = pos[:, best]

    # Update convergence curve
    walk[t] = best
    if verbose:
      sys.stdout.write('\r')
      sys.stdout.write("It %-5d: [%-25s] %.3f %.3f sec"
                       %(t,
                         '█' * int(t / (max_iters/26)) + '-' * (25 - int(t / (max_iters/26))),
                         fmin,
                         time.time() - sol.start_time))
  if verbose:
    sys.stdout.write('\n')

  sol.end_time   = time.time()
  sol.run_time   = sol.end_time - sol.start_time
  sol.walk       = walk
  sol.best       = fmin
  sol.population = pos.T

  return sol

if __name__ == "__main__":

  from ..landscape import AckleyFunction

  n_population = 50
  max_iters = 500
  lower_bound = -32
  upper_bound = 32
  dim = 30
  score_func = AckleyFunction(dim=dim)

  sol = fss(objfunc = score_func,
            lower_bound = lower_bound,
            upper_bound = upper_bound,
            dim = dim,
            n_population = n_population,
            max_iters = max_iters)
