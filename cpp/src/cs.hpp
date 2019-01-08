#ifndef CS_H
#define CS_H

#include <walkers.h>

namespace walker
{
  template<typename Func>
  Solution cs(Func objfunc,
              const float &lower_bound,
              const float &upper_bound,
              const int &dim,
              const int &n_population,
              const int &max_iters,
              float pa = .25f, // discovery rate of alien eggs/solution
              std::size_t seed = 0,
              int verbose = 1,
              int nth = 4
              )
  {
    typedef std::pair<int, float> best_idx;
    int iteration = 0;
    best_idx best;

    Solution s(n_population, dim, max_iters, "CS");

    // Initialize timer for the experiment
    auto start_time = std::chrono::high_resolution_clock::now();

#ifdef VERBOSE
    std::cout << "CS is optimizing..." << std::endl;
#endif

#ifdef _OPENMP
#pragma omp parallel num_threads(nth)
  {
#endif

#ifdef _OPENMP
    std::mt19937 engine(seed + omp_get_thread_num());
#else
    std::mt19937 engine(seed);
#endif

    std::uniform_real_distribution<float> rng(lower_bound, upper_bound);

    // main loop
    while(iteration < max_iters)
    {




      //s.walk[iteration] = ;

#ifdef _OPENMP
#pragma omp single
#endif
      ++iteration;
    } // end while

#ifdef _OPENMP
  } // end parallel section
#endif

    auto end_time = std::chrono::high_resolution_clock::now();
    s.execution_time = std::chrono::duration_cast<std::chrono::seconds>(end_time - start_time).count();
    s.best = best.second;

    return s;
  }
}

#endif // CS_H
