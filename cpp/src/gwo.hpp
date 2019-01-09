#ifndef GWO_H
#define GWO_H

#include <walkers.h>

namespace walker
{
  template<typename Func>
  Solution gwo(Func objfunc,
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
        alpha_pos = 0, beta_pos = 0, delta_pos = 0;
    float alpha_score = inf,
          beta_score  = inf,
          delta_score = inf,
          a, fitness;
    best_idx best;

    std::shared_ptr<std::shared_ptr<float[]>[]> positions(new std::shared_ptr<float[]>[n_population]);
    std::array<float, 3> r1, r2;

    Solution s(n_population, dim, max_iters, "GWO");

    // Initialize timer for the experiment
    auto start_time = std::chrono::high_resolution_clock::now();

#ifdef VERBOSE
    std::cout << "GWO is optimizing..." << std::endl;
#endif

#ifdef _OPENMP
#pragma omp declare reduction (minPair : best_idx : omp_out = omp_in.second < omp_out.second ? omp_in : omp_out) initializer(omp_priv = omp_orig)
#pragma omp parallel num_threads(nth) private(fitness, a, alpha_pos, alpha_score, beta_pos, beta_score, delta_pos, delta_score)
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
    for (int i = 0; i < n_population; ++i) positions[i] = std::make_unique<float[]>(dim);
#else
    std::generate_n(positions.get(), n_population, [&](){return std::make_unique<float[]>(dim);});
#endif

    // initialize the positions/solutions
#ifdef _OPENMP
#pragma omp for collapse(2)
#endif
    for (int i = 0; i < n_population; ++i)
      for (int j = 0; j < dim; ++j)
        positions[i][j] = bound_rng(engine);

    // main loop
    while(iteration < max_iters)
    {
      best.second = inf;
      best.first  = 0;

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

      alpha_pos   = best.second < alpha_score ? best.first  : alpha_pos;
      alpha_score = best.second < alpha_score ? best.second : alpha_score;

      beta_pos    = (best.second > alpha_score && best.second < beta_score) ? best.first  : beta_pos;
      beta_score  = (best.second > alpha_score && best.second < beta_score) ? best.second : beta_score;

      delta_pos   = (best.second > alpha_score && best.second > beta_score && best.second < delta_score) ? best.first  : delta_pos;
      delta_score = (best.second > alpha_score && best.second > beta_score && best.second < delta_score) ? best.second : delta_score;

      a = 2.f - iteration * 2.f / max_iters; // a decreases linearly from 2 to 0

#ifdef _OPENMP
#pragma omp for collapse(2)
#endif
      for (int i = 0; i < n_population; ++i)
        for (int j = 0; j < dim; ++j)
        {
          r1[0] = rng(engine);
          r1[1] = rng(engine);
          r1[2] = rng(engine);
          r2[0] = rng(engine);
          r2[1] = rng(engine);
          r2[2] = rng(engine);
          (positions.get())[i][j] = (
                              (positions[alpha_pos][j] - std::fabs(2.f * r2[i*3]     * positions[alpha_pos][j] - positions[i][j]) * 2.f * a * r1[i*3] - a)
                              +
                              (positions[beta_pos][j]  - std::fabs(2.f * r2[i*3 + 1] * positions[beta_pos][j]  - positions[i][j]) * 2.f * a * r1[i*3 + 1] - a)
                              +
                              (positions[delta_pos][j] - std::fabs(2.f * r2[i*3 + 2] * positions[delta_pos][j] - positions[i][j]) * 2.f * a * r1[i*3 + 2] - a)
                            ) * .333333333f;
          // clip
          (positions.get())[i][j] = (positions[i][j] < lower_bound) ? lower_bound :
                                    (positions[i][j] > upper_bound) ? upper_bound :
                                     positions[i][j];
        }

      s.walk[iteration] = positions[alpha_pos];

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
                      << std::setw(5) << std::setprecision(3)  << alpha_score
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
    } // end while

#ifdef _OPENMP
  } // end parallel section
#endif

    auto end_time = std::chrono::high_resolution_clock::now();
    s.execution_time = std::chrono::duration_cast<std::chrono::seconds>(end_time - start_time).count();
    s.best = alpha_score;

    return s;
  }
}

#endif //GWO_H
