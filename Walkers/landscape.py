#!/usr/bin/env python
import numpy as np

# Reference: https://www.sfu.ca/~ssurjano/optimization.html

class ObjectiveFunction(object):
  def __init__(self, name, dim, lower_bound, upper_bound):
    self.__name__ = name
    self.dim = dim
    self.lower_bound = lower_bound
    self.upper_bound = upper_bound

  def evaluate(self, arr):
    pass
  def get_minimum(self):
    pass
  def get_boundary(self):
    pass

class AckleyFunction(ObjectiveFunction):
  a, b, c = 20., .2, np.pi * 2.

  def __init__(self, dim = 2):
    super(AckleyFunction, self).__init__('Ackley', dim, -32.768, 32.768)

  def evaluate(self, arr):
    assert(len(arr) == self.dim)
    return -self.a * np.exp(-self.b * np.sqrt(sum(arr*arr) / self.dim)) - np.exp(sum(np.cos(self.c * arr) / self.dim)) + self.a + 2.718281828459045 # np.exp(1)

  def get_minimum(self):
    return np.repeat(0., repeats=self.dim)

  def get_boundary(self):
    return (self.lower_bound, self.upper_bound)

class BoothFunction(ObjectiveFunction):

  def __init__(self, dim=2):
    assert(dim == 2)
    super(BoothFunction, self).__init__('Booth', dim, -10., 10.)

  def evaluate(self, arr):
    assert(len(arr) == self.dim)
    x, y = arr
    return (x + 2. * y - 7.)**2 + (2. * x + y - 5.)**2

  def get_minimum(self):
    return np.array([1., 3.])

  def get_boundary(self):
    return (self.lower_bound, self.upper_bound)


class BukinN6Function(ObjectiveFunction):
  # x belongs to [-15, -5]
  # y belongs to [-3, 3]
  def __init__(self, dim=2):
    assert(dim == 2)
    super(BukinN6Function, self).__init__('BukinN6', dim, -15, 3)

  def evaluate(self, arr):
    assert(len(arr) == self.dim)
    x, y = arr
    return 100. * np.sqrt(abs(y - 1e-2*x*x)) + 1e-2 * abs(y + 10.)

  def get_minimum(self):
    return np.array([-10., 1.])

  def get_boundary(self):
    return (self.lower_bound, self.upper_bound)


class CrossInTrayFunction(ObjectiveFunction):

  def __init__(self, dim=2):
    assert(dim == 2)
    super(CrossInTrayFunction, self).__init__('CrossInTray', dim, -10, 10)

  def evaluate(self, arr):
    assert(len(arr) == self.dim)
    x, y = arr
    return -1e-4 * (abs(np.sin(x)*np.sin(y)*np.exp(abs(100. - np.sqrt(sum(arr*arr)) / np.pi)) ) + 1.)**1e-1

  def get_minimum(self):
    return np.array([ (1.3491, -1.3491), (1.3491, 1.3491), (-1.3491, 1.3491), (-1.3491, -1.3491) ])

  def get_boundary(self):
    return (self.lower_bound, self.upper_bound)


class DixonPriceFunction(ObjectiveFunction):

  def __init__(self, dim):
    super(DixonPriceFunction, self).__init__('DixonPrice', dim, -10., 10.)

  def evaluate(self, arr):
    assert(len(arr) == self.dim)
    idx = np.arange(2., self.dim + 1.)
    return (arr[0] - 1.)**2 + sum(idx * (2. * arr[1:]**2 - arr[:-1]) ** 2)

  def get_minimum(self):
    idx = 2.**(np.arange(1., self.dim + 1.))
    return 2.**(-(idx - 2)/idx)

  def get_boundary(self):
    return (self.lower_bound, self.upper_bound)


class DropWaveFunction(ObjectiveFunction):

  def __init__(self, dim=2):
    assert(dim == 2)
    super(DropWaveFunction, self).__init__('DropWave', dim, -5.12, 5.12)

  def evaluate(self, arr):
    assert(len(arr) == self.dim)
    x, y = arr
    a2 = sum(arr * arr)
    return - (1. + np.cos(12. * np.sqrt(a2))) / (.5 * a2 + 2.)

  def get_minimum(self):
    return np.repeat(0., repeats=self.dim)

  def get_boundary(self):
    return (self.lower_bound, self.upper_bound)


