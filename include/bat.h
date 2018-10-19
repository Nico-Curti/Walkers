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
    typedef std::pair<int, float> best_idx;
    int iteration = 0;
    best_idx best;

    float **Sol = new float*[n_population],
          **S   = new float*[n_population];
          **vel = new float*[n_population];

    std::unique_ptr<float[]> Q(new float[n_population]), // frequency
                             fitness(new float[n_population]),
                             new_fit(new float[n_population]),
                             rng1(new float[n_population]);

    solution s(n_population, dim, max_iters, "BAT");

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

    // initialize the Sol/solutions
#ifdef _OPENMP
#pragma omp for
    for (int i = 0; i < n_population; ++i)
    {
      Sol[i] = new float[dim];
      S[i]   = new float[dim];
      vel[i] = new float[dim];
    }
#else
    std::generate_n(Sol, n_population, [&](){return new float[dim];});
    std::generate_n(S,   n_population, [&](){return new float[dim];});
    std::generate_n(vel, n_population, [&](){return new float[dim];});
#endif

#ifdef _OPENMP
#pragma omp for collapse(2)
    for (int i = 0; i < n_population; ++i)
      for (int j = 0; j < dim; ++j)
        vel[i][j] = 0.f;
#else
    for (int i = 0; i < n_population; ++i)
      std::fill_n(vel[i], dim, 0.f);
#endif

    best.second = inf;
    best.first  = 0;
#ifdef _OPENMP
#pragma omp for reduction(minPair : best)
#endif
    for (int i = 0; i < n_population; ++i)
    {
      fitness[i] = fit(Sol[i]);
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
#pragma omp for
      for (int i = 0; i < n_population; ++i)
      {
        Q[i] = Qmin + (Qmin - Qmax) * rng(engine);
        rng1[i] = rng(engine);
      }
#else
      std::generate_n(Q.get(), n_population, [&](){return Qmin + (Qmin - Qmax) * rng(engine);});
      std::generate_n(rng1.get(), n_population, [&](){return rng(engine);});
#endif

#ifdef _OPENMP
#pragma omp for collapse(2)
#endif
      for (int i = 0; i < n_population; ++i)
        for (int j = 0; j < dim; ++j)
        {
          vel[i][j] += Q[i] * (Sol[i][j] - Sol[best.first][j]);
          S[i][j] = rng1[i] > r ? Sol[best.first][j] + 1e-3f * normal(engine) : Sol[i][j] + vel[i][j];
        }

#ifdef _OPENMP
#pragma omp for reduction(minPair : best)
#endif
      for (int i = 0; i < n_population; ++i)
      {
        float f = fit(S[i]);
        float r = rng(engine);
        fitness[i] = (f <= fitness[i] && r < A) ? f : fitness[i];

        std::copy_n(S[i], dim, Sol[i]);

        best.first  = fitness[i] < best.second ? i          : best.first;
        best.second = fitness[i] < best.second ? fitness[i] : best.second;
      }

      s.walk[iteration] = Sol[best.first];

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
