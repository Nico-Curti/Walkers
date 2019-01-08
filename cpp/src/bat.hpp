#ifndef BAT_H
#define BAT_H

#include <walkers.h>

namespace walker
{
  template<typename Func>
  Solution bat(Func objfunc,
               const float &lower_bound,
               const float &upper_bound,
               const int &dim,
               const int &n_population,
               const int &max_iters,
               float A = .5f,             // Loudness   (constant or decreasing)
               float r = .5f,             // Pulse rate (constant or decreasing)
               float Qmin = 0.f,          // Frequency minimum
               float Qmax = 2.f,          // Frequency maximum
               float step = 1e-3f,        // scale of normal random generator
               std::size_t seed = 0,
               int verbose = 1,
               int nth = 4
               )
  {
    //using res_t = typename std::result_of<Func(const float *)>::type; // since c++17
    //static_assert(std::is_floating_point<res_t>::value, "Invalid type function");

    typedef std::pair<int, float> best_idx;
    int iteration = 0;
    best_idx best;

    std::unique_ptr<std::unique_ptr<float[]>[]> S  (new std::unique_ptr<float[]>[n_population]),
                                                v  (new std::unique_ptr<float[]>[n_population]);
    std::shared_ptr<std::shared_ptr<float[]>[]> Sol(new std::shared_ptr<float[]>[n_population]);
    std::unique_ptr<float[]> rngt   (new float[n_population]),
                             fitness(new float[n_population]),
                             new_fit(new float[n_population]);

    Solution s(n_population, dim, max_iters, "BAT");

    // Initialize timer for the experiment
    auto start_time = std::chrono::high_resolution_clock::now();

#ifdef VERBOSE
    std::cout << "BAT is optimizing..." << std::endl;
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
    std::uniform_real_distribution<float> Qbox(Qmin, Qmax);
    std::uniform_real_distribution<float> rng(0.f, 1.f);
    std::normal_distribution<float> normal(0.f, 1.f);

#ifdef _OPENMP
#pragma omp for
#endif
    for (int i = 0; i < n_population; ++i)
    {
      S[i]   = std::make_unique<float[]>(dim);
      Sol[i] = std::make_unique<float[]>(dim);
      v[i]   = std::make_unique<float[]>(dim);
    }

    // initialize
#ifdef _OPENMP
#pragma omp for collapse(2)
#endif
    for (int i = 0; i < n_population; ++i)
      for (int j = 0; j < dim; ++j)
      {
        v[i][j]   = 0.f;
        Sol[i][j] = bound_rng(engine);
      }

    best.second = inf;
    best.first  = 0;

#ifdef _OPENMP
#pragma omp for reduction(minPair : best)
#endif
    for (int i = 0; i < n_population; ++i)
    {
      fitness[i] = objfunc(Sol[i].get(), dim);
      // find the initial best solution
      best.first  = fitness[i] < best.second ? i          : best.first;
      best.second = fitness[i] < best.second ? fitness[i] : best.second;
    }

#ifdef _OPENMP
#pragma omp for collapse(2)
#endif
    for (int i = 0; i < n_population; ++i)
      for (int j = 0; j < dim; ++j)
      {
        v[i][j] += Qbox(engine) * (Sol[i][j] - Sol[best.first][j]);
        S[i][j]  = Sol[i][j] + v[i][j];
        // pulse rate
        S[i][j]  = (rngt[i] > r) ? Sol[best.first][j] + step * normal(engine) : S[i][j];
      }

    while (true)
    {
      // Evaluate new solutions
#ifdef _OPENMP
#pragma omp for
#endif
      for (int i = 0; i < n_population; ++i)
      {
        new_fit[i] = objfunc(S[i].get(), dim);
        rngt[i]    = rng(engine);
      }

      // Update if the solution improves
#ifdef _OPENMP
#pragma omp for collapse(2)
#endif
      for (int i = 0; i < n_population; ++i)
        for (int j = 0; j < dim; ++j)
        {
          // troubles with random (same also in next loop!)
          Sol[i][j]  = (new_fit[i] <= fitness[i] && rngt[i] < A) ? S[i][j]     :  Sol[i][j];
          Sol[i][j]  = (Sol[i][j]  < lower_bound)                ? lower_bound : (Sol[i][j] > upper_bound) ? upper_bound : Sol[i][j];
        }

    // Update the current best solution
    best.second = inf;
    best.first  = 0;
#ifdef _OPENMP
#pragma omp for reduction(minPair : best)
#endif
    for (int i = 0; i < n_population; ++i)
    {
      fitness[i] = (new_fit[i] <= fitness[i] && rngt[i] < A) ? new_fit[i] : fitness[i];
      // find the new best solution
      best.first  = fitness[i] < best.second ? i          : best.first;
      best.second = fitness[i] < best.second ? fitness[i] : best.second;

      rngt[i]    = rng(engine);
    }

    s.walk[iteration] = Sol[best.first];

#ifdef _OPENMP
#pragma omp single
#endif
      ++iteration;

    if (iteration >= max_iters) break;

    // Loop over all bats(solutions)
#ifdef _OPENMP
#pragma omp for collapse(2)
#endif
    for (int i = 0; i < n_population; ++i)
      for (int j = 0; j < dim; ++j)
      {
        v[i][j] += Qbox(engine) * (Sol[i][j] - S[best.first][j]);
        S[i][j]  = Sol[i][j] + v[i][j];
        // pulse rate
        S[i][j]  = (rngt[i] > r) ? S[best.first][j] + step * normal(engine) : S[i][j];
      }

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

#endif // BAT_H
