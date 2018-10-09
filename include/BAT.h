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
  auto bat(const int &n_population,
          const int &max_iters,
          Func objfunc,
          const float &upper_bound,
          const float &lower_bound,
          float A = .5f,            // Loudness   (constant or decreasing)
          float r = .5f,            // Pulse rate (constant or decreasing)
          float Qmin = 0.f,         // Frequency minimum
          float Qmax = 2.f,         // Frequency maximum
          float step = 1e-3f,       // scale of normal random generator
          std::size_t seed = 0,
          int verbose = 1,
          int nth = 4
          )
  {
    using res_t = typename std::result_of<Func(const genome &)>::type; // since c++17
    typedef std::pair<int, float> best_idx;
    int iteration = 0;
    best_idx best;
    std::unique_ptr<float[]> Q(new float[n_population]),       // frequency
                             v(new float[n_population * dim]); // velocity


    std::unique_ptr<genome[]> population(new genome[n_population]),
                              new_gen(   new genome[n_population]);
    std::unique_ptr<res_t[]> fitness (   new res_t[n_population]);

    solution s(n_population, max_iters, "BAT");

    std::mt19937 engine(seed);
    std::uniform_real_distribution<float> bound_rng(lower_bound, upper_bound);
    std::uniform_real_distribution<float> rng(0.f, 1.f);
    std::normal_distribution<float> normal(); // miss

    // Initialize timer for the experiment
    auto timer = std::chrono::high_resolution_clock::now();
    s.start_time = timer;

#ifdef VERBOSE
    std::cout << "BAT is optimizing..." << std::endl;
#endif

#ifdef _OPENMP
#pragma omp declare reduction (minPair : best_idx : omp_out = omp_in.second < omp_out.second ? omp_in : omp_out) initializer(omp_priv = omp_orig)
#pragma omp parallel num_threads(nth)
  {
#endif

    // initialize the population/solutions
#ifdef _OPENMP
#pragma omp for
    for (int i = 0; i < n_population; ++i) population[i] = genome(bound_rng(engine));
#else
    std::generate_n(population.get(), n_population, [&](){return genome(bound_rng(engine));});
#endif

    best.second = inf;
    best.first  = 0;
#ifdef _OPENMP
#pragma omp for reduction(minPair : best)
#endif
    for (int i = 0; i < n_population; ++i)
    {
      fitness[i] = fit(population[i]);
      // find the initial best solution
      best.first  = fitness[i] < best.second ? i          : best.first;
      best.second = fitness[i] < best.second ? fitness[i] : best.second;
    }

    // main loop
    while(iteration < max_iters)
    {
      best.second = inf;
      best.first  = 0;
      // loop over all bats (solutions)
#ifdef _OPENMP
#pragma omp for reduction(minPair : best)
#endif
      for (int i = 0; i < n_population; ++i)
      {
        Q[i]       = Qmin + (Qmin - Qmax) * rng(engine);
        v[i]      += Q[i] * (population[i] - population[best]); // WRONG
        new_gen[i] = population[i] + v[i];

        // check boundaries
        //population[i] = (population[i] < lower_bound) ? lower_bound :
        //                (population[i] > upper_bound) ? upper_bound :
        //                 population[i]; // mmmmh

        // pulse rate
        if (rng(engine) > r) new_gen[i] = best + step * normal(engine); // wrong

        // evaluate new solution
        res_t f_new = fit(new_gen[i]);

        // update if the solution improves
        float random = rng(engine);
        population[i] = (f_new <= fitness[i] && random < A) ? new_gen[i] : population[i];
        fitness[i]    = (f_new <= fitness[i] && random < A) ? f_new      : fitness[i];

        // update the current best solution
        best.first  = fitness[i] < best.second ? i          : best.first;
        best.second = fitness[i] < best.second ? fitness[i] : best.second;
      }
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

#endif // BAT_H
