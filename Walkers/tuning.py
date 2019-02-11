#!/usr/bin/env python
from skopt import gp_minimize
import inspect
from .solution import Solution
import Walkers.optimizers as opt

class OptimizeOptimizer(object):

  def __init__(self, optimizer, n_population = 10, max_iters = 100, **params):
    self.opt          = eval('opt.' + optimizer)
    self.n_population = n_population
    self.max_iters    = max_iters
    self.params       = dict(params)

  def evaluate(self, arr):
    sol = self.optimizer(self.objfunc,
                         self.lower_bound,
                         self.upper_bound,
                         self.dim,
                         self.npop,
                         self.mi,
                         *arr,
                         verbose=False
                         )
    return sol.best

  def optimize(self, optimizer, objfunc, bounds, dim = 2, n_population = 50, max_iters = 500):
    self.optimizer = optimizer
    self.objfunc = objfunc
    flags        = inspect.getfullargspec(self.optimizer)
    common_flags = ['objfunc', 'n_population', 'lower_bound', 'upper_bound', 'dim', 'n_population', 'max_iters', 'pos', 'verbose']#, 'seed']
    self.dim_hp = len([i for i in flags.args if i not in common_flags ])
    self.lower_bound, self.upper_bound = self.objfunc.get_boundary()

    self.dim  = dim
    self.npop = n_population
    self.mi   = max_iters

    lower_bound = min([i for i, _ in bounds])
    upper_bound = max([i for _, i in bounds])

    if len(bounds) != self.dim_hp:
      raise Warning("The list of bounds must have the same length of the optimizer's hyperparams")

    self.__name__ = self.optimizer.__name__.upper() + ' hyperparams'
    return self.opt(self,
                    lower_bound,
                    upper_bound,
                    self.dim_hp,
                    self.n_population,
                    self.max_iters,
                    **self.params
                    )


class BayesianOptimizer(object):

  def __init__(self, acq_func='EI', n_calls=15, n_random_starts=5, noise=.1**2, seed=123):
    self.acq_func = acq_func
    self.n_calls  = n_calls
    self.n_random_starts = n_random_starts
    self.noise    = noise
    self.seed     = seed

  def optimize(self, optimizer, objfunc, bounds, dim = 2, n_population = 50, max_iters = 500):
    lower_bound, upper_bound = objfunc.get_boundary()

    dim          = objfunc.dim

    def call_optimizer(hyperparams):
      sol = optimizer(objfunc,
                      lower_bound,
                      upper_bound,
                      dim,
                      n_population,
                      max_iters,
                      *hyperparams,
                      seed=123,
                      verbose=False)
      return sol.best

    res = gp_minimize(lambda hyperparams : call_optimizer(hyperparams),
                      bounds,
                      acq_func = self.acq_func,
                      n_calls  = self.n_calls,
                      n_random_starts = self.n_random_starts,
                      noise    = self.noise,
                      random_state = self.seed,
                      verbose=True
                      )
    sol = Solution( dim = len(bounds),
                    n_population = self.n_calls,
                    max_iters = self.n_random_starts,
                    optimizer = res['models'][0],
                    objfname = optimizer.__name__ + '_' + objfunc.__name__
                   )
    sol.best = res['x']
    sol.walk = res['x_iters']
    return sol




if __name__ == '__main__':

  from landscape import AckleyFunction

  n_population = 5
  max_iters = 100
  dim = 2
  score_func = AckleyFunction(dim=dim)

  optimizer = opt.bat
  Opt = BayesianOptimizer()
  bayesian_res = Opt.optimize(optimizer,
                              score_func,
                              bounds    = [(0., 1.),     # domain of A
                                           (0., 1.),     # domain of r
                                           (0., 1.),     # domain of Qmin
                                           (1., 3.),     # domain of Qmax
                                           (1e-3, 1e-1)  # domain of step
                                           ]
                              )

  Opt = OptimizeOptimizer('pso',
                          n_population,
                          max_iters
                          )
  Opt.optimize(optimizer,
               score_func,
               bounds    = [(0., 1.),     # domain of A
                            (0., 1.),     # domain of r
                            (0., 1.),     # domain of Qmin
                            (1., 3.),     # domain of Qmax
                            (1e-3, 1e-1), # domain of step
                            (0, 123456789) # domain of seed
                            ],
               n_population = 10,
               max_iters    = 50
               )

