#ifndef CFA_H
#define CFA_H

#include <walkers.h>

namespace walker
{
  template<typename Func>
  Solution cfa(Func objfunc,
               const float &lower_bound,
               const float &upper_bound,
               const int &dim,
               const int &n_population,
               const int &max_iters,
               std::size_t seed = 0,
               int verbose = 1,
               int nth = 4)
  {
    typedef std::pair<int, float> best_idx;
    int iteration = 0,
        m   = n_population / 4;

    best_idx best;
    best.second = inf;
    best.first  = 0;
    float fitness, avg_best, R, V, W;

    std::shared_ptr<std::shared_ptr<float[]>[]> positions(new std::shared_ptr<float[]>[n_population]);

    Solution s(n_population, dim, max_iters, "CFA");

    // Initialize timer for the experiment
    auto start_time = std::chrono::high_resolution_clock::now();

#ifdef VERBOSE
    std::cout << "CFA is optimizing..." << std::endl;
#endif

#ifdef _OPENMP
#pragma omp declare reduction (minPair : best_idx : omp_out = omp_in.second < omp_out.second ? omp_in : omp_out) initializer(omp_priv = omp_orig)
#pragma omp parallel num_threads(nth) private(fitness, R, V, W)
  {
#endif

#ifdef _OPENMP
    std::mt19937 engine(seed + omp_get_thread_num());
#else
    std::mt19937 engine(seed);
#endif

    std::uniform_real_distribution<float> bound_rng(lower_bound, upper_bound),
                                          rngR(-1.f, 2.f),
                                          rngV(-1.5f, 1.5f),
                                          rngW(-1.f, 1.f);

#ifdef _OPENMP
#pragma omp for
    for (int i = 0; i < n_population; ++i)
      positions[i] = std::make_unique<float[]>(dim);
#else
    std::generate_n(positions.get(), n_population, [&](){return std::make_unique<float[]>(dim);});
#endif

#ifdef _OPENMP
#pragma omp for collapse(2)
#endif
    for (int i = 0; i < n_population; ++i)
      for (int j = 0; j < dim; ++j)
        positions[i][j] = bound_rng(engine);

#ifdef _OPENMP
#pragma omp for reduction(minPair : best)
#endif
    for (int i = 0; i < n_population; ++i)
    {
      fitness = objfunc(positions[i].get(), dim);
      // find the initial best solution
      best.first   = fitness < best.second  ? i       : best.first;
      best.second  = fitness < best.second  ? fitness : best.second;
    }

    // main loop
    while(iteration < max_iters)
    {
      best.second = inf;
      best.first  = 0;

      R = rngR(engine); // [-1, 2]
      V = rngV(engine); // [-1.5, 1.5]
      W = rngW(engine); // [-1, 1]

#ifdef _OPENMP
      avg_best = 0.f;
#pragma omp for reduction(+ : avg_best)
      for (int i = 0; i < dim; ++i)
        avg_best += positions[best.first][i];
#else
      avg_best = std::accumulate(positions[best.first].get(),
                                 positions[best.first].get() + dim,
                                 0.f) / dim;
#endif

#ifdef _OPENMP
#pragma omp for collapse(2)
#endif
      for (int i = 0; i < m; ++i)
        for (int j = 0; j < dim; ++j)
        {
          positions[i      ][j] = R *  positions[i][j] + (positions[best.first][j] - positions[i][j]);
          positions[i +   m][j] = V * (positions[best.first][j] - positions[i + m][j]) + positions[best.first][j];
          positions[i + 2*m][j] = W * (positions[best.first][j] - avg_best) + positions[best.first][j];
          positions[i + 3*m][j] = bound_rng(engine);
        }

#ifdef _OPENMP
#pragma omp for reduction(minPair : best)
#endif
      for (int i = 0; i < n_population; ++i)
      {
        fitness = objfunc(positions[i].get(), dim);
        // find the initial best solution
        best.first   = fitness < best.second  ? i       : best.first;
        best.second  = fitness < best.second  ? fitness : best.second;
      }

      s.walk[iteration] = positions[best.first];

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

#endif // CFA_H
