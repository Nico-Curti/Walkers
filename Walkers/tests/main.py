#!/usr/bin/env python

from Walkers import landscape
import Walkers.optimizers as opt

import argparse
import sys


if __name__ == '__main__':

  description = "Walkers test example"
  parser = argparse.ArgumentParser(description = description)
  parser.add_argument('-n', required=False, dest='n_population', action='store', help='Population size',          default=50)
  parser.add_argument('-i', required=False, dest='max_iters',    action='store', help='Max number of iterations', default=500)
  parser.add_argument('-d', required=False, dest='dim',          action='store', help='Dimension of the problem', default=2)
  parser.add_argument('-v', required=False, dest='view',         action='store', help='Able/Disable viewer',      default=False)
  parser.add_argument('-p', required=False, dest='parameters',   action='store', help='Optimizer parameters',     default='dict()')
  parser.add_argument('-l', required=True,  dest='landscape',    action='store', help='Landscape name to test')
  parser.add_argument('-o', required=True,  dest='optimizer',    action='store', help='Optimizer name to test')

  if len(sys.argv) <= 3:
    parser.print_help()
    sys.exit(1)
  else:
    args = parser.parse_args()

  n_population = int(args.n_population)
  max_iters    = int(args.max_iters)
  dim          = int(args.dim)
  function     = args.landscape
  optimizer    = args.optimizer
  view         = bool(int(args.view))
  parameters   = eval(args.parameters)

  functions = [m for m in dir(landscape) if m.endswith('Function') and m != 'ObjectiveFunction']
  try:
    function = eval('landscape.' + function + '(dim = %d)'%dim)
  except Exception:
    print('Wrong landscape function name! Possible values are only: ')
    print('- ', end='')
    print(*functions, sep='\n- ', end='\n', flush=True)
    exit(1)

  optimizers = [m for m in dir(opt) if not m.startswith('__')]
  try:
    optimizer = eval('opt.' + optimizer)
  except Exception:
    print('Wrong optimizer name! Possible values are only:')
    print('- ', end='')
    print(*optimizers, sep='\n- ', end='\n', flush=True)
    exit(1)

  lower_bound, upper_bound = function.get_boundary()

  sol = optimizer(
                  objfunc      = function,
                  dim          = dim,
                  lower_bound  = lower_bound,
                  upper_bound  = upper_bound,
                  n_population = n_population,
                  max_iters    = max_iters,
                  **parameters
                  )

  if dim != 2 and view:
    raise UserWarning('The viewer option can be set only for dim = 2')
    view = False

  if view:

    import numpy as np

    walk = np.asarray(sol.walk)

    import matplotlib.pylab as plt

    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator, FormatStrFormatter

    Nstep = 100
    x = np.linspace(lower_bound, upper_bound, Nstep)
    x, y = np.meshgrid(x, x)
    z = np.asarray([[i, j] for i, j in zip(x.ravel(), y.ravel())])
    z = list(map(function.evaluate, z))
    z = np.asarray(z).reshape((Nstep, Nstep))
    m_z = np.min(z)
    M_z = np.max(z)

    fig = plt.figure(figsize=(10, 8))
    fig.subplots_adjust(top=.9, bottom=.1, left=.1, right=.9)
    ax = fig.gca(projection='3d')

    surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False, alpha=.5)

    fitness_walk = [function.evaluate(w) for w in walk]
    walk_step = ax.plot(walk[:, 0], walk[:, 1], fitness_walk, color='k', linewidth=2, alpha=.8)

    minimum = function.get_minimum()
    if len(minimum.shape) > 1:
      for m in minimum:
        min_line = ax.scatter(m[0], m[1], function.evaluate(m), c='r', s=50)
    else:
      min_line = ax.scatter(minimum[0], minimum[1], function.evaluate(minimum), c='r', s=50)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    ax.set_title(function.__name__, fontsize=14, fontweight='bold')
    ax.set_xlabel("x", fontsize=14)
    ax.set_ylabel("y", fontsize=14)
    ax.set_zlabel(function.__name__+"(x, y)", fontsize=14)

    fig.colorbar(surf , shrink=.5, aspect=5)
    plt.show()
