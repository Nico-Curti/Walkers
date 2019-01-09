#ifndef SSA_H
#define SSA_H

#include <walkers.h>

namespace walker
{
  template<typename Func>
  Solution ssa(Func objfunc,
               const float &lower_bound,
               const float &upper_bound,
               const int &dim,
               const int &n_population,
               const int &max_iters,
               std::size_t seed = 0,
               int verbose = 1,
               int nth = 4
               )
  {
    //using res_t = typename std::result_of<Func(const float *)>::type; // since c++17
    //static_assert(std::is_floating_point<res_t>::value, "Invalid type function");

    typedef std::pair<int, float> best_idx;
    const int half = n_population >> 1;
    int iteration = 0;
    best_idx best, tmp;
    float c1, c2, c3;

    std::shared_ptr<std::shared_ptr<float[]>[]> SalpPos(new std::shared_ptr<float[]>[n_population]);
    std::unique_ptr<float[]> fitness(new float[n_population]);

    Solution s(n_population, dim, max_iters, "SSA");

    // Initialize timer for the experiment
    auto start_time = std::chrono::high_resolution_clock::now();

#ifdef VERBOSE
    std::cout << "SSA is optimizing..." << std::endl;
#endif

#ifdef _OPENMP
#pragma omp declare reduction (minPair : best_idx : omp_out = omp_in.second < omp_out.second ? omp_in : omp_out) initializer(omp_priv = omp_orig)
#pragma omp parallel num_threads(nth)
  {
#endif
#ifdef _OPENMP
    std::mt19937 engine(seed + omp_get_thread_num());
#else
    std::mt19937 engine(seed);
#endif

    std::uniform_real_distribution<float> bound_rng(lower_bound, upper_bound);
    std::uniform_real_distribution<float> rng(0.f, 1.f);

#ifdef _OPENMP
#pragma omp for
#endif
    for (int i = 0; i < n_population; ++i)
      SalpPos[i] = std::make_unique<float[]>(dim);

    // initialize
#ifdef _OPENMP
#pragma omp for collapse(2)
#endif
    for (int i = 0; i < n_population; ++i)
      for (int j = 0; j < dim; ++j)
        SalpPos[i][j] = bound_rng(engine);

    best.second = inf;
    best.first  = 0;
#ifdef _OPENMP
#pragma omp for reduction(minPair : best)
#endif
    for (int i = 0; i < n_population; ++i)
    {
      fitness[i] = objfunc(SalpPos[i].get(), dim);
      // find the new best solution
      best.first  = fitness[i] < best.second ? i          : best.first;
      best.second = fitness[i] < best.second ? fitness[i] : best.second;
    }

    while (iteration < max_iters)
    {
#ifdef _OPENMP
#pragma omp single
      {
#endif
        c1 = 4.f * (iteration + 2) / max_iters;
        c1 = 2.f * std::exp(-c1*c1);
#ifdef _OPENMP
      }
#endif

#ifdef _OPENMP
#pragma omp for private(c2, c3) collapse(2)
#endif
      for (int i = 0; i < half; ++i)
        for (int j = 0; j < dim; ++j)
        {
          c2 = bound_rng(engine);
          c3 = rng(engine);
          SalpPos[i][j] = (c3 < .5f) ? SalpPos[best.first][j] + c1 * c2 :
                                       SalpPos[best.first][j] - c1 * c2 ;
        }

#ifdef _OPENMP
#pragma omp for collapse(2)
#endif
      for (int i = half; i < n_population; ++i)
        for (int j = 0; j < dim; ++j)
          SalpPos[i][j] = ( SalpPos[i - 1][j] + SalpPos[i][j] ) * .5f;

#ifdef _OPENMP
#pragma omp for collapse(2)
#endif
      for (int i = 0; i < n_population; ++i)
        for (int j = 0; j < dim; ++j)
          SalpPos[i][j] = (SalpPos[i][j] < lower_bound) ? lower_bound :
                          (SalpPos[i][j] > upper_bound) ? upper_bound :
                           SalpPos[i][j];

      tmp.second = inf;
      tmp.first  = 0;
#ifdef _OPENMP
#pragma omp for reduction(minPair : best)
#endif
      for (int i = 0; i < n_population; ++i)
      {
        fitness[i] = objfunc(SalpPos[i].get(), dim);
        // find the new best solution
        tmp.first  = fitness[i] < tmp.second ? i          : tmp.first;
        tmp.second = fitness[i] < tmp.second ? fitness[i] : tmp.second;
      }

#ifdef _OPENMP
#pragma omp master
#endif
      best = (tmp.second < best.second) ? tmp : best;

      s.walk[iteration] = SalpPos[best.first];

#ifdef _OPENMP
#pragma omp single nowait
      {
#endif
        switch(verbose)
        {
          case 1: printProgress(iteration, max_iters, start_time);
          break;
          case 2:
          {
            std::cout << "iter: "
                      << std::setw(5) << iteration             << " : "
                      << std::setw(5) << std::setprecision(3)  << best.second
                      << std::endl;
          } break;
          default: break;
        }
#ifdef _OPENMP
      } // close single section
#endif

#ifdef _OPENMP
#pragma omp single
#endif
      ++iteration;
    }
#ifdef _OPENMP
  } // end parallel section
#endif

    auto end_time = std::chrono::high_resolution_clock::now();
    s.execution_time = std::chrono::duration_cast<std::chrono::seconds>(end_time - start_time).count();
    s.best = best.second;

    return s;
  }
}

#endif //SSA_H
