#!/usr/bin/env python
import pickle

class Solution:

  def __init__( self,
                dim = None,
                n_population = None,
                max_iters = None,
                optimizer = "",
                objfname  = "",
                start_time = 0.
              ):
    self.dim            = dim
    self.n_population   = n_population
    self.max_iters      = max_iters
    self.start_time     = start_time
    self.optimizer      = optimizer
    self.objfname       = objfname
    self.best           = 0.
    self.end_time       = 0.
    self.execution_time = 0.

    self.walk           = []
    self.population     = []

  def dump(self, path):
    with open(path, 'wb') as fp:
      pickle.dump(self, fp)

  def load(self, path):
    with open(path, 'rb') as fp:
      self = pickle.load(fp)

  def __repr__(self):
    class_name = self.__class__.__name__
    return '<%s Class>'%(class_name)

  def __str__(self):
    fmt_str  = 'Solution of %s algorithm\n'%(self.optimizer)
    fmt_str += 'Score function: %s <dim=%d, n_pop=%d>\n'%(self.objfname, self.dim, self.n_population)
    fmt_str += 'Best Solution found: %.3f\n'%(self.best)
    fmt_str += 'Estimated in %.3f sec (it=%d)\n'%(self.execution_time, self.max_iters)
    return fmt_str