class EggholderFunction(ObjectiveFunction):

  def __init__(self, dim=2):
    assert(dim == 2)
    super(EggholderFunction, self).__init__('Eggholder', dim, -512, 512)

  def evaluate(self, arr):
    assert(len(arr) == self.dim)
    x, y = arr
    return -(y + 47.)*np.sin(np.sqrt(abs(y + .5*x + 47.))) - x * np.sin(np.sqrt(abs(x - (y + 47.))))

  def get_minimum(self):
    return np.array([512, 404.2319])

  def get_boundary(self):
    return (self.lower_bound, self.upper_bound)

#class GramacyLeeFunction(ObjectiveFunction):
#
#  def __init__(self, dim=1):
#    assert(dim == 1)
#    super(GramacyLeeFunction, self).__init__('GramacyLee', dim, .5, 2.5)
#
#  def evaluate(self, arr):
#    assert(len(arr) == self.dim)
#    return .5 * np.sin(10. * np.pi * arr) / arr + (arr - 1.)**4
#
#  def get_minimum(self):
#    return np.array([None]) # around (.6, -.9)
#
#  def get_boundary(self):
#    return (self.lower_bound, self.upper_bound)


class GrieWankFunction(ObjectiveFunction):

  def __init__(self, dim):
    super(GrieWankFunction, self).__init__('GrieWank', dim, -600., 600.)

  def evaluate(self, arr):
    assert(len(arr) == self.dim)
    return np.sum(arr * arr * .00025) - np.prod(np.cos(arr / np.sqrt(np.arange(1, self.dim + 1)))) + 1.

  def get_minimum(self):
    return np.repeat(0., repeats=self.dim)

  def get_boundary(self):
    return (self.lower_bound, self.upper_bound)

class HolderTableFunction(ObjectiveFunction):

  def __init__(self, dim=2):
    assert(dim == 2)
    super(HolderTableFunction, self).__init__('HolderTable', dim, -10., 10.)

  def evaluate(self, arr):
    assert(len(arr) == self.dim)
    x, y = arr
    return - abs(np.sin(x)*np.cos(y)*np.exp(abs(1. - np.sqrt(sum(arr*arr)) / np.pi)))

  def get_minimum(self):
    return np.array([ (8.05502, 9.66459), (8.05502, -9.66459), (-8.05502, 9.66459), (-8.05502, -9.66459) ])

  def get_boundary(self):
    return (self.lower_bound, self.upper_bound)


class MatyasFunction(ObjectiveFunction):

  def __init__(self, dim=2):
    assert(dim == 2)
    super(MatyasFunction, self).__init__('Matyas', dim, -10., 10.)

  def evaluate(self, arr):
    assert(len(arr) == self.dim)
    x, y = arr
    return .26 * sum(arr*arr) - .48*x*y

  def get_minimum(self):
    return np.zeros(shape=(self.dim,), dtype=float)

  def get_boundary(self):
    return (self.lower_bound, self.upper_bound)


class McCormickFunction(ObjectiveFunction):
  # x belongs to [-1.5, 4]
  # y belongs to [-3., 4]
  def __init__(self, dim=2):
    assert(dim == 2)
    super(McCormickFunction, self).__init__('McCormick', dim, -3., 4.)

  def evaluate(self, arr):
    assert(len(arr) == self.dim)
    x, y = arr
    return np.sin(sum(arr)) + (x - y)**2 - 1.5*x + 2.5*y + 1.

  def get_minimum(self):
    return np.array([-.54719, -1.54719])

  def get_boundary(self):
    return (self.lower_bound, self.upper_bound)


# class LangermannFunction(ObjectiveFunction):
#   self.m, self.c = 5., np.array([1., 2., 5., 2., 3.])
#   self.A = np.array([ [3., 5.],
#                       [5., 2.],
#                       [2., 1.],
#                       [1., 4.],,
#                       [7., 9.]
#                     ])
#
#   def __init__(self, dim):
#     assert(dim == 2)
#     super(LangermannFunction, self).__init__('Langermann', dim, 0., 10.)
#
#   def evaluate(self, arr):
#     assert(len(x) == self.dim)
#     return np.sum(c * np.exp(  ) * np.cos(np.pi * ) )
#
#   def get_minimum(self):
#     return np.repeat(None, repeats=self.dim) # ignored
#
#   def get_boundary(self):
#     return (self.lower_bound, self.upper_bound)


