#!usr/bin/python

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

    self.walk       = []
    self.population = []
