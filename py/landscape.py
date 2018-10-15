#!usr/bin/python
import numpy as np

Ufunc = lambda x, a, k, m : k * (x - a)**m * (x > a) + k * (-x - a)**m * (x < -a)

F1  = lambda x : np.sum(x * x)
F2  = lambda x : np.sum(abs(x)) + np.prod(abs(x))
F3  = lambda x : np.cumsum(x)**2
F4  = lambda x : np.max(abs(x))
F5  = lambda x : np.sum(1e2 * (x[1:-1] - (x[:-2]**2))**2 + (x[:-2] - 1.)**2)
F6  = lambda x : np.sum(abs(x + .5)**2)
F7  = lambda x : np.sum(np.arange(1, len(x) + 1) * x*x*x*x) + np.random.uniform(low=0., high=1.)
F8  = lambda x : np.sum(-x * np.sim(np.sqrt(abs(x))))
F9  = lambda x : np.sum(x*x - 10. * np.cos(2. * np.pi * x)) + 10. * len(x)
F10 = lambda x : -20. * np.exp(-.2 * np.sqrt(np.mean(x*x))) - np.exp(np.mean(np.cos(2. * np.pi * x))) + 22.718281828459045
F11 = lambda x : np.sum(x * x) / 4e3 - np.prod(np.cos(x / np.sqrt(np.arange(1, len(x)+1)))) + 1.

F12 = lambda x : np.pi / len(x) * (10. * ((np.sin(np.pi * (1. + (x[0] + 1.) * .25)))**2) ) #####à

F16 = lambda x : 4. * x[0]*x[0] - 2.1 * x[0]**4 + x[0]**6 * 0.333333333333333 + x[0] * x[1] - 4. * x[1]*x[1] + 4. * x[1]*x[1]*x[1]*x[1]
F17 = lambda x : (x[1] - x[0]*x[0] * 0.12918450914398066 + 5. / np.pi * x[0] - 6.)**2 + 10. * (1. - 1. / (8. * np.pi)) * np.cos(x[0]) + 10.
F18 = lambda x : (1. + (x[:2] + 1.)**2 * (19. - 14. * x[0] + 3. * x[0] * x[0] - 14. * x[1] + 6. * x[:2] + 3. * x[1]*x[1])) * (30. + (2. * x[0] - 3. * x[1])**2 * (18. - 32. * x[0] + 12. * x[0] * x[0] + 48. * x[1] - 36. * x[:2] + 27. * x[1]*x[1]))


if __name__ == '__main__':

  import matplotlib.pylab as plt
