#include <walkers.h>

namespace walker
{
  template<typename Func>
  auto cs(Func objfunc,
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
    using res_t = typename std::result_of<Func(const genome &)>::type; // since c++17
    typedef std::pair<int, float> best_idx;
    int iteration = 0;
    best_idx best;

    solution s(n_population, max_iters, "CS");

    std::mt19937 engine(seed);
    std::uniform_real_distribution<float> rng(lower_bound, upper_bound);

    // Initialize timer for the experiment
    auto timer = std::chrono::high_resolution_clock::now();
    s.start_time = timer;

#ifdef VERBOSE
    std::cout << "CS is optimizing..." << std::endl;
#endif

#ifdef _OPENMP
#pragma omp parallel num_threads(nth)
  {
#endif

    // main loop
    while(iteration < max_iter)
    {




      s.walk[iteration] = best.second;

#ifdef _OPENMP
#pragma omp single
#endif
      ++iteration;
    } // end while

#ifdef _OPENMP
  } // end parallel section
#endif

    timer = std::chrono::high_resolution_clock::now();
    s.end_time = timer;
    s.execution_time = std::chrono::duration_cast<std::chrono::seconds>(s.end_time - s.start_time).count();
    s.best = best.second;

    return s;
  }
}

