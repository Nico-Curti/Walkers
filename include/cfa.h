#ifndef CFA_H
#define CFA_H
#ifdef VERBOSE
#include <iostream>
#endif
#include <memory>
#include <chrono>
#include <random>
#include <climits>
#include <algorithm>
#include <numeric>

static constexpr float inf = std::numeric_limits<float>::infinity();

namespace walker
{
  template<typename Func>
  auto cfa(Func objfunc,
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

    std::unique_ptr<float*, std::function<void(float**)>> positions(new float*[n_population](),
                                                                    [&](float** x)
                                                                    {
                                                                      std::for_each(x, x + dim, std::default_delete<float[]>());
                                                                      delete[] x;
                                                                    });
    solution s(n_population, max_iters, "CFA");

    std::mt19937 engine(seed);
    std::uniform_real_distribution<float> bound_rng(lower_bound, upper_bound);

    // Initialize timer for the experiment
    auto timer = std::chrono::high_resolution_clock::now();
    s.start_time = timer;

#ifdef VERBOSE
    std::cout << "CFA is optimizing..." << std::endl;
#endif

#ifdef _OPENMP
#pragma omp declare reduction (minPair : best_idx : omp_out = omp_in.second < omp_out.second ? omp_in : omp_out) initializer(omp_priv = omp_orig)
#pragma omp parallel num_threads(nth) private(fitness, R, V, W)
  {
#endif

#ifdef _OPENMP
#pragma omp for
    for (int i = 0; i < n_population; ++i) (positions.get()) = new float[dim];
#else
    std::generate_n(positions.get(), n_population, [&](){return new float[dim];});

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
      fitness = fit(positions[i]);
      // find the initial best solution
      best.first   = fitness < best.second  ? i       : best.first;
      best.second  = fitness < best.second  ? fitness : best.second;
    }

    // main loop
    while(iteration < max_iters)
    {
      best.second = inf;
      best.first  = 0;

      R = ; // [-1, 2]
      V = ; // [-1.5, 1.5]
      W = ; // [-1, 1]

#ifdef _OPENMP
      avg_best = 0.f;
#pragma omp for reduction(+ : avg_best)
      for (int i = 0; i < dim; ++i) avg_best += positions[best.first][j];
#else
      avg_best = std::accumulate(positions[best.first],
                                 positions[best.first] + dim,
                                 0.f) / dim;
#endif

#ifdef _OPENMP
#pragma omp for collapse(2)
#endif
      for (int i = 0; i < m; ++i)
        for (int j = 0; j < dim; ++j)
        {
          positions[i      ][j] = R * positions[i][j] + (positions[best.first][j] - positions[i][j]);
          positions[i +   m][j] = V * (positions[best.first][j] - positions[i + m][j]) + positions[best.first][j];
          positions[i + 2*m][j] = W * (positions[best.first][j] - avg_best) + positions[best.first][j];
          positions[i + 3*m][j] = bound_rng(engine);
        }

#ifdef _OPENMP
#pragma omp for reduction(minPair : best)
#endif
      for (int i = 0; i < n_population; ++i)
      {
        fitness = fit(positions[i]);
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

    timer = std::chrono::high_resolution_clock::now();
    s.end_time = timer;
    s.execution_time = std::chrono::duration_cast<std::chrono::seconds>(s.end_time - s.start_time).count();
    s.best = best.second;

    return s;
  }

#endif // CFA_H
