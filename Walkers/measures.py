#!/usr/bin/env python

# References : https://stackoverflow.com/questions/34222272/computing-mean-square-displacement-using-python-and-fft

import numpy as np

class Measures(object):

  def __init__(self, coords, stat_min = 10):
    self.npt, self.dim = coords.shape

  def compute_velocity(self, coords):
    self.velocity = np.apply_along_axis(np.diff, 1, coords)

  def compute_etavacf(self, velocity, stat_min):
    nt0, nx = velocity.shape
    ntau    = nt0 - stat_min
    self.etavacf = None # TODO

  def compute_tavacf(self, velocity, stat_min):
    nt0, nx = velocity.shape
    ntau    = nt0 - stat_min
    self.tavacf = None # TODO

  def compute_eavacf(self, velocity, stat_min):
    nt0, nx = velocity.shape
    ntau    = nt0 - stat_min
    self.eavacf = None # TODO

  def compute_etamsd(self, coords, stat_min):
    nt0, nx = coords.shape
    ntau    = nt0 - stat_min
    self.etamsd = None # TODO

  def compute_eamsd(self, coords, stat_min):
    nt0, nx = coords.shape
    ntau    = nt0 - stat_min
    self.eamsd = None # TODO

  def compute_tamsd(self, coords, stat_min):
    nt0, nx = coords.shape
    ntau    = nt0 - stat_min
    self.tamsd = None # TODO

  def compute_etav(self, velocity, stat_min):
    nt0, nx = velocity.shape
    ntau    = nt0 - stat_min
    self.etav = None # TODO

  def compute_tav(self, velocity, stat_min):
    nt0, nx = velocity.shape
    ntau    = nt0 - stat_min
    self.tav = None # TODO

  def compute_eav(self, velocity, stat_min):
    nt0, nx = velocity.shape
    ntau    = nt0 - stat_min
    self.eav = None # TODO

  def autocorrFFT(x):
    N = len(x)
    F = np.fft.fft(x, n=2*N)  #2*N because of zero-padding
    PSD = F * F.conjugate()
    res = np.fft.ifft(PSD)
    res = (res[:N]).real   #now we have the autocorrelation in convention B
    n   = np.linspace(1./N, 1, num=N) #divide res(m) by (N-m)
    return res * n #this is the autocorrelation in convention A

  def msd_fft(r):
    N  = len(r)
    D  = np.square(r).sum(axis=1)
    D  = np.append(D,0)
    S2 = sum([autocorrFFT(r[:, i]) for i in range(r.shape[1])])
    Q  = 2.*D.sum()
    S1 = np.empty(shape=(N,))
    for m in range(N):
      norm  = 1. / (N - m)
      Q     = Q - D[m - 1] - D[N - m]
      S1[m] = Q * norm
    return S1 - 2.*S2

  def __repr__(self):
    class_name = self.__class__.__name__
    return '<%s Class>'%(class_name)

  def __str__(self):
    fmt_str  = 'Statistical Measures\n'
    fmt_str += 'Velocity: %s'%(', '.join(map(str, self.velocity)))
    fmt_str += 'Ensemble time average velocity autocorrelation function: %s\n'%(', '.join(map(str, self.etavacf)))
    fmt_str += 'Time average velocity autocorrelation function: %s\n'%(', '.join(map(str, self.tavacf)))
    fmt_str += 'Ensemble average velocity autocorrelation function: %s\n'%(', '.join(map(str, self.eavacf)))
    fmt_str += 'Ensemble time average mean square displacement: %s\n'%(', '.join(map(str, self.etamsd)))
    fmt_str += 'Ensemble average mean square displacement: %s\n'%(', '.join(map(str, self.eamsd)))
    fmt_str += 'Time average mean square displacement: %s\n'%(', '.join(map(str, self.tamsd)))
    fmt_str += 'Ensemble time average velocity: %s\n'%(', '.join(map(str, self.etav)))
    fmt_str += 'Time average velocity: %s\n'%(', '.join(map(str, self.tav)))
    fmt_str += 'Ensemble average velocity: %s\n'%(', '.join(map(str, self.eav)))
    return fmt_str


if __name__ == '__main__':

  np.random.seed(42)

  N = 1024
  dim = 3
  coords = np.random.uniform(low=0., high=1., size=(n_population, dim))
  stat_min = 10

