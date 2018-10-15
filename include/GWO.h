#ifndef BAT_H
#define BAT_H
#ifdef VERBOSE
#include <iostream>
#endif
#include <memory>
#include <chrono>
#include <random>
#include <climits>
#include <utility>

static constexpr float inf = std::numeric_limits<float>::infinity();

namespace walker
{
  template<typename genome, typename Func>
  auto gwo(const int &n_population,
          const int &max_iters,
          Func objfunc,
          const float &upper_bound,
          const float &lower_bound,
          std::size_t seed = 0,
          int verbose = 1,
          int nth = 4
          )
  {
    using res_t = typename std::result_of<Func(const genome &)>::type; // since c++17
    typedef std::pair<int, float> best_idx;
    int iteration = 0,
        alpha_pos = 0, beta_pos = 0, delta_pos = 0;
    float alpha_score = inf, beta_score = inf, delta_score = inf,
          a, r1, r2, A, C, D_alpha, D_beta, D_delta;
    best_idx best;

    std::unique_ptr<genome[]> population(new genome[n_population]);

    solution s(n_population, max_iters, "GWO");

    std::mt19937 engine(seed);
    std::uniform_real_distribution<float> bound_rng(lower_bound, upper_bound);
    std::uniform_real_distribution<float> rng(0.f, 1.f);

    // Initialize timer for the experiment
    auto timer = std::chrono::high_resolution_clock::now();
    s.start_time = timer;

#ifdef VERBOSE
    std::cout << "GWO is optimizing..." << std::endl;
#endif

#ifdef _OPENMP
#pragma omp declare reduction (minPair : best_idx : omp_out = omp_in.second < omp_out.second ? omp_in : omp_out) initializer(omp_priv = omp_orig)
#pragma omp parallel num_threads(nth) private(a, r1, r2, A, C, D_alpha, D_beta, D_delta)
  {
#endif

    // initialize the population/solutions
#ifdef _OPENMP
#pragma omp for
    for (int i = 0; i < n_population; ++i) population[i] = genome(bound_rng(engine));
#else
    std::generate_n(population.get(), n_population, [&](){return genome(bound_rng(engine));});
#endif

    // main loop
    while(iteration < max_iters)
    {
#ifdef _OPENMP
#pragma omp for reduction(minPair : best)
#endif
      for (int i = 0; i < n_population; ++i)
      {
        fitness[i] = fit(population[i]);
        // find the initial best solution
        best.first   = fitness[i] < best.second  ? i          : best.first;
        best.second  = fitness[i] < best.second  ? fitness[i] : best.second;
      }

      alpha_pos   = fitness[best.first] < alpha_score ? best.first          : alpha_pos;
      alpha_score = fitness[best.first] < alpha_score ? fitness[best.first] : alpha_score;

      beta_pos   = (fitness[best.first] > alpha_score && fitness[best.first] < beta_score) ? best.first          : beta_pos;
      beta_score = (fitness[best.first] > alpha_score && fitness[best.first] < beta_score) ? fitness[best.first] : beta_score;

      delta_pos   = (fitness[best.first] > alpha_score && fitness[best.first] > beta_score && fitness[best.first] < delta_score) ? best.first          : delta_pos;
      delta_score = (fitness[best.first] > alpha_score && fitness[best.first] > beta_score && fitness[best.first] < delta_score) ? fitness[best.first] : delta_score;

      a = 2.f - iteration * 2.f / max_iters; // a decreases linearly from 2 to 0

      // Update the Position of search agents including omegas
#ifdef _OPENMP
#pragma omp for
#endif
      for (int i = 0; i < n_population; ++i)
      {
        r1 = rng(engine);
        r2 = rng(engine);

        A  = 2.f * a * r1 - a;
        C  = 2.f * r2;
        D_alpha = std::fabs(C * );

        r1 = rng(engine);
        r2 = rng(engine);

        A  = 2.f * a * r1 - a;
        C  = 2.f * r2;
        D_beta = std::fabs(C * );

        r1 = rng(engine);
        r2 = rng(engine);

        A  = 2.f * a * r1 - a;
        C  = 2.f * r2;
        D_delta = std::fabs(C * );

        population[i] = (D_alpha + D_beta + D_delta) * .33333333f;
      }

      s.walk[iteration] = alpha.second;

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

#endif // GWO_H
