#!/usr/bin/python
"""
@author: NICO

Levy flight simulator
"""

import scipy as sc
import numpy as np
import matplotlib.pyplot as plt

def levy(n, dim, beta):
    num = sc.special.gamma(1. + beta) * sc.sin(sc.pi * beta * .5)
    den = sc.special.gamma((1. + beta)*.5) * beta*2.**((beta-1)*.5)
    sigma_u = (num / den)**(1. / beta)
    u = sc.random.normal(0., sigma_u*sigma_u, size=(n, dim))
    v = sc.random.normal(0., 1., size=(n, dim))
    z = u / (abs(v)**(1. / beta))
    return z


if __name__ == "__main__":

  N = 10000
  l = sc.cumsum(levy(N, 2, 1.85), axis=0)
  l /= np.max(abs(l), axis=0)
  time = sc.cumsum(sc.random.exponential(scale=1., size=(len(l))))

  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  ax.plot(l[:, 0], l[:, 1], time, label='levy flight')
  ax.set_xlim(-1, 1)
  ax.set_ylim(-1, 1)
  ax.set_xlabel("x",    fontsize=14)
  ax.set_ylabel("y",    fontsize=14)
  ax.set_zlabel("time", fontsize=14)
  ax.legend()