class LevyFunction(ObjectiveFunction):

  def __init__(self, dim):
    super(LevyFunction, self).__init__('Levy', dim, -10., 10.)

  def evaluate(self, arr):
    assert(len(arr) == self.dim)
    w = 1. + (arr - 1.) * .25
    return np.sin(np.pi * w[0])**2 +  \
           np.sum( (w[:-1] - 1.)**2 * \
           (1. + 10. * np.sin(np.pi * w[:-1] + 1.)**2) ) + \
           (w[-1] - 1.)**2 * (1. + np.sin(2.*np.pi * w[-1])**2)

  def get_minimum(self):
    return np.ones(shape=(self.dim,), dtype=float)

  def get_boundary(self):
    return (self.lower_bound, self.upper_bound)


class LevyN13Function(ObjectiveFunction):

  def __init__(self, dim=2):
    assert(dim == 2)
    super(LevyN13Function, self).__init__('LevyN13', dim, -10., 10.)

  def evaluate(self, arr):
    assert(len(arr) == self.dim)
    x, y = arr
    return np.sin(3. * np.pi * x)**2 + (x - 1.)**2 * (1. + np.sin(3. * np.pi * y)**2) + (y - 1.)**2 * (1. + np.sin(2. * np.pi * y)**2)

  def get_minimum(self):
    return np.repeat(1., repeats=self.dim)

  def get_boundary(self):
    return (self.lower_bound, self.upper_bound)


# class PowerSumFunction(ObjectiveFunction):
#   self.b = np.array([8., 18., 44., 114.], dtype=float)
#
#   def __init__(self, dim):
#     assert(dim == 4)
#     super(PowerSumFunction, self).__init__('PowerSum', dim, 0., dim)
#
#   def evaluate(self, arr):
#     assert(len(arr) == self.dim)
#     return sum(  )
#
#   def get_minimum(self):
#     return np.repeat(None, repeats=self.dim) # ignore
#
#   def get_boundary(self):
#     return (self.lower_bound, self.upper_bound)


class RastringFunction(ObjectiveFunction):

  def __init__(self, dim):
    super(RastringFunction, self).__init__('Rastring', dim, -5.12, 5.12)

  def evaluate(self, arr):
    assert(len(arr) == self.dim)
    return 10. * self.dim + sum(arr*arr - 10. * np.cos(2*np.pi*arr))

  def get_minimum(self):
    return np.zeros(shape=(self.dim,), dtype=float)

  def get_boundary(self):
    return (self.lower_bound, self.upper_bound)


class RosenbrockFunction(ObjectiveFunction):

  def __init__(self, dim):
    super(RosenbrockFunction, self).__init__('Rosenbrock', dim, -5., 10.)

  def evaluate(self, arr):
    assert(len(arr) == self.dim)
    return sum( 100. * (arr[1:] - arr[:-1]*arr[:-1])**2 + (arr[:-1] - 1.)**2)

  def get_minimum(self):
    return np.ones(shape=(self.dim,), dtype=float)

  def get_boundary(self):
    return (self.lower_bound, self.upper_bound)


class SchafferN2Function(ObjectiveFunction):

  def __init__(self, dim=2):
    assert(dim == 2)
    super(SchafferN2Function, self).__init__('SchafferN2', dim, -100., 100.)

  def evaluate(self, arr):
    assert(len(arr) == self.dim)
    x, y = arr
    return .5 * (np.sin(x*x - y*y) - .5) / (1. + 1e-3*(x*x + y*y))**2

  def get_minimum(self):
    return np.zeros(shape=(self.dim,), dtype=float)

  def get_boundary(self):
    return (self.lower_bound, self.upper_bound)


class SchafferN4Function(ObjectiveFunction):

  def __init__(self, dim=2):
    assert(dim == 2)
    super(SchafferN4Function, self).__init__('SchafferN4', dim, -100., 100.)

  def evaluate(self, arr):
    assert(len(arr) == self.dim)
    x, y = arr
    return .5 + (np.cos(np.sin(abs(x*x - y*y))) - .5) / (1. + 1e-3*(x*x + y*y))**2

  def get_minimum(self):
    return np.repeat(None, repeats=self.dim)#np.zeros(shape=(self.dim,), dtype=float)

  def get_boundary(self):
    return (self.lower_bound, self.upper_bound)


class SchwefelFunction(ObjectiveFunction):

  def __init__(self, dim):
    super(SchwefelFunction, self).__init__('Schwefel', dim, -500., 500.)

  def evaluate(self, arr):
    assert(len(arr) == self.dim)
    return 418.9829 * self.dim - np.sum(arr * np.sin(np.sqrt(abs(arr))))

  def get_minimum(self):
    return np.repeat(420.9687, repeats=self.dim)

  def get_boundary(self):
    return (self.lower_bound, self.upper_bound)

