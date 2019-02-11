#!/usr/bin/env python
import pickle

class Solution:

  def __init__( self,
                dim = -1,
                n_population = -1,
                max_iters = -1,
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

  @classmethod
  def load(self, path):
    with open(path, 'rb') as fp:
      return pickle.load(fp)

  def __getitem__(self, stat):
    var = eval('self.' + str(stat))
    return var

  def __repr__(self):
    class_name = self.__class__.__name__
    return '<%s Class>'%(class_name)

  def __str__(self):
    fmt_str  = 'Solution of %s algorithm\n'%(self.optimizer)
    fmt_str += 'Score function: %s <dim=%d, n_pop=%d>\n'%(self.objfname, self.dim, self.n_population)
    if isinstance(self.best, (list,)):
      fmt_str += 'Best Solution found: %s\n'%(self.best)
    else:
      fmt_str += 'Best Solution found: %.3f\n'%(self.best)
    fmt_str += 'Estimated in %.3f sec (it=%d)\n'%(self.execution_time, self.max_iters)
    return fmt_str



if __name__ == '__main__':

  sol = Solution()
  sol.best = 3.14
  print(sol)
  sol.dump('dummy.sol')

  sol2 = Solution.load('dummy.sol')
  print(sol2)

