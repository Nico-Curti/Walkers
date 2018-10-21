#!/usr/bin/python
"""
@author: NICO

Levy flight convergence
"""

import levy

Ntraj = 5000
Npts  = 1000
target = (.5, .5)
radius = 0.1
res = []
for t in range(Ntraj):
    l = sc.cumsum(levy.levy(Npts, 2, 1.85), axis=0)
    l /= np.max(abs(l), axis=0)
    time = sc.cumsum(sc.random.exponential(scale=1., size=(Npts)))
    tmp = [i for i, (x, y) in enumerate(l) if x >= .4 and y >= .4
                                            and
                                            x <= .6 and y <= .6]
    if len(tmp) != 0: res.append(time[tmp[0]])

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))
ax.hist(res, bins=100)
ax.set_xlabel("convergence time", fontsize=14)
ax.set_ylabel("occurrences", fontsize=14)
