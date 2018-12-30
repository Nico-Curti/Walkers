#include <walkers.h>

namespace walker
{
  template<typename Func>
  auto bbo(Func objfunc,
           const float &lower_bound,
           const float &upper_bound,
           const int &dim,
           const int &n_population,
           const int &max_iters,
           float pmutate = 1e-2f,
           float elite = 2.f,
           std::size_t seed = 0,
           int verbose = 1,
           int nth = 4)
  {
#ifdef _OPENMP
    nth -= nth % 2;
    const int diff_size = n_population % nth,
              size      = diff_size ? n_population - diff_size : n_population;
#endif
    int iteration = 0;

    std::shared_ptr<std::shared_ptr<std::function<float[]>>[]> positions(new std::shared_ptr<std::function<float[]>>[n_population]);

    std::unique_ptr<float[]> fitness(new float[n_population]);
    std::unique_ptr<int[]> rank(new int[n_population]);

    solution s(n_population, max_iters, "BBO");

    std::mt19937 engine(seed);
    std::uniform_real_distribution<float> bound_rng(lower_bound, upper_bound);
    std::uniform_real_distribution<float> rng(0.f, 1.f);

    // Initialize timer for the experiment
    auto start_time = std::chrono::high_resolution_clock::now();

#ifdef VERBOSE
    std::cout << "BBO is optimizing..." << std::endl;
#endif

#ifdef _OPENMP
#pragma omp parallel num_threads(nth)
  {
#endif

#ifdef _OPENMP
#pragma omp for
    for (int i = 0; i < n_population; ++i)
    {
      positions[i] = new float[dim];
      rank[i] = i;
    }
#else
    std::generate_n(positions.get(), n_population, [&](){return new float[dim];});
    std::iota(rank.get(), rank.get() + n_population, 0);
#endif

    // initialize the positions/solutions
#ifdef _OPENMP
#pragma omp for collapse(2)
#endif
    for (int i = 0; i < n_population; ++i)
      for (int j = 0; j < dim; ++j)
        positions[i].get()[j] = bound_rng(engine);

#ifdef _OPENMP
#pragma omp for
    for (int i = 0; i < n_population; ++i) fitness[i] = objfunc(positions[i]);
#else
    std::transform(positions.get(), positions.get() + n_population,
                   fitness.get(),
                   [&](const std::unique_ptr<float[]> &pop)
                   {
                    return objfunc(pop);
                  });
#endif

#ifdef _OPENMP
#pragma omp single
    {
      mergeargsort_parallel_omp(rank.get(), fitness.get(), 0, size, nth, [&](const int &a1, const int &a2){return fitness[a1] < fitness[a2];});
      if (diff_size)
      {
        std::sort(rank.get() + size, rank.get() + n_population, [&](const int &a1, const int &a2){return fitness[a1] < fitness[a2];});
        std::inplace_merge(rank.get(), rank.get() + size, rank.get() + n_population, [&](const int &a1, const int &a2){return fitness[a1] < fitness[a2];});
      }
    }
#else
    std::sort(rank.get(), rank.get() + n_population, [&](const int &a1, const int &a2){return fitness[a1] < fitness[a2];});
#endif

    // main loop
    while(iteration < max_iters)
    {


      s.walk[iteration] = positions[rank[0]];

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
    s.best = fitness[0];

    return s;
  }

}
