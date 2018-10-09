#!usr/bin/python

import numpy as np
import time
import sys
    
np.random.seed(123)

solution = {"best" : 0.,
            "walk" : [],
            "optimizer" : "",
            "objfname"  : "",
            "start_time" : 0.,
            "end_time"   : 0.,
            "execution_time" : 0.,
            "dimension" : 0.,
            "population" : 0.,
            "max_iters" : 0.
        }


def bat(objfunc,
        lower_bound,
        upper_bound,
        dim,          # Number of dimensions 
        n_population, # Population size
        max_iters,    # Number of generations
        A = .5,       # Loudness  (constant or decreasing)
        r = .5,       # Pulse rate (constant or decreasing)
        Qmin = 0.,    # Frequency minimum
        Qmax = 2.,    # Frequency maximum
        step = 1e-3   # scale of normal random generator
        ):
    # Initializing arrays
    Q  = Qmin + (Qmin - Qmax) * np.random.rand(max_iters, n_population)
    v = np.zeros(shape=(dim, n_population), dtype=float) # velocities
    walk = np.empty(shape=(max_iters,), dtype=float)
    
    # Initialize the population/solutions
    Sol = np.random.uniform(low=lower_bound, 
                            high=upper_bound, 
                            size=(dim, n_population))
    print ("BAT is optimizing \"" + objfunc.__name__ + "\"")
    solution["optimizer"] = "BAT"
    solution["dimension"] = dim,
    solution["population"] = n_population
    solution["max_iters"] = max_iters
    solution["objfname"] = objfunc.__name__
    timer = time.time()
    solution["start_time"] = timer
    
    fitness = np.apply_along_axis(objfunc, 0, Sol)
    best = np.argmin(fitness)
    fmin = fitness[best]
    best = np.array(Sol[:, best], ndmin=2)
    
    rng = np.random.uniform(low=0., high=1., size=(max_iters, 
                                                   n_population))
    rng = rng > r
    dim_rng = np.sum(rng, axis=1)
    rng2 = np.random.uniform(low=0., high=1., size=(max_iters, 
                                                    n_population))
    rng2 = rng2 < A
    # main loop
    for t in range(max_iters):
        v += Q[t] * (Sol - best.T)
        S  = Sol + v
        
        # check boundaries
        Sol = np.clip(Sol, lower_bound, upper_bound)
        
        # Pulse rate        
        S[:, rng[t]] = best.T + step * np.random.randn(dim, dim_rng[t])

        # Evaluate new solutions
        fit_new = np.apply_along_axis(objfunc, 0, S)
        
        # Update if the solution improves
        upd = np.logical_and(rng2[t], fit_new <= fitness)
        Sol[:, upd] = S[:, upd]
        fitness[upd] = fit_new[upd]
        
        tmp_best = np.argmin(fit_new)
        tmp_fmin = fit_new[tmp_best]
        # Update the current best solution
        if tmp_fmin <= fmin:
            best = np.array(S[:, tmp_best], ndmin=2)
            fmin = tmp_fmin
        # Update convergence curve
        walk[t] = fmin
        
        sys.stdout.write('\r')
        sys.stdout.write("It %-5d: [%-25s] %.3f %.3f sec"
                         %(t,
                           '=' * int(t / 20),
                           fmin, 
                           time.time() - solution["start_time"]))
        
    solution["end_time"] = time.time()
    solution["run_time"] = solution["end_time"] - solution["start_time"]
    solution["walk"] = walk
    solution["best"] = fmin



def score_func(x): # F10
    dim = len(x)
    return -20. * np.exp(-.2 * np.sqrt(sum(x*x) / dim))     \
                - np.exp(sum(np.cos(2. * np.pi * x)) / dim) \
           + 22.718281828459045

if __name__ == "__main__":
    
    n_population = 50
    max_iters = 500
    lower_bound = -32
    upper_bound = 32
    dim = 30
    
    bat(score_func,
        lower_bound,
        upper_bound,
        dim,          
        n_population,
        max_iters)
