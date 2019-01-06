#include <walkers.h>

namespace walker
{
  template<typename Func>
  auto pso(Func objfunc,
           const float &lower_bound,
           const float &upper_bound,
           const int &dim,
           const int &n_population,
           const int &max_iters,
           float Vmax = 6.f,
           float wmax = .9f,
           float wmin = .2f,
           float c1   = 2.f,
           float c2   = 2.f,
           std::size_t seed = 0,
           int verbose = 1,
           int nth = 4)
  {
    typedef std::pair<int, float> best_idx;
    int iteration = 0;
    best_idx best;

    std::unique_ptr<std::unique_ptr<float[]>[]> positions(new std::unique_ptr<float[]>[n_population]),
                                                velocity (new std::unique_ptr<float[]>[n_population]);
    std::unique_ptr<float[]> fitness(new float[n_population]);

    solution s(n_population, max_iters, "PSO");


    // Initialize timer for the experiment
    auto start_time = std::chrono::high_resolution_clock::now();

#ifdef VERBOSE
    std::cout << "PSO is optimizing..." << std::endl;
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
    for (int i = 0; i < n_population; ++i)
    {
      positions[i] = std::make_unique<float[]>(dim);
      velocity[i]  = std::make_unique<float[]>(dim);
      fitness[i]   = inf;
    }
#else
    std::generate_n(positions.get(), n_population, [&](){return std::make_unique<float[]>(dim);});
    std::generate_n(velocity.get(),  n_population, [&](){return std::make_unique<float[]>(dim);});
    std::fill_n(fitness.get(), n_population, inf);
#endif

    // initialize the positions/solutions
#ifdef _OPENMP
#pragma omp for collapse(2)
#endif
    for (int i = 0; i < n_population; ++i)
      for (int j = 0; j < dim; ++j)
      {
        positions[i][j] = bound_rng(engine);
        velocity[i][j]  = 0.f;
      }

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
        float f = objfunc(positions[i].get());
        // find the initial best solution
        best.first   = f < best.second  ? i : best.first;
        best.second  = f < best.second  ? f : best.second;

        fitness[i]   = f < fitness[i]   ? f : fitness[i];
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