class ShubertFunction(ObjectiveFunction):

  def __init__(self, dim=2):
    assert(dim == 2)
    super(ShubertFunction, self).__init__('Shubert', dim, -10., 10.)

  def evaluate(self, arr):
    assert(len(arr) == self.dim)
    x, y = arr
    idx = np.arange(1., 6.)

    return np.sum(idx * np.cos( (idx + 1.)*x + idx )) * np.sum(idx * np.cos( (idx + 1.)*y + idx ))

  def get_minimum(self):
    return np.repeat(None, repeats=self.dim)#np.zeros(shape=(self.dim,), dtype=float)

  def get_boundary(self):
    return (self.lower_bound, self.upper_bound)


class SixHumpCamelFunction(ObjectiveFunction):
  # x belongs to [-3, 3]
  # y belongs to [-2, 2]
  def __init__(self, dim=2):
    assert(dim == 2)
    super(SixHumpCamelFunction, self).__init__('SixHumpCamel', dim, -3., 3.)

  def evaluate(self, arr):
    assert(len(arr) == self.dim)
    x, y = arr
    return x**2 * (4. - 2.1 * x**2 + x**4 / 3.) + x*y + (-4. + 4.*y**2)*y**2

  def get_minimum(self):
    return np.array([(.0898, -.7126), (-.0898, .7126)])

  def get_boundary(self):
    return (self.lower_bound, self.upper_bound)


class ThreeHumpCamelFunction(ObjectiveFunction):

  def __init__(self, dim=2):
    assert(dim == 2)
    super(ThreeHumpCamelFunction, self).__init__('ThreeHumpCamel', dim, -5., 5.)

  def evaluate(self, arr):
    assert(len(arr) == self.dim)
    x, y = arr
    return 2. * x**2 - 1.05 * x**4 + x**6 / 6. + x * y + y**2

  def get_minimum(self):
    return np.zeros(shape=(self.dim,), dtype=float)

  def get_boundary(self):
    return (self.lower_bound, self.upper_bound)


class ZakharovFunction(ObjectiveFunction):

  def __init__(self, dim):
    super(ZakharovFunction, self).__init__('Zakharov', dim, -5., 10.)

  def evaluate(self, arr):
    assert(len(arr) == self.dim)
    idx = np.arange(1., self.dim + 1.)
    return sum(arr*arr) + sum(.5 * idx * arr)**2 + sum(.5 * idx * arr)**4

  def get_minimum(self):
    return np.zeros(shape=(self.dim,), dtype=float)

  def get_boundary(self):
    return (self.lower_bound, self.upper_bound)




if __name__ == '__main__':

  from mpl_toolkits.mplot3d import Axes3D
  import matplotlib.pylab as plt
  from matplotlib import cm
  from matplotlib.ticker import LinearLocator, FormatStrFormatter

  import sys, inspect
  functions = [m[0] for m in
               inspect.getmembers(sys.modules[__name__], inspect.isclass)
               if m[1].__module__ == '__main__'
               and m[0] != 'ObjectiveFunction'
               and m[0][0] != '_']


  func = eval(functions[1])(dim=2)

  Nstep = 100
  lb = func.lower_bound
  ub = func.upper_bound
  x = np.linspace(lb, ub, Nstep)
  x, y = np.meshgrid(x, x)
  z = np.asarray([[i, j] for i, j in zip(x.ravel(), y.ravel())])
  z = list(map(func.evaluate, z))
  z = np.asarray(z).reshape((Nstep, Nstep))
  m_z = np.min(z)
  M_z = np.max(z)


  fig = plt.figure(figsize=(10, 8))
  fig.subplots_adjust(top=.9, bottom=.1, left=.1, right=.9)
  ax = fig.gca(projection='3d')

  surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm,
                         linewidth=0, antialiased=False, alpha=.5)

  minimum = func.get_minimum()
  if len(minimum.shape) > 1:
    for m in minimum:
      min_line = ax.scatter(m[0], m[1], func.evaluate(m), c='r', s=50)
  else:
    min_line = ax.scatter(minimum[0], minimum[1], func.evaluate(minimum), c='r', s=50)

  ax.zaxis.set_major_locator(LinearLocator(10))
  ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

  ax.set_title(func.__name__, fontsize=14, fontweight='bold')
  ax.set_xlabel("x", fontsize=14)
  ax.set_ylabel("y", fontsize=14)
  ax.set_zlabel(func.__name__+"(x, y)", fontsize=14)

  fig.colorbar(surf , shrink=.5, aspect=5)
  plt.show()
