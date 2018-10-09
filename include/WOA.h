#ifndef WOA_H
#define WOA_H
#ifdef VERBOSE
#include <iostream>
#endif
#include <memory>
#include <chrono>
#include <random>
#include <climits>

static constexpr float inf = std::numeric_limits<float>::infinity();

namespace walker
{
  template<typename genome, typename Func>
  auto woa(const int &n_population,
           const int &max_iters,
           Func objfunc,
           const float &upper_bound,
           const float &lower_bound,
           float b = 1.f,
           std::size_t seed = 0,
           int verbose = 1,
           int nth = 4
           )
  {
    using res_t = typename std::result_of<Func(const genome &)>::type; // since c++17
    typedef std::pair<int, float> best_idx;
    int iteration = 0;
    best_idx leader;
    res_t fitness;

    std::unique_ptr<genome[]> population(new genome[n_population]);

    solution s(n_population, max_iters, "WOA");

    std::mt19937 engine(seed);
    std::uniform_real_distribution<float> bound_rng(lower_bound, upper_bound);
    std::uniform_real_distribution<float> rng(0.f, 1.f);

    // Initialize timer for the experiment
    auto timer = std::chrono::high_resolution_clock::now();
    s.start_time = timer;

#ifdef VERBOSE
    std::cout << "WOA is optimizing..." << std::endl;
#endif

#ifdef _OPENMP
#pragma omp declare reduction (minPair : best_idx : omp_out = omp_in.second < omp_out.second ? omp_in : omp_out) initializer(omp_priv = omp_orig)
#pragma omp parallel num_threads(nth) private(fitness)
  {
#endif

    // initialize the population of search agents
#ifdef _OPENMP
#pragma omp for
    for (int i = 0; i < n_population; ++i) population[i] = genome(bound_rng(engine));
#else
    std::generate_n(population.get(), n_population, [&](){return genome(bound_rng(engine));});
#endif

    // main loop
    while(iteration < max_iters)
    {
      leader.second = inf;
      leader.first  = 0;
#ifdef _OPENMP
#pragma omp for reduction(minPair : leader)
#endif
      for (int i = 0; i < n_population; ++i)
      {
        // compute objective function for each search agent
        fitness = fit(population[i]);
        // update the leader
        leader.first  = fitness < leader.second ? i       : leader.first; // update alpha
        leader.second = fitness < leader.second ? fitness : leader.second;
      }

      float a  = 2.f - iteration * (2.f / max_iters); // a decreases linearly from 2 to 0 in Eq. (2.3)
      float a2 = 1.f + iteration * (-1.f / max_iters);// a2 linearly decreases from -1 to -2 to calculate t in Eq. (3.12)

      // update the position of search agents
#ifdef _OPENMP
#pragma omp for
#endif
      for (int i = 0; i < n_population; ++i)
      {
        float r1 = rng(engine);
        float r2 = rng(engine);

        float A  = 2.f * a * r1 - a; // Eq. (2.3) in the paper
        float C  = 2.f * r2;         // Eq. (2.4) in the paper
        float l  = (a2 - 1.f) * rng(engine) + 1.f; // parameters in Eq. (2.5)
        bool p   = static_cast<bool>(rng(engine) > .5f);      // Eq. (2.6)

        // miss

      }

      s.walk[iteration] = leader_score;

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
    s.best = leader_score;

    return s;
  }

#endif // WOA_H
